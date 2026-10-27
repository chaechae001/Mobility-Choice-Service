# Mobility Choice 작업 안내

- 먼저 docs/HANDOFF.md, PROJECT_STATUS.md, VERIFICATION.md를 읽습니다.
- frontend는 Next.js, backend는 Express/MongoDB/JWT, ai-backend는 FastAPI/Ollama입니다.
- 현재 추천은 필수 필터 통과 후 가격 정렬입니다. 라이프스타일·우선순위 랭킹이 완성되었다고 표현하지 않습니다.
- 추천 계약 변경 시 `ai-backend/tests/` 회귀 테스트를 함께 확인합니다.
- .env·JWT·MongoDB 인증정보와 로컬 모델을 Git에 넣지 않습니다.
- 실제 DB/모델 검증을 수행했는지 기록하고 미검증을 성공으로 표시하지 않습니다.
