# Mobility Choice 검증 기록

기준일: 2026-10-27 (KST).

| 확인 | 결과 | 범위 |
|---|---|---|
| `python -m unittest discover -s tests -v` (`ai-backend`) | 8개 통과 | 예산 단위·경계, 필수 조건, 모든 기능 AND, 차종 OR, 가격 정렬, 입력 불변성 |
| `npm run build` (`frontend`) | 통과 | Next.js production build |
| Python 문법 검사 | 통과 | Git 후보 Python 전체 AST 파싱 |
| 백업 비교 | 완료 | main.py/advisor_service.py/requirements.txt 차이 확인, 로컬 백업 유지 |
| 비밀정보·대용량 검사 | 통과 | 지정 토큰 패턴 미검출, .env·캐시 제외 |

미검증: 실제 MongoDB 인증·seed·차량 응답, Ollama 모델 구동·설명 근거·SSE 전체 흐름, 실사용 로그인→조건→추천 통합. 이번 통과 결과는 외부 서버 없는 추천 계약과 프론트 빌드에 한정합니다.
