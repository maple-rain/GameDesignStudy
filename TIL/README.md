# TIL

게임 기획 학습 기록. 하루에 한 게임을 분해하는 훈련의 과정을 남긴다.

이 폴더는 **공부했다는 것을 보여주는 기록**이다.
정리된 결과물은 [GameAnalysis](../GameAnalysis)와 [MechanicStudy](../MechanicStudy)에 있다.

| 구분 | 성격 |
|---|---|
| [GameAnalysis](../GameAnalysis) / [MechanicStudy](../MechanicStudy) | 다른 사람이 읽는 결과물 |
| **TIL** | 그날 무엇을 분석하고 무엇을 배웠는지, 그리고 무엇을 틀렸는지 |

TIL은 분석 원문을 축약한 요약이 아니다.
당일의 사고 과정, 판단이 바뀐 지점, 아쉬웠던 부분을 그대로 남긴다.

## 문서

- [Learned Concepts](./LearnedConcepts.md) — 분석하면서 만든 개념 목록, 판단이 바뀐 기록, 자기 점검 질문

## 2026

2026년 7월 21일부터 하루에 한 게임씩 분해했다.

| 날짜 | 게임 | 그날의 주제 | 얻은 개념 |
|---|---|---|---|
| 07-21 | [Portal 2](./2026/07-21-Portal2.md) | 메커닉 간의 결합, 문제 체이닝 | Core Mechanic, Problem Chaining, UI도 메커닉 |
| 07-22 | [Vampire Survivors](./2026/07-22-VampireSurvivors.md) | 보상 루프, 메커닉 언어화 훈련 | Reward Loop, 언어화 공식, 가변 보상 |
| 07-23 | [Celeste](./2026/07-23-Celeste.md) | 이동 기술을 자원으로 보기 | Resource Chaining, 규칙 지배감 |
| 07-24 | [Hollow Knight](./2026/07-24-HollowKnight.md) | 개발 의도와 플레이 경험의 구분 | 개인적 불편함 ≠ UX 문제 |
| 07-27 | [Outer Wilds](./2026/07-27-OuterWilds.md) | 모든 게임이 같은 방식으로 분석되지는 않는다 | 분석 불가라는 결론 |
| 07-28 | [Papers, Please](./2026/07-28-PapersPlease.md) | 메커닉과 재미 요소는 같은 것이 아니다 | 초회차 / 반복 플레이 분리 |
| 07-29 | [INSIDE](./2026/07-29-INSIDE.md) | 분석 템플릿 정립, 반복 구조는 설계다 | 플레이 필수 / 경험 강화 구분 |
| 07-30 | [Slay the Spire](./2026/07-30-SlayTheSpire.md) | 시스템 중심 게임, 핵심 자원의 발견 | Core Resource, 덱 순환 |
| 08-04 | [Return of the Obra Dinn](./2026/08-04-ReturnOfTheObraDinn.md) | 정보 설계, 확신에 도달하는 과정 | 정보 체이닝, 처벌 없는 신중함 |
| 08-04 | [Baba Is You](./2026/08-04-BabaIsYou.md) | 규칙도 메커닉이 될 수 있는가 | System Mechanic, 제거 테스트의 한계 |
| 08-06 | [Factorio](./2026/08-06-Factorio.md) | 메커닉과 개발 의도의 층위 구분 | 게임 목표 / 플레이어 목표 |
| 08-06 | [The Witness](./2026/08-06-TheWitness.md) | 규칙을 발견하게 만드는 설계 | 튜토리얼 위장, 취향 / UX 판정 |
| 08-07 | [Among Us](./2026/08-07-AmongUs.md) | 플레이어는 시스템을 최적화한다 | 메타 분석, 자원의 소유자 |

### 기록에 대한 메모

- **07-31** — Obra Dinn 분석을 시작했지만 일정 때문에 메모만 남기고 중단했고, 08-04에 본분석을 진행했다.
- **08-04** — Obra Dinn을 마친 뒤 이어서 Baba Is You를 분석해 하루에 두 개를 기록했다.
- **08-06** — Factorio를 마친 뒤 The Witness가 빠진 것을 발견해 같은 날 하나 더 분석했다.

## 작성 형식

```md
# TIL - (게임명) : (그날의 주제)

> 분석일: YYYY-MM-DD (분석 순서 N)
> 관련 분석: [게임명](../../GameAnalysis/게임명.md)

## 오늘의 목표

## (분석 본문)

## 오늘의 핵심 인사이트
```

새 게임을 분석할 때는 [Analysis Framework](../AnalysisFramework.md)의 6단계 사고 순서를 따르고,
결과물은 10단계 문서 템플릿으로 [GameAnalysis](../GameAnalysis)에 남긴다.
