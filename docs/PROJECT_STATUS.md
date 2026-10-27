# Mobility Choice 진행 현황

기준일: 2026-10-27.

## 반영 대상

- 기존 `main`: 차량 탐색·상세·비교, Express/JWT/MongoDB 차량 API.
- 기존 `feat/ai-advisor` (`278a3c3`): Next.js → FastAPI → 인증된 차량 API → 규칙 추천 → Ollama 설명, SSE 스트리밍.
- 미커밋 `ranking_service.py`: 예산·차종·동력·국산/수입·필수 기능을 필터로 사용하고, 통과 후보를 가격 오름차순 정렬.
- 이번 정리: 필수 조건 회귀 테스트, SSE Cache-Control 헤더 오타 수정, 실행·남은 작업 문서.

## 현재 추천 계약

- 예산 입력은 만 원, 차량 시작 가격은 원입니다.
- 여러 차종·동력·국산/수입 선택은 그중 하나가 일치하면 통과합니다. 기능은 선택한 항목을 모두 만족해야 합니다.
- 동력은 문자열 포함 검사입니다. `가솔린`은 `가솔린 하이브리드`도 통과할 수 있습니다.
- 비선택 조건은 필터하지 않으며 가격 미상은 제외합니다.
- 필수 조건을 모두 통과한 후보는 같은 조건 일치 점수를 갖습니다. 따라서 현재 순위는 사실상 가격 오름차순입니다.
- lifestyles/priorities/usageTypes는 현재 필터·점수에 반영되지 않습니다. 사용자 노트까지 활용한 개인화 랭킹으로 과장하지 않습니다.
- LLM은 후보를 선정하지 않고 규칙 결과를 설명합니다.

## 백업 비교

`E:\Project\mobility_choice_local_backup`의 main.py/advisor_service.py/requirements.txt를 현재와 비교했습니다. 별도 `/api/recommendations` 비동기 호출 실험이 있지만 현재 브랜치에는 동기 preview와 SSE가 있습니다. 백업으로 현재를 덮어쓰지 않았으며 파일은 로컬에 유지했습니다. 백업의 최소 의존성 환경은 현재 LangChain 연동을 완전히 재현하지 못합니다.

## 다음 작업

1. MongoDB·Ollama를 포함한 로그인 → 조건 → 추천 → SSE 설명을 재검증.
2. 필수 조건과 선호 점수의 제품 의미를 정하고 라이프스타일·우선순위 랭킹을 별도 설계.
3. `advisor_service.py`의 스트리밍 경로가 만든 `advice_vehicles` 대신 원본 recommendations를 JSON에 넣는 불일치 정리.
4. SSE의 upstream 인증/HTTP 오류 구분, 중단·재시도와 프롬프트 근거 일치 검증.
