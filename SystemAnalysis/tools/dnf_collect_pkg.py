# -*- coding: utf-8 -*-
"""
트로피컬 바캉스 패키지 수집기 — 세라샵 패키지의 골드 환산 가격과 구성품 시세

본 스크립트는 네오플 오픈 API 서비스를 이용합니다.
결과 데이터의 저작권 등 제반 권리는 (주)네오플 또는 제3자에게 있습니다.
  약관 https://developers.neople.co.kr/contents/policy

왜 만들었나
  2026 여름 패키지가 2026-08-27 점검 전까지만 판매된다.
  판매 종료가 다가올 때 구성품 시세가 어떻게 움직이는지는
  지금 재지 않으면 영영 못 잰다. (API는 최근 100건까지만 준다)

무엇을 재는가
  패키지 본체와 구성품 상자, 개별 아바타 부위가 모두 경매장에서 거래된다.
  따라서 '현금 N원짜리 패키지'를 골드로 환산한 값과
  '구성품을 따로 사 모았을 때의 값'을 나란히 놓고 볼 수 있다.

대상 목록은 pkg_items.json 에 굳혀두었다. (2026-08-12 기준)
목록을 다시 만들려면 build_pkg_list.py 참고.

사용법은 dnf_collect.py 와 같다.
  python dnf_collect_pkg.py           수집
  python dnf_collect_pkg.py --raw     응답 원본 확인
"""
import os, sys, csv, json, time
from datetime import datetime, timezone, timedelta
from urllib.parse import quote
from urllib.request import urlopen, Request
from urllib.error import HTTPError

HERE = os.path.dirname(os.path.abspath(__file__))
KEY_FILE = os.path.join(HERE, "apikey.txt")
ITEM_FILE = os.path.join(HERE, "pkg_items.json")
DATA_DIR = os.path.join(HERE, "data")
BASE = "https://api.neople.co.kr/df"

KST = timezone(timedelta(hours=9))


def load_key():
    """환경변수 DNF_API_KEY 를 먼저 보고, 없으면 apikey.txt 를 읽는다."""
    key = os.environ.get("DNF_API_KEY", "").strip()
    if key:
        return key
    if not os.path.exists(KEY_FILE):
        sys.exit(f"키가 없다. 환경변수 DNF_API_KEY 를 넣거나 {KEY_FILE} 에 한 줄로 적을 것.")
    key = open(KEY_FILE, encoding="utf-8").read().strip()
    if not key:
        sys.exit("apikey.txt 가 비어 있다.")
    return key


def load_items():
    if not os.path.exists(ITEM_FILE):
        sys.exit(f"{ITEM_FILE} 이 없다. build_pkg_list.py 로 만들 것.")
    return json.load(open(ITEM_FILE, encoding="utf-8"))


def call(path, params, key):
    qs = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
    req = Request(f"{BASE}{path}?{qs}&apikey={key}",
                  headers={"User-Agent": "dnf-collect-pkg/1.0"})
    try:
        with urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except HTTPError as e:
        print(f"  HTTP {e.code} — {e.read().decode('utf-8', 'replace')[:200]}")
        return None


def parse_dt(s):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=KST)
        except (ValueError, TypeError):
            continue
    return None


def collect(item, key):
    """한 아이템의 체결 내역과 등록 매물을 한 줄로 요약한다.

    약관 제5조 제5항에 따라 개별 체결 기록은 남기지 않는다.
    받아온 rows 는 여기서 집계하고 버린다.
    """
    iid = item["itemId"]
    sold = call("/auction-sold", {"itemId": iid, "limit": 100}, key)
    live = call("/auction", {"itemId": iid, "limit": 100, "sort": "unitPrice:asc"}, key)
    if sold is None:
        return None

    rows = sold.get("rows", [])
    now = datetime.now(KST)

    prices, times, total_qty = [], [], 0
    for r in rows:
        up = r.get("unitPrice")
        if up is None and r.get("price") and r.get("count"):
            up = r["price"] / r["count"]
        if up:
            prices.append(up)
        total_qty += r.get("count", 0) or 0
        dt = parse_dt(r.get("soldDate") or "")
        if dt:
            times.append(dt)

    prices.sort()
    n = len(prices)
    median = prices[n // 2] if n else None

    span_h = per_h = None
    if len(times) >= 2:
        span_h = round((max(times) - min(times)).total_seconds() / 3600, 3)
        if span_h > 0:
            per_h = round(len(times) / span_h, 2)

    live_rows = (live or {}).get("rows", [])
    live_low = live_avg = None
    live_qty = 0
    for r in live_rows:
        up = r.get("unitPrice")
        if up and (live_low is None or up < live_low):
            live_low = up
        live_qty += r.get("count", 0) or 0
        if live_avg is None and r.get("averagePrice"):
            live_avg = r["averagePrice"]

    return {
        "수집시각": now.strftime("%Y-%m-%d %H:%M:%S"),
        "라벨": item["label"],
        "아이템": item["itemName"],
        "등급": item.get("rarity"),
        "슬롯": item.get("slot"),
        "itemId": iid,
        "체결건수": len(rows),
        "체결수량합": total_qty,
        "체결가_중앙": median,
        "체결가_최저": prices[0] if n else None,
        "체결_최초": min(times).strftime("%Y-%m-%d %H:%M:%S") if times else None,
        "체결_최종": max(times).strftime("%Y-%m-%d %H:%M:%S") if times else None,
        "체결구간_분": round(span_h * 60, 1) if span_h is not None else None,
        "시간당_체결건수": per_h,
        "매물_최저가": live_low,
        "매물_평균가": live_avg,
        "매물_수량": live_qty,
        "매물_등록수": len(live_rows),
    }


FIELDS = ["수집시각", "라벨", "아이템", "등급", "슬롯", "itemId",
          "체결건수", "체결수량합", "체결가_중앙", "체결가_최저",
          "체결_최초", "체결_최종", "체결구간_분", "시간당_체결건수",
          "매물_최저가", "매물_평균가", "매물_수량", "매물_등록수"]


def main():
    key = load_key()
    items = load_items()

    if "--raw" in sys.argv:
        print(json.dumps(call("/auction-sold", {"itemId": items[0]["itemId"], "limit": 2}, key),
                         ensure_ascii=False, indent=2)[:2000])
        return

    os.makedirs(DATA_DIR, exist_ok=True)
    tag = os.environ.get("DNF_COLLECT_TAG", "")
    out = os.path.join(DATA_DIR, f"pkg_{datetime.now(KST):%Y%m}{tag}.csv")
    new = not os.path.exists(out)

    ok = fail = 0
    with open(out, "a", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if new:
            w.writeheader()
        for it in items:
            row = collect(it, key)
            if row:
                w.writerow(row)
                ok += 1
            else:
                fail += 1
                print(f"  실패: {it['label']}")
            time.sleep(0.3)

    print(f"{ok}종 기록 / {fail}종 실패  ->  {out}")


if __name__ == "__main__":
    main()
