# GameDesignStudy

게임의 재미와 시스템을 분석하고, 디자이너의 의도를 추론하는 연구 기록입니다.

> 기획자는 게임의 메커닉(규칙)을 정의하고, 플레이어는 그 규칙을 자유롭게 활용하며 자신의 플레이를 만들어간다.

2025년 2월부터 약 18개월간 이어온 작업이며,
**분석 대상보다 분석 방법이 더 많이 바뀌었습니다.**
그 변화 과정은 **[Research Log](./ResearchLog.md)** 에 정리했습니다. 이 저장소를 처음 보신다면 여기부터 읽어주세요.

---

## 구성

문서는 **결과물**과 **과정** 두 성격으로 나뉩니다.

### 결과물

| 폴더 | 관점 | 내용 |
|---|---|---|
| [AnalysisFramework.md](./AnalysisFramework.md) | 방법 | 게임을 분해하는 절차와 언어 규칙 |
| [GameAnalysis/](./GameAnalysis) | **메커닉** | 게임 하나를 10단계 템플릿으로 분석 — 13개 |
| [MechanicStudy/](./MechanicStudy) | **개념** | 여러 게임에서 공통으로 나타난 설계 원리 — 5개 |
| [SystemAnalysis/](./SystemAnalysis) | **서비스 · 경제** | 운영되는 게임의 시스템과 재화 구조 — 3개 |
| [DesignDoc/](./DesignDoc) | **설계** | 직접 만든 기획 산출물 |

### 과정

| 폴더 | 내용 |
|---|---|
| [ResearchLog.md](./ResearchLog.md) | 18개월간 분석 방법이 어떻게 바뀌었는가 |
| [TIL/](./TIL) | 날짜별 학습 기록 13개 + [개념 목록과 판단이 바뀐 기록](./TIL/LearnedConcepts.md) |

```
GameDesignStudy
│
├── ResearchLog.md         ← 여기서 시작
├── AnalysisFramework.md
│
├── GameAnalysis/          메커닉 렌즈
├── MechanicStudy/         개념 연구
├── SystemAnalysis/        서비스 · 경제 렌즈
├── DesignDoc/             설계 산출물
│
└── TIL/                   학습 과정
```

---

## SystemAnalysis — 서비스와 경제

운영 중인 게임의 시스템·재화·성장 구조를 다룹니다.

| 문서 | 기간 | 결론 |
|---|---|---|
| [로스트아크 재련 SWOT](./SystemAnalysis/LostArk_Refining_SWOT.md) | 2025-02 ~ 05 | 비용은 14~15배 증가하는데 딜증은 1.15~1.4%로 고정. **10개월 뒤 실제 패치와 대조 검증 포함** |
| [젠레스 존 제로 성장 곡선](./SystemAnalysis/ZZZ_GrowthCurve.md) | 2026-01 | 이 게임은 플레이 시간이 아니라 **경과 일수로 성장을 통제**한다. 59→60레벨에 70일 |
| [마비노기 모바일 재화 구조와 가격 설계](./SystemAnalysis/Mabinogi_CurrencyMap.md) | 2025-11 ~ 2026-01 | 재화 1,000행 전수 조사. **모든 패키지의 판매가가 거래 재화 값과 정확히 일치** — 성장 아이템은 전부 덤. 월 최대 과금액 226만원 |

## DesignDoc — 설계 산출물

분석에서 얻은 원리를 직접 설계에 적용한 문서입니다.

| 문서 | 기간 | 내용 |
|---|---|---|
| [(가제) 색을 칠하는 총](./DesignDoc/ColorPaint_Concept.md) | 2026-08 | 게임 기획서. **빗나감이 정보가 되는 구조** — 탄환과 정보가 서로를 잡아먹는 자원 설계. 각 요소가 어느 분석에서 나왔는지 대응표 포함 |
| [엘더펜 마을 NPC 컨셉](./DesignDoc/NPC_Elderfen.md) | 2025-06 ~ 11 | NPC 14명 (기능 8 / 장식 6). 관계망 설계 |

## GameAnalysis — 메커닉

| 게임 | 핵심 자원 | 특징 |
|---|---|---|
| [Portal 2](./GameAnalysis/Portal2.md) | 정보 (공간 규칙) | 포탈 메커닉, 문제 체이닝 |
| [Vampire Survivors](./GameAnalysis/VampireSurvivors.md) | 성장 기회 | 보상 루프, 가변 보상, 확률 공간 조작 |
| [Celeste](./GameAnalysis/Celeste.md) | 대시와 스태미너 | 이동 기술의 자원화 |
| [Hollow Knight](./GameAnalysis/HollowKnight.md) | 소울 | 메트로배니아, 불편함이 메커닉인 사례 |
| [Outer Wilds](./GameAnalysis/OuterWilds.md) | 지식 + 루프당 시간 | 소모 자원과 축적 자원의 분리 |
| [Papers, Please](./GameAnalysis/PaperPlease.md) | 시간 | 서로를 잡아먹는 두 자원 |
| [INSIDE](./GameAnalysis/INSIDE.md) | 위험에 대한 사전 정보 | 설명 없는 학습, 실패 비용 설계 |
| [Slay the Spire](./GameAnalysis/SlayTheSpire.md) | 에너지·드로우·체력·골드 | 덱 순환, 시스템 중심 게임 |
| [Return of the Obra Dinn](./GameAnalysis/ReturnOfTheObraDinn.md) | 정보 (연결 대상) | 처벌 없이 신중함을 만드는 구조 |
| [Baba Is You](./GameAnalysis/BabaIsYou.md) | 규칙 | 규칙 자체가 플레이 대상 |
| [Factorio](./GameAnalysis/Factorio.md) | 처리량 | 자원을 유량으로 설계한 사례 |
| [The Witness](./GameAnalysis/TheWitness.md) | 규칙에 대한 가설 | 튜토리얼을 퍼즐로 위장 |
| [Among Us](./GameAnalysis/AmongUs.md) | 신뢰 | 메타 분석, 자원의 소유자 |

## MechanicStudy — 개념 연구

개별 게임이 아니라, 여러 게임에서 반복적으로 나타난 설계 원리를 개념 단위로 묶었습니다.
각 문서는 `정의 → 게임별 사례 비교 → 분석 체크리스트` 구조입니다.

| 문서 | 다루는 질문 |
|---|---|
| [Core Mechanic](./MechanicStudy/CoreMechanic.md) | 이 게임을 다른 게임과 구분하는 규칙은 무엇인가 |
| [Problem Chaining](./MechanicStudy/ProblemChaining.md) | 플레이어가 다음 질문을 스스로 만들게 하려면 |
| [Reward Loop](./MechanicStudy/RewardLoop.md) | 행동을 반복하게 만드는 구조는 |
| [Failure Design](./MechanicStudy/FailureDesign.md) | 실패를 처벌이 아닌 무엇으로 바꿀 수 있는가 |
| [UX Feedback](./MechanicStudy/UXFeedback.md) | 플레이어는 지금 상태를 어떻게 아는가 |

---

## Analysis Framework

상세 절차와 예시는 **[AnalysisFramework.md](./AnalysisFramework.md)** 에 있습니다.

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

### 메커닉 언어화 공식

```
행동 → 규칙 → 결과 → 감정
```

가장 자주 빠뜨리는 항목은 **결과**이며, 시스템 결과(`아이템 레벨 +1`)와
플레이 결과(`빌드 방향이 고정된다`)를 구분해서 씁니다.

---

## 진행 상황

- [x] GameAnalysis 13개 문서를 10단계 템플릿으로 통일
- [x] MechanicStudy 5개 개념 문서 작성
- [x] SystemAnalysis 3개 문서화 (로스트아크 예측 검증 포함)
- [x] DesignDoc — NPC 컨셉 문서화
- [x] Research Log 작성
- [x] 마비노기 유료 상품 가격 설계 분석 완결
- [x] NPC 문서 QA 수정 (Ver1.02)
- [x] 자체 게임 기획서 초안 — 분석에서 설계로 이어지는 경로 확보
- [ ] 기획서 수치 검증 (특히 적개심 누적 구조)
- [ ] 마비노기 무과금 관점 — 골드 일일 수급 측정
- [ ] 젠레스 데니(재화) 축 완성
- [ ] Outer Wilds · INSIDE 직접 플레이 후 재분석
