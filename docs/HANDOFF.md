# Mobility Choice 인수인계

## 작업 위치

- 로컬: `E:\Project\mobility_choice_service`.
- 원격: https://github.com/chaechae001/Mobility-Choice-Service
- 이번 브랜치: `chore/portfolio-handoff-20261027`, 기존 `feat/ai-advisor`에서 분기.

## 실행 순서

1. MongoDB를 준비합니다. `backend/.env.example`을 복사하고 MONGODB_URI, JWT_SECRET, PORT를 설정합니다. 실제 키는 커밋하지 않습니다.
2. `backend`에서 `npm ci`, 필요한 경우 `npm run seed:vehicles`, `npm run dev` (기본 4000).
3. Python 3.12+ 가상환경을 만들고 `ai-backend/requirements.txt`를 설치합니다.
4. Ollama에 `exaone3.5:2.4b` 모델을 준비하고 로컬 API를 실행합니다. 모델 다운로드와 실제 AI 호출은 이번 정리에서 수행하지 않았습니다.
5. `ai-backend`에서 `python -m uvicorn main:app --host 127.0.0.1 --port 8000`.
6. `frontend`에서 `npm ci`, `npm run dev` (3000).
7. 회원가입/로그인 후 JWT를 유지한 채 차량 조건과 추천을 확인합니다.

## 독립 검증

```powershell
cd ai-backend
python -m unittest discover -s tests -v
```

외부 서버 없이 예산 단위·필터·기능 AND·복수 차종 OR·정렬·원본 불변성을 검사합니다. 새 기능 테스트나 SSE 통합 검증을 대체하지 않습니다.

## 후속 범위

[PROJECT_STATUS.md](PROJECT_STATUS.md)의 계약을 먼저 확인하고 `main`으로 병합하기 전 API 체인 전체를 검증합니다. 별도 백업은 비교 자료이며 실행 기준은 현재 저장소입니다. 테스트 결과와 외부 서비스 미검증 항목은 [VERIFICATION.md](VERIFICATION.md)에 있습니다.
