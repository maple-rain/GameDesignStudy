# -*- coding: utf-8 -*-
"""
(가제) 보호색 — 색적 4단계와 색 소멸 밸런스 시뮬레이션

검증하려는 질문
    1. 색적을 하는 것이 그냥 난사하는 것보다 이득인가?
    2. 색 지속 시간 40초가 적절한가?
    3. 그림자를 쓸 수 없는 밤이 실제로 난이도를 올리는가?

기획서: ../ColorPaint_Concept.md
"""
import random, statistics
from collections import Counter

# ============================================================
# 파라미터 — 전부 기획서 6장의 제안값이거나, 아래 주석에 근거를 적은 가정값
# ============================================================
MAP_W, MAP_H      = 10, 10     # 맵 면적 100 (기획서 6-1)
AMMO              = 12         # 스테이지 1 탄환 (기획서 6-1)
COVERAGE          = 3          # 발당 커버리지 3칸 (기획서 6-1)
COLOR_DURATION    = 40         # 색 지속 시간(초) (기획서 6-5, 미검증)

ANIMAL_MOVE_P     = 0.25       # 가정: 초당 이동 확률. 값 자체가 검증 대상
SHOT_TIME         = 2          # 가정: 조준 + 발사에 걸리는 시간(초)

# 색적 단계 — (이름, 소요 시간, 후보 축소 후 칸 수, 밤에 사용 가능한가)
SCOUT_STEPS = [
    ("소리 — 대략적 방향", 3, 25, True),
    ("발자국 — 경로",      4, 12, True),
    ("소리 — 정밀 위치",   3,  4, True),
    ("그림자 — 실루엣",    2,  1, False),   # 빛에 의존 (기획서 4장)
]

TRIALS = 20000


class Stage:
    def __init__(self, night=False, color_duration=COLOR_DURATION):
        self.night = night
        self.color_duration = color_duration
        self.cells = MAP_W * MAP_H
        self.animal = random.randrange(self.cells)
        self.ammo = AMMO
        self.t = 0
        self.painted = {}          # cell -> 칠해진 시각
        self.candidates = set(range(self.cells))

    # --- 시간이 흐르면 동물이 움직이고 색이 사라진다 ---
    def advance(self, seconds):
        for _ in range(seconds):
            self.t += 1
            if random.random() < ANIMAL_MOVE_P:
                self.animal = random.randrange(self.cells)
                # 동물이 움직였으므로 색적으로 좁힌 후보가 무효가 된다
                self.candidates = set(range(self.cells)) - self.fresh_paint()
        # 수명이 지난 색은 사라지고 그 칸은 다시 미지가 된다
        expired = [c for c, when in self.painted.items()
                   if self.t - when >= self.color_duration]
        for c in expired:
            del self.painted[c]
            self.candidates.add(c)

    def fresh_paint(self):
        return {c for c, when in self.painted.items()
                if self.t - when < self.color_duration}

    # --- 색적: 단계를 밟을수록 후보가 줄지만 시간이 든다 ---
    def scout(self, upto):
        for i, (_, cost, narrowed, day_only_ok) in enumerate(SCOUT_STEPS):
            if i >= upto:
                break
            if self.night and not day_only_ok:
                break                      # 밤에는 그림자 단계를 쓸 수 없다
            self.advance(cost)
            pool = list(self.candidates - self.fresh_paint())
            if not pool:
                pool = list(range(self.cells))
            keep = min(narrowed, len(pool))
            # 동물이 있는 칸은 반드시 후보에 남는다 (색적이 틀리지는 않는다)
            picked = {self.animal} | set(random.sample(pool, keep))
            self.candidates = picked

    # --- 발사 ---
    def shoot(self):
        self.ammo -= 1
        self.advance(SHOT_TIME)
        pool = list(self.candidates - self.fresh_paint())
        if not pool:
            pool = [c for c in range(self.cells) if c not in self.fresh_paint()] or list(range(self.cells))
        target = random.choice(pool)
        if target == self.animal:
            return True
        # 빗나감 — 주변 COVERAGE칸이 칠해지고, 칠해진 칸은 '동물 없음'으로 확정
        splash = {target}
        while len(splash) < COVERAGE:
            splash.add(random.randrange(self.cells))
        for c in splash:
            if c != self.animal:
                self.painted[c] = self.t
                self.candidates.discard(c)
        return False


def run(strategy_steps, night=False, color_duration=COLOR_DURATION):
    """strategy_steps = 발사 전에 밟을 색적 단계 수"""
    s = Stage(night, color_duration)
    while s.ammo > 0:
        s.scout(strategy_steps)
        if s.shoot():
            return True, AMMO - s.ammo, s.t
    return False, AMMO, s.t


STRATEGIES = [
    ("난사 — 색적 없음", 0),
    ("1단계 — 소리만", 1),
    ("2단계 — 발자국까지", 2),
    ("3단계 — 정밀 소리까지", 3),
    ("4단계 — 그림자까지", 4),
]


def experiment(night=False, color_duration=COLOR_DURATION):
    rows = []
    for name, steps in STRATEGIES:
        wins, ammo_used, times = 0, [], []
        for _ in range(TRIALS):
            ok, used, t = run(steps, night, color_duration)
            if ok:
                wins += 1
                ammo_used.append(used)
                times.append(t)
        rows.append({
            "name": name,
            "steps": steps,
            "rate": wins / TRIALS,
            "ammo": statistics.mean(ammo_used) if ammo_used else float("nan"),
            "time": statistics.mean(times) if times else float("nan"),
        })
    return rows


def table(title, rows):
    print("\n" + title)
    print("  %-22s %8s %10s %10s" % ("전략", "성공률", "평균 탄환", "평균 시간"))
    print("  " + "-" * 54)
    best = max(r["rate"] for r in rows)
    for r in rows:
        mark = "  <-" if r["rate"] == best else ""
        print("  %-22s %7.1f%% %9.1f발 %9.0f초%s"
              % (r["name"], r["rate"] * 100, r["ammo"], r["time"], mark))


if __name__ == "__main__":
    random.seed(20260810)

    print("=" * 60)
    print("(가제) 보호색 — 색적 / 색 소멸 밸런스 시뮬레이션")
    print("맵 %d칸 · 탄환 %d발 · 발당 커버리지 %d · 시행 %d회"
          % (MAP_W * MAP_H, AMMO, COVERAGE, TRIALS))
    print("=" * 60)

    day = experiment(night=False)
    table("[1] 낮 — 색 지속 %d초" % COLOR_DURATION, day)

    night = experiment(night=True)
    table("[2] 밤 — 그림자 단계 사용 불가", night)

    print("\n[3] 색 지속 시간에 따른 변화 (4단계 색적 기준)")
    print("  %-10s %8s %10s %10s" % ("지속 시간", "성공률", "평균 탄환", "평균 시간"))
    print("  " + "-" * 42)
    for d in (10, 20, 30, 40, 60, 90, 9999):
        rows = experiment(night=False, color_duration=d)
        r = rows[-1]
        label = "무한" if d > 1000 else "%d초" % d
        print("  %-10s %7.1f%% %9.1f발 %9.0f초" % (label, r["rate"] * 100, r["ammo"], r["time"]))

    print("\n[4] 동물 이동 확률에 따른 색적의 가치")
    print("  %-8s %14s %14s %10s" % ("이동확률", "난사 성공률", "4단계 성공률", "차이"))
    print("  " + "-" * 50)
    for p in (0.0, 0.1, 0.25, 0.5, 0.8):
        globals()["ANIMAL_MOVE_P"] = p
        rows = experiment(night=False)
        a, b = rows[0]["rate"], rows[-1]["rate"]
        print("  %-8.2f %13.1f%% %13.1f%% %+9.1f%%p" % (p, a * 100, b * 100, (b - a) * 100))
    globals()["ANIMAL_MOVE_P"] = 0.25
