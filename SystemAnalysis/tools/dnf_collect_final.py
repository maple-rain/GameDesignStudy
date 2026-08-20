# -*- coding: utf-8 -*-
"""판매 종료 구간 집중 수집기 — 2026-08-27 06시 전후

왜 따로 만들었나
  주 수집기는 2시간 간격이다. 그 간격으로는 종료 직전 급락을 4~5점으로만 잡는다.
  게다가 회차 시각을 보면 05:32 다음이 07:29 라서 06시 삭제 시점에 관측점이 없다.
  삭제된 뒤에는 경매장 조회가 되지 않을 수 있으므로 그 구간은 지금 아니면 못 잰다.

무엇을 재는가
  주 수집기 133종 중 종료 전후 판단에 쓰이는 19종만 고른다.
  삭제 대상 12종, 존속 대상 5종, 만기가 다른 대조군 2종.
  전량을 15분마다 받으면 API 부담이 커서 대상을 좁혔다.

사용법
  python dnf_collect_final.py                      1회 수집
  FINAL_LOOP_MIN=300 FINAL_INTERVAL_SEC=300 \
  python dnf_collect_final.py                      300분 동안 5분 간격 반복

본 스크립트는 네오플 오픈 API 서비스를 이용합니다.
결과 데이터의 저작권 등 제반 권리는 (주)네오플 또는 제3자에게 있습니다.
  약관 https://developers.neople.co.kr/contents/policy
약관 제5조 제5항에 따라 개별 체결 기록은 남기지 않고 집계값만 저장한다.
"""
import csv
import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from dnf_collect_pkg import FIELDS, collect, load_key  # noqa: E402

ITEM_FILE = os.path.join(HERE, "pkg_items.json")
DATA_DIR = os.path.join(HERE, "data")
KST = timezone(timedelta(hours=9))

# 판매 종료: 2026-08-27 06:00 KST
DEADLINE = datetime(2026, 8, 27, 6, 0, tzinfo=KST)

# 8월 27일 06시에 삭제되는 것 — 급락을 재는 대상
DELETED = [
    "트로피컬 바캉스 패키지",
    "트로피컬 바캉스 아바타 풀세트 상자",
    "트로피컬 바캉스 오라 상자",
    "트로피컬 바캉스 칭호 상자",
    "트로피컬 바캉스 크리쳐 상자",
    "트로피컬 바캉스 세라 상자",
    "트로피컬 바캉스 무기 아바타 상자",
    "트로피컬 바캉스 오라 변경권",
    "트로피컬 에너지 카드",
    "트로피컬 바캉스 칭호 보주",
    "프리미엄 플래티넘 엠블렘 선택 상자",
    "프리미엄 플래티넘 엠블렘 선택 상자#2",
]

# 삭제되지 않는 것 — 종료 후 오르는지 재는 대상
SURVIVES = [
    "트로피컬 바캉스 아바타 풀세트 상자[E타입][무제한]",
    "트로피컬 바캉스 스페셜 모자 아바타 상자[무제한]",
    "열대야의 추억 오라 상자",
    "청량한 바다의 기억 오라 상자",
    "따스한 노을의 기억 오라 상자",
]

# 만기가 다르거나 이 패키지와 무관한 대조군
CONTROL = [
    "황금빛 장비 증폭권[골고라이언] 상자",   # 만기 2026-12-24
    "황홀한 여름밤 바캉스 칭호 선택 상자",     # 기간 무제한
]

WANTED = {label: group for group, labels in
          (("삭제", DELETED), ("존속", SURVIVES), ("대조", CONTROL))
          for label in labels}


def pick_items():
    """주 수집 목록에서 대상 19종만 골라낸다. 빠진 이름은 실패로 알린다."""
    allitems = json.load(open(ITEM_FILE, encoding="utf-8"))
    bylabel = {i["label"]: i for i in allitems}
    picked, missing = [], []
    for label in WANTED:
        if label in bylabel:
            it = dict(bylabel[label])
            it["group"] = WANTED[label]
            picked.append(it)
        else:
            missing.append(label)
    return picked, missing


def one_pass(items, key, writer, fh):
    now = datetime.now(KST)
    ok = fail = 0
    for it in items:
        row = collect(it, key)
        if row:
            row["구분"] = it["group"]
            writer.writerow(row)
            ok += 1
        else:
            fail += 1
            print(f"    실패: {it['label']}", flush=True)
        time.sleep(0.25)
    fh.flush()
    left = DEADLINE - now
    hrs = left.total_seconds() / 3600
    print(f"  {now:%m-%d %H:%M:%S}  {ok}종 기록 / {fail}종 실패"
          f"   종료까지 {hrs:.1f}시간", flush=True)
    return ok, fail


def main():
    items, missing = pick_items()
    print(f"대상 {len(items)}종  "
          f"(삭제 {sum(1 for i in items if i['group']=='삭제')} / "
          f"존속 {sum(1 for i in items if i['group']=='존속')} / "
          f"대조 {sum(1 for i in items if i['group']=='대조')})")
    if missing:
        print(f"★ 주 목록에서 못 찾은 이름 {len(missing)}개: {missing}")
    if not items:
        sys.exit("대상이 비었다. pkg_items.json 을 확인할 것.")

    loop_min = int(os.environ.get("FINAL_LOOP_MIN", "0") or 0)
    interval = int(os.environ.get("FINAL_INTERVAL_SEC", "300") or 300)

    os.makedirs(DATA_DIR, exist_ok=True)
    # 파일명이 _ci.csv 로 끝나야 .gitignore 예외에 걸려 저장소에 남는다
    out = os.path.join(DATA_DIR, f"pkg_{datetime.now(KST):%Y%m}_final_ci.csv")
    new = not os.path.exists(out)
    key = load_key()
    fields = FIELDS + ["구분"]

    started = datetime.now(KST)
    passes = 0
    with open(out, "a", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        if new:
            w.writeheader()
        while True:
            one_pass(items, key, w, fh)
            passes += 1
            if loop_min <= 0:
                break
            elapsed = (datetime.now(KST) - started).total_seconds() / 60
            if elapsed + interval / 60 > loop_min:
                break
            time.sleep(interval)

    print(f"{passes}회 수집  ->  {out}")


if __name__ == "__main__":
    main()
