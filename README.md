# edu-2026h2-agent-loop

2026 하반기 3회차 **Harness·Loop Engineering과 최소 Agent Loop** (EDU-2026-H2-03, 2026-09-17) 실습 저장소입니다.

프레임워크 없이 while 루프 하나로 Agent를 만듭니다. 8회차에서 이 코드를 LangGraph로 옮깁니다.

환경: Python 3.12, Conda 환경 `hs-2026h2`

| 파일 | 내용 |
| --- | --- |
| `tools.py` | Tool 함수와 스키마 (`TOOLS` 딕셔너리) |
| `tracing.py` | 단계별 기록을 `traces/*.jsonl`로 저장 |
| `agent_loop.py` | 최소 Agent Loop: 최대 단계, 재시도, 종료 조건 |
| `failure_cases.md` | 일부러 실패시키는 시나리오 3개 |

> 표준 라이브러리 `trace` 모듈과 이름이 겹치지 않도록 기록 파일 이름은 `tracing.py`입니다.

## 과제: 안전하게 종료되는 Agent Loop

- 최대 단계, Tool 오류 재시도 제한, 같은 Tool·같은 인자 반복 감지 세 가지 종료 조건
- 실패 시나리오 3개의 Trace 첨부
- 기한: 9/30(수) 23:59 (추석 연휴로 2주)
