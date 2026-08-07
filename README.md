# GameDesignStudy

게임의 재미 요소와 핵심 메커닉을 분석하고, 게임 디자이너의 의도를 추론하는 학습 기록 저장소입니다.

> 기획자는 게임의 메커닉(규칙)을 정의하고, 플레이어는 그 규칙을 자유롭게 활용하며 자신의 플레이를 만들어간다.

이 문장을 출발점으로 하루에 한 게임을 분해하는 훈련을 기록하고 있습니다.

## Structure

```
GameDesignStudy
├── AnalysisFramework.md   분석 절차와 언어 규칙
├── GameAnalysis/          게임별 정리된 분석
├── MechanicStudy/         게임 전반에 적용되는 설계 개념 연구
├── TIL/                   날짜별 학습 기록
└── StudyLog/              정리되지 않은 사고 과정 기록
```

세 폴더는 역할이 다릅니다.

| 폴더 | 성격 | 읽는 대상 |
|---|---|---|
| GameAnalysis | 정리된 게임별 분석 | 다른 사람이 읽어도 이해되는 형태 |
| TIL | 그날 무엇을 분석하고 무엇을 배웠는지 | 학습 진행 기록 |
| StudyLog | 실패한 가설, 고민, 바뀐 관점 | 사고 과정 원본 |

TIL은 분석 원문을 축약해서 대체하지 않습니다. 깊은 분석은 GameAnalysis에, 사고 과정은 StudyLog에 남깁니다.

### GameAnalysis

게임별 분석 기록

- [Portal 2](./GameAnalysis/Portal2.md)
- [Vampire Survivors](./GameAnalysis/VampireSurvivors.md)
- [Celeste](./GameAnalysis/Celeste.md)
- [Hollow Knight](./GameAnalysis/HollowKnight.md)
- [Outer Wilds](./GameAnalysis/OuterWilds.md)
- [Paper, Please](./GameAnalysis/PaperPlease.md)
- [INSIDE](./GameAnalysis/INSIDE.md)
- [Slay the Spire](./GameAnalysis/SlayTheSpire.md)
- [Return of the Obra Dinn](./GameAnalysis/ReturnOfTheObraDinn.md)
- [Among Us](./GameAnalysis/AmongUs.md)
- [The Witness](./GameAnalysis/TheWitness.md)
- [Factorio](./GameAnalysis/Factorio.md)
- [Baba Is You](./GameAnalysis/BabaIsYou.md)

### TIL

날짜별 게임 기획 학습 기록 — [전체 목록](./TIL/README.md)

| # | 게임 | 그날의 주제 |
|---|---|---|
| 1 | [Portal 2](./TIL/2026/01-Portal2.md) | 메커닉 간의 결합, 문제 체이닝 |
| 2 | [Vampire Survivors](./TIL/2026/02-VampireSurvivors.md) | 보상 루프, 메커닉 언어화 훈련 |
| 3 | [Celeste](./TIL/2026/03-Celeste.md) | 이동 기술을 자원으로 보기 |
| 4 | [Hollow Knight](./TIL/2026/04-HollowKnight.md) | 개발 의도와 플레이 경험의 구분 |
| 5 | [Outer Wilds](./TIL/2026/05-OuterWilds.md) | 모든 게임이 같은 방식으로 분석되지는 않는다 |
| 6 | [Papers, Please](./TIL/2026/06-PapersPlease.md) | 메커닉과 재미 요소는 같은 것이 아니다 |
| 7 | [INSIDE](./TIL/2026/07-INSIDE.md) | 분석 템플릿 정립, 반복 구조는 설계다 |
| 8 | [Slay the Spire](./TIL/2026/08-SlayTheSpire.md) | 시스템 중심 게임, 핵심 자원의 발견 |
| 9 | [Return of the Obra Dinn](./TIL/2026/09-ReturnOfTheObraDinn.md) | 정보 설계, 확신에 도달하는 과정 |
| 10 | [Baba Is You](./TIL/2026/10-BabaIsYou.md) | 규칙도 메커닉이 될 수 있는가 |
| 11 | [Factorio](./TIL/2026/11-Factorio.md) | 메커닉과 개발 의도의 층위 구분 |
| 12 | [The Witness](./TIL/2026/12-TheWitness.md) | 규칙을 발견하게 만드는 설계 |
| 13 | [Among Us](./TIL/2026/13-AmongUs.md) | 플레이어는 시스템을 최적화한다 |

### MechanicStudy

게임 전반에 적용되는 설계 개념 연구

- [Core Mechanic](./MechanicStudy/CoreMechanic.md) — 게임을 차별화하는 중심 규칙. 행동 메커닉과 시스템 메커닉의 구분, 제거 테스트, 핵심 자원
- [Problem Chaining](./MechanicStudy/ProblemChaining.md) — 플레이어의 사고 순서를 설계하는 기법. 사고 유도 4단계, 오답 설계, 자원 · 정보 · 규칙 체이닝
- [Reward Loop](./MechanicStudy/RewardLoop.md) — 행동을 반복하게 만드는 보상 구조. 가변 보상, 성장 체감, Build Chase Loop

### StudyLog

포트폴리오용 결과물이 아닌, 분석 과정에서 나온 생각과 고민의 기록

- [Game Analysis Study Note](./StudyLog/GameAnalysisNote.md)

## Analysis Framework

상세 절차와 예시는 **[AnalysisFramework.md](./AnalysisFramework.md)** 에 정리되어 있습니다.

### 사고 순서 (분석할 때)

1. **게임의 핵심 요소 나열** — 판단 없이 존재하는 것만 적는다
2. **재미 요소 분석** — 재미 → 이유 → 감정까지 연결한다
3. **없어도 되는 요소** — 제거했을 때 핵심 경험이 유지되는가
4. **메커닉 분석** — 행동 메커닉과 시스템 메커닉을 구분한다
5. **핵심 자원(Core Resource)** — 플레이어는 무엇이 항상 부족한가
6. **개발 의도(가설)** — 이 게임은 무엇을 경험시키기 위해 만들어졌는가

### 문서 순서 (GameAnalysis에 남길 때)

`1. 게임 개요` → `2. Core Experience` → `3. 재미 요소 분석` → `4. 핵심 메커닉 분석` →
`5. 핵심 자원` → `6. 플레이 루프` → `7. Problem Chaining` → `8. 제거/변경 분석` →
`9. 디자이너 의도 추론` → `10. 기획자로서 배울 점`

제거 판단은 **사고에서는 3번**(메커닉을 훑기 전에 던져야 판단이 끌려가지 않는다),
**문서에서는 8번**(근거를 깔고 결론으로 낸다)에 위치합니다.
기준 문서는 [BabaIsYou.md](./GameAnalysis/BabaIsYou.md)입니다.

### 메커닉 언어화 공식

```
행동 → 규칙 → 결과 → 감정
```

가장 자주 빠뜨리는 항목은 **결과**이며, 시스템 결과(`아이템 레벨 +1`)와
플레이 결과(`빌드 방향이 고정된다`)를 구분해서 씁니다.

## 다음 작업

GameAnalysis 템플릿 통일 진행 상황

- [x] 템플릿 확정 (10단계, 핵심 자원 포함, 톤 `~한다`)
- [ ] 배치 1 — SlayTheSpire, Portal2, Celeste, ReturnOfTheObraDinn
- [ ] 배치 2 — VampireSurvivors, HollowKnight, INSIDE
- [ ] 배치 3 — PaperPlease, OuterWilds
- [ ] 배치 4 — AmongUs, TheWitness, Factorio (구조는 있으나 내용 보강 및 핵심 자원 추가 필요)

그 외

- [ ] TIL 각 문서의 `분석일` 채우기
- [ ] TIL/2026/08-07.md 용도 결정 (인덱스 전환 또는 삭제)
- [ ] MechanicStudy에 UXFeedback / FailureDesign 항목 추가 검토
