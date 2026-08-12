# -*- coding: utf-8 -*-
"""
던전앤파이터 경매장 수집기 — 소울 결정 5종의 체결가와 거래 속도

본 스크립트는 네오플 오픈 API 서비스를 이용합니다.
결과 데이터의 저작권 등 제반 권리는 (주)네오플 또는 제3자에게 있습니다.
  약관 https://developers.neople.co.kr/contents/policy

약관 제5조 제5항에 따라 개별 체결 기록은 저장하지 않는다.
받아온 rows는 메모리에서 집계한 뒤 버리고, 중앙값·건수·시간 폭만 CSV로 남긴다.
호출량은 실행 1회당 10회(아이템 5종 x 엔드포인트 2개), 호출 간 0.5초를 둔다.

네오플 공개 API 두 개를 함께 쓴다.
  /df/auction-sold   최근 체결 내역 (최대 100건 / 1개월)  → 수요
  /df/auction        현재 등록 매물                        → 공급

auction-sold 가 100건까지만 주는 것을 역이용한다.
100건이 쌓이는 데 걸린 시간을 재면 그것이 곧 거래 속도다.

사용법
  1. https://developers.neople.co.kr 에서 apikey 발급
  2. 이 폴더에 apikey.txt 를 만들고 키만 한 줄로 적는다 (git에 올리지 않는다)
  3. python dnf_collect.py
  4. 하루 2~3회 실행하면 data/ 아래 csv가 쌓인다

첫 실행 시 --raw 를 붙이면 응답 원본을 그대로 출력한다.
필드명이 문서와 다를 수 있으므로 처음 한 번은 이걸로 확인할 것.
  python dnf_collect.py --raw
"""
import os, sys, csv, json, time
from datetime import datetime, timezone, timedelta
from urllib.parse import quote
from urllib.request import urlopen, Request
from urllib.error import HTTPError

HERE = os.path.dirname(os.path.abspath(__file__))
KEY_FILE = os.path.join(HERE, "apikey.txt")
DATA_DIR = os.path.join(HERE, "data")
BASE = "https://api.neople.co.kr/df"

# 수집 대상
# itemId로 조회한다. itemName + wordType=full 은 전체 텍스트 검색이라
# 이름이 비슷한 다른 아이템이 섞여 들어온다. (2026-08-12 확인)
# ID는 /df/items?itemName=...&wordType=match 로 얻었다.
ITEMS = {
    "레어 소울 결정":     "c4816db14d145416921f0210063cb014",
    "유니크 소울 결정":   "0620c107b1aae1f3a6cf9eee3aaf43d7",
    "레전더리 소울 결정": "c6947ff630cc59aebdcbabfb449258d1",
    "에픽 소울 결정":     "c7d845c65ab9dbcff6e55dc910fbea87",
    "태초 소울 결정":     "d288ebf406a65f4ec23d1f9c33227888",
}

KST = timezone(timedelta(hours=9))


def load_key():
    """환경변수 DNF_API_KEY 를 먼저 보고, 없으면 apikey.txt 를 읽는다.

    GitHub Actions에서는 Secrets가 환경변수로 들어오므로 파일이 필요 없다.
    로컬에서는 기존처럼 apikey.txt 를 쓴다.
    """
    key = os.environ.get("DNF_API_KEY", "").strip()
    if key:
        return key
    if not os.path.exists(KEY_FILE):
        sys.exit(f"키가 없다. 환경변수 DNF_API_KEY 를 넣거나 {KEY_FILE} 에 한 줄로 적을 것.")
    key = open(KEY_FILE, encoding="utf-8").read().strip()
    if not key:
        sys.exit("apikey.txt 가 비어 있다.")
    return key


def call(path, params, key):
    qs = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
    url = f"{BASE}{path}?{qs}&apikey={key}"
    req = Request(url, headers={"User-Agent": "dnf-collect/1.0"})
    try:
        with urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:300]
        print(f"  HTTP {e.code} — {body}")
        return None


def parse_dt(s):
    """API가 주는 시각 문자열을 datetime으로. 형식이 다르면 None."""
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=KST)
        except (ValueError, TypeError):
            continue
    return None


def collect(name, item_id, key):
    """한 아이템의 체결 내역과 등록 매물을 한 줄로 요약한다."""
    sold = call("/auction-sold", {"itemId": item_id, "limit": 100}, key)
    live = call("/auction", {"itemId": item_id, "limit": 100, "sort": "unitPrice:asc"}, key)
    if sold is None:
        return None

    rows = sold.get("rows", [])
    now = datetime.now(KST)

    # 체결가 — unitPrice 가 있으면 그것을, 없으면 price / count 로 계산
    prices = []
    times = []
    total_qty = 0
    for r in rows:
        up = r.get("unitPrice")
        if up is None and r.get("price") and r.get("count"):
            up = r["price"] / r["count"]
        if up:
            prices.append(up)
        total_qty += r.get("count", 0) or 0
        dt = parse_dt(r.get("soldDate") or r.get("soldDate ") or "")
        if dt:
            times.append(dt)

    prices.sort()
    n = len(prices)
    median = prices[n // 2] if n else None
    lowest = prices[0] if n else None

    # 거래 속도 — 100건(또는 n건)이 쌓인 시간 폭
    span_h = None
    per_h = None
    if len(times) >= 2:
        span = max(times) - min(times)
        span_h = round(span.total_seconds() / 3600, 3)
        if span_h > 0:
            per_h = round(len(times) / span_h, 2)

    live_rows = (live or {}).get("rows", [])
    live_low = None
    live_qty = 0
    live_avg = None
    for r in live_rows:
        up = r.get("unitPrice")
        if up and (live_low is None or up < live_low):
            live_low = up
        live_qty += r.get("count", 0) or 0
        if live_avg is None and r.get("averagePrice"):
            live_avg = r["averagePrice"]      # API가 주는 시장 평균가

    return {
        "수집시각": now.strftime("%Y-%m-%d %H:%M:%S"),
        "아이템": name,
        "체결건수": len(rows),
        "체결수량합": total_qty,
        "체결가_중앙": median,
        "체결가_최저": lowest,
        "체결_최초": min(times).strftime("%Y-%m-%d %H:%M:%S") if times else None,
        "체결_최종": max(times).strftime("%Y-%m-%d %H:%M:%S") if times else None,
        "체결구간_분": round(span_h * 60, 1) if span_h is not None else None,
        "시간당_체결건수": per_h,
        "매물_최저가": live_low,
        "매물_평균가": live_avg,
        "매물_수량": live_qty,
        "매물_등록수": len(live_rows),
    }


FIELDS = ["수집시각", "아이템", "체결건수", "체결수량합", "체결가_중앙", "체결가_최저",
          "체결_최초", "체결_최종", "체결구간_분", "시간당_체결건수",
          "매물_최저가", "매물_평균가", "매물_수량", "매물_등록수"]


def main():
    key = load_key()

    if "--raw" in sys.argv:
        tid = ITEMS["태초 소울 결정"]
        print("=== auction-sold 원본 (태초 소울 결정) ===")
        print(json.dumps(call("/auction-sold", {"itemId": tid, "limit": 3}, key),
                         ensure_ascii=False, indent=2)[:3000])
        print("\n=== auction 원본 ===")
        print(json.dumps(call("/auction", {"itemId": tid, "limit": 3}, key),
                         ensure_ascii=False, indent=2)[:3000])
        return

    os.makedirs(DATA_DIR, exist_ok=True)

    # 수집 주체를 파일명으로 나눈다. 로컬과 CI가 같은 파일을 건드리면
    # git에서 매번 충돌이 나기 때문이다. CI는 DNF_COLLECT_TAG=_ci 로 돈다.
    tag = os.environ.get("DNF_COLLECT_TAG", "")
    out = os.path.join(DATA_DIR, f"soul_{datetime.now(KST):%Y%m}{tag}.csv")
    new = not os.path.exists(out)

    with open(out, "a", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if new:
            w.writeheader()
        for name, item_id in ITEMS.items():
            row = collect(name, item_id, key)
            if row:
                w.writerow(row)
                span = row["체결구간_분"]
                span_s = f"{span:>7.1f}분" if span is not None else "     —  "
                print(f"{name:16} 체결 {row['체결건수']:>3}건 / {span_s}"
                      f"  중앙가 {row['체결가_중앙'] or '-':>10}"
                      f"  매물 {row['매물_등록수']:>3}건")
            else:
                print(f"{name:16} 실패")
            time.sleep(0.5)

    print(f"\n저장: {out}")


if __name__ == "__main__":
    main()
