# -*- coding: utf-8 -*-
"""판매 종료 구간 집중 수집기 — 2026-08-27 06시 전후

왜 따로 만들었나
  주 수집기는 2시간 간격이다. 그 간격으로는 종료 직전 급락을 4~5점으로만 잡는다.
  게다가 회차 시각을 보면 05:32 다음이 07:29 라서 06시 삭제 시점에 관측점이 없다.
  삭제된 뒤에는 경매장 조회가 되지 않을 수 있으므로 그 구간은 지금 아니면 못 잰다.

무엇을 재는가
  주 수집기 133종 중 종료 전후 판단에 쓰이는 33종만 고른다.
  삭제 대상 12종, 존속 대상 5종, 만기가 다른 대조군 2종,
  세트별 9부위 합계를 내기 위한 아바타 개별 부위 14종.
  전량을 짧은 주기로 받으면 API 부담이 커서 대상을 좁혔다.
  약관 제5조 제8항이 주기적·지속적 접속으로 인한 과부하를 금지한다.

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

# 아바타 개별 부위 — 세트별 9부위 합계를 종료 순간에 재기 위한 A타입 14종.
#
# 풀세트 상자(교환가능)는 8/27 06시 삭제되지만, 개봉해서 나온 아바타 9부위는
# 교환가능 · 기간 무제한이라 남는다. 즉 개별 부위가 종료 후 시장에 남는
# 유일한 아바타 형태다. 상자가 사라지고 부위가 남는 순간을 재려면 부위가 필요하다.
#
# 어떤 테마도 9슬롯을 다 덮지 않는다. 귤 5부위 · 오렌지 3 · 시계 1 · 수박 1 이고
# 머리 · 목가슴 · 신발 · 스킨은 테마 없는 공용 품목으로 채운다.
# 공용 4부위를 공유하므로 14종이면 네 세트의 9부위 합계를 모두 낼 수 있다.
# 문서 7장의 '세트별 9부위 합계'와 같은 방식으로 묶을 수 있게 세트를 열로 남긴다.
AVATAR = [
    ("귤", "트로피컬 바캉스 미니 귤 핀[A타입]"),
    ("귤", "트로피컬 바캉스 렌즈와 귤 귀걸이[A타입]"),
    ("귤", "트로피컬 바캉스 귤 수영복 상의[A타입]"),
    ("귤", "트로피컬 바캉스 귤 수영복 하의[A타입]"),
    ("귤", "트로피컬 바캉스 귤 랩 스커트[A타입]"),
    ("오렌지", "트로피컬 바캉스 오렌지 무늬 스티커[A타입]"),
    ("오렌지", "트로피컬 바캉스 오렌지 무늬 씰[A타입]"),
    ("오렌지", "트로피컬 바캉스 오렌지 무늬 수영복[A타입]"),
    ("시계", "트로피컬 바캉스 시계와 목걸이[A타입]"),
    ("수박", "트로피컬 바캉스 수박 수영복 하의[A타입]"),
    ("공용", "트로피컬 바캉스 투블럭 헤어[A타입]"),
    ("공용", "트로피컬 바캉스 목가슴 투명 아바타[A타입]"),
    ("공용", "트로피컬 바캉스 밴드[A타입]"),
    ("공용", "트로피컬 바캉스 진줏빛 피부[A타입]"),
]

WANTED = {label: (group, "") for group, labels in
          (("삭제", DELETED), ("존속", SURVIVES), ("대조", CONTROL))
          for label in labels}
for _set, _label in AVATAR:
    WANTED[_label] = ("아바타", _set)


def pick_items():
    """주 수집 목록에서 대상만 골라낸다. 빠진 이름은 실패로 알린다."""
    allitems = json.load(open(ITEM_FILE, encoding="utf-8"))
    bylabel = {i["label"]: i for i in allitems}
    picked, missing = [], []
    for label, (group, setname) in WANTED.items():
        if label in bylabel:
            it = dict(bylabel[label])
            it["group"] = group
            it["set"] = setname
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
            row["세트"] = it["set"]
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


def push(out, passes):
    """수집 도중에 중간 커밋한다.

    장기 실행(350분)은 잡이 끝나야 워크플로가 커밋한다. 그사이 잡이 취소되거나
    러너가 죽으면 여섯 시간치가 통째로 사라진다. 이 구간은 판매 종료 전이라
    다시 못 받는다. 그래서 몇 회마다 끊어서 올린다.

    파일을 열어 둔 채로 rebase 하면 파일이 새로 쓰이면서 열린 fd 가 없어진 쪽을
    가리킨다. 그래서 main() 은 매 회차마다 열고 닫는다.
    """
    import subprocess

    def run(*a):
        return subprocess.run(a, capture_output=True, text=True)

    if not run("git", "config", "user.name").stdout.strip():
        run("git", "config", "user.name", "github-actions[bot]")
        run("git", "config", "user.email",
            "41898282+github-actions[bot]@users.noreply.github.com")

    run("git", "add", out)
    if run("git", "diff", "--staged", "--quiet").returncode == 0:
        print("  중간 커밋: 변화 없음", flush=True)
        return
    stamp = f"{datetime.now(KST):%Y-%m-%d %H:%M}"
    run("git", "commit", "-m", f"종료 구간 수집 중간 {stamp} KST ({passes}회차)")
    for _ in range(5):
        if (run("git", "pull", "--rebase", "origin", "main").returncode == 0
                and run("git", "push", "origin", "main").returncode == 0):
            print(f"  중간 커밋 완료 ({passes}회차)", flush=True)
            return
        # 충돌한 채로 두면 다음 회차의 add/commit 이 전부 어긋난다.
        run("git", "rebase", "--abort")
        time.sleep(15)
    # 커밋은 로컬에 남아 있다. 워크플로 마지막 「커밋」 단계가 이걸 찾아서 올린다.
    print("  ★ 중간 푸시 실패. 로컬 커밋은 남아 있고 다음 회차에 다시 시도한다.", flush=True)


def main():
    items, missing = pick_items()
    print(f"대상 {len(items)}종  "
          f"(삭제 {sum(1 for i in items if i['group']=='삭제')} / "
          f"존속 {sum(1 for i in items if i['group']=='존속')} / "
          f"대조 {sum(1 for i in items if i['group']=='대조')} / "
          f"아바타 {sum(1 for i in items if i['group']=='아바타')})")
    if missing:
        print(f"★ 주 목록에서 못 찾은 이름 {len(missing)}개: {missing}")
    if not items:
        sys.exit("대상이 비었다. pkg_items.json 을 확인할 것.")

    loop_min = int(os.environ.get("FINAL_LOOP_MIN", "0") or 0)
    interval = int(os.environ.get("FINAL_INTERVAL_SEC", "300") or 300)
    # 0 이면 중간 커밋을 하지 않는다. 로컬에서 돌릴 때의 기본값이다.
    push_every = int(os.environ.get("FINAL_PUSH_EVERY", "0") or 0)

    os.makedirs(DATA_DIR, exist_ok=True)
    # 파일명이 _ci.csv 로 끝나야 .gitignore 예외에 걸려 저장소에 남는다
    out = os.path.join(DATA_DIR, f"pkg_{datetime.now(KST):%Y%m}_final_ci.csv")
    new = not os.path.exists(out)
    key = load_key()
    fields = FIELDS + ["구분", "세트"]

    started = datetime.now(KST)
    passes = 0
    # 중간 커밋이 파일을 새로 쓸 수 있어서 매 회차마다 열고 닫는다.
    while True:
        with open(out, "a", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            if new:
                w.writeheader()
                new = False
            one_pass(items, key, w, fh)
        passes += 1
        if loop_min <= 0:
            break
        if push_every and passes % push_every == 0:
            push(out, passes)
        elapsed = (datetime.now(KST) - started).total_seconds() / 60
        if elapsed + interval / 60 > loop_min:
            break
        time.sleep(interval)

    print(f"{passes}회 수집  ->  {out}")


if __name__ == "__main__":
    main()
