# GameDesignStudy

게임의 재미 요소와 핵심 메커닉을 분석하고, 게임 디자이너의 의도를 추론하는 학습 기록 저장소입니다.

> 기획자는 게임의 메커닉(규칙)을 정의하고, 플레이어는 그 규칙을 자유롭게 활용하며 자신의 플레이를 만들어간다.

이 문장을 출발점으로 하루에 한 게임을 분해하는 훈련을 기록하고 있습니다.
현재까지 13개 게임을 분석했습니다.

---

## 이 저장소의 구성

이 저장소는 두 가지 성격의 문서로 나뉩니다.

### 1. 결과물 — 기획 분석 문서

다른 사람이 읽는 것을 전제로 작성한 문서입니다. 통일된 템플릿과 서술체를 사용합니다.

| 폴더 | 내용 |
|---|---|
| [AnalysisFramework.md](./AnalysisFramework.md) | 게임을 분해하는 절차와 언어 규칙 |
| [GameAnalysis/](./GameAnalysis) | 게임 하나를 10단계 템플릿으로 분석한 문서 (13개) |
| [MechanicStudy/](./MechanicStudy) | 여러 게임에서 공통으로 발견한 설계 개념 연구 (5개) |

### 2. 과정 — 학습 기록

무엇을 공부했고 무엇을 틀렸는지를 남긴 기록입니다. 1인칭으로 작성합니다.

| 폴더 | 내용 |
|---|---|
| [TIL/](./TIL) | 날짜별 분석 기록 (13개) + [개념 목록과 판단이 바뀐 기록](./TIL/LearnedConcepts.md) |

```
GameDesignStudy
│
├── AnalysisFramework.md   분석 절차와 언어 규칙
├── GameAnalysis/          게임별 분석 결과물
├── MechanicStudy/         게임 전반에 적용되는 설계 개념 연구
│
└── TIL/                   학습 과정 기록
    ├── LearnedConcepts.md 개념 목록 / 바뀐 생각 / 자기 점검
    └── 2026/              날짜별 기록
```

TIL은 분석 원문을 축약한 요약이 아닙니다.
깊은 분석은 GameAnalysis에, 개념 정리는 MechanicStudy에, 사고 과정은 TIL에 남깁니다.

---

## GameAnalysis

게임 하나를 10단계 템플릿으로 분석한 문서입니다.

| 게임 | 핵심 자원 | 특징 |
|---|---|---|
| [Portal 2](./GameAnalysis/Portal2.md) | 정보 (공간 규칙) | 포탈 메커닉, 문제 체이닝 |
| [Vampire Survivors](./GameAnalysis/VampireSurvivors.md) | 성장 기회 | 보상 루프, 가변 보상, 확률 공간 조작 |
| [Celeste](./GameAnalysis/Celeste.md) | 대시와 스태미너 | 이동 기술의 자원화, 난이도 설계 |
| [Hollow Knight](./GameAnalysis/HollowKnight.md) | 소울 | 메트로배니아, 지도 시스템, 탐험 |
| [Outer Wilds](./GameAnalysis/OuterWilds.md) | 지식과 루프당 시간 | 소모 자원과 축적 자원의 분리 |
| [Paper, Please](./GameAnalysis/PaperPlease.md) | 시간 | 도덕적 딜레마, 정보 대조 |
| [INSIDE](./GameAnalysis/INSIDE.md) | 위험에 대한 사전 정보 | 환경 스토리텔링, 암묵적 학습 |
| [Slay the Spire](./GameAnalysis/SlayTheSpire.md) | 에너지·드로우·체력·골드 | 덱 순환, 로그라이크, 선택 |
| [Return of the Obra Dinn](./GameAnalysis/ReturnOfTheObraDinn.md) | 정보 (연결 대상) | 추리, 정보 연결, 검증 |
| [Baba Is You](./GameAnalysis/BabaIsYou.md) | 규칙 | 규칙 변경 메커닉 |
| [Factorio](./GameAnalysis/Factorio.md) | 처리량 | 자동화, 시스템 설계 |
| [The Witness](./GameAnalysis/TheWitness.md) | 규칙에 대한 가설 | 퍼즐 학습, 문제 체이닝 |
| [Among Us](./GameAnalysis/AmongUs.md) | 신뢰 | 사회적 추론, 정보 비대칭, 메타 분석 |

## MechanicStudy

개별 게임 분석이 아니라, **여러 게임에서 반복적으로 나타난 설계 원리**를 개념 단위로 묶은 연구입니다.
각 문서는 정의 → 게임별 사례 비교 → 분석 체크리스트 순서로 구성됩니다.

| 문서 | 다루는 질문 |
|---|---|
| [Core Mechanic](./MechanicStudy/CoreMechanic.md) | 이 게임을 다른 게임과 구분하는 규칙은 무엇인가 |
| [Problem Chaining](./MechanicStudy/ProblemChaining.md) | 플레이어가 다음 질문을 스스로 만들게 하려면 |
| [Reward Loop](./MechanicStudy/RewardLoop.md) | 플레이어가 행동을 반복하게 만드는 구조는 |
| [Failure Design](./MechanicStudy/FailureDesign.md) | 실패를 처벌이 아닌 무엇으로 바꿀 수 있는가 |
| [UX Feedback](./MechanicStudy/UXFeedback.md) | 플레이어는 지금 상태를 어떻게 아는가 |

## TIL

2026년 7월 21일부터 하루에 한 게임씩 분해했습니다. — [전체 목록](./TIL/README.md)

| 날짜 | 게임 | 그날의 주제 |
|---|---|---|
| 07-21 | [Portal 2](./TIL/2026/07-21-Portal2.md) | 메커닉 간의 결합, 문제 체이닝 |
| 07-22 | [Vampire Survivors](./TIL/2026/07-22-VampireSurvivors.md) | 보상 루프, 메커닉 언어화 훈련 |
| 07-23 | [Celeste](./TIL/2026/07-23-Celeste.md) | 이동 기술을 자원으로 보기 |
| 07-24 | [Hollow Knight](./TIL/2026/07-24-HollowKnight.md) | 개발 의도와 플레이 경험의 구분 |
| 07-27 | [Outer Wilds](./TIL/2026/07-27-OuterWilds.md) | 모든 게임이 같은 방식으로 분석되지는 않는다 |
| 07-28 | [Papers, Please](./TIL/2026/07-28-PapersPlease.md) | 메커닉과 재미 요소는 같은 것이 아니다 |
| 07-29 | [INSIDE](./TIL/2026/07-29-INSIDE.md) | 분석 템플릿 정립, 반복 구조는 설계다 |
| 07-30 | [Slay the Spire](./TIL/2026/07-30-SlayTheSpire.md) | 시스템 중심 게임, 핵심 자원의 발견 |
| 08-04 | [Return of the Obra Dinn](./TIL/2026/08-04-ReturnOfTheObraDinn.md) | 정보 설계, 확신에 도달하는 과정 |
| 08-04 | [Baba Is You](./TIL/2026/08-04-BabaIsYou.md) | 규칙도 메커닉이 될 수 있는가 |
| 08-06 | [Factorio](./TIL/2026/08-06-Factorio.md) | 메커닉과 개발 의도의 층위 구분 |
| 08-06 | [The Witness](./TIL/2026/08-06-TheWitness.md) | 규칙을 발견하게 만드는 설계 |
| 08-07 | [Among Us](./TIL/2026/08-07-AmongUs.md) | 플레이어는 시스템을 최적화한다 |

---

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

---

## 다음 작업

- [x] GameAnalysis 13개 문서를 10단계 템플릿으로 통일 (톤 `~한다`, 핵심 자원 포함)
- [x] MechanicStudy에 FailureDesign / UXFeedback 추가
- [x] 문서 성격을 결과물 / 학습 기록 2가지로 정리
- [x] TIL 파일명과 `분석일`을 실제 분석 날짜로 정리
- [ ] Outer Wilds 직접 플레이 후 재분석
- [ ] INSIDE 사운드 포함 재분석
