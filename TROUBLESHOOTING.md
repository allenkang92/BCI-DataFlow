# BCI-DataFlow 트러블슈팅 가이드

## 일반적인 문제 해결

### 1. 설치 관련 문제

#### PostgreSQL 연결 오류
```
django.db.utils.OperationalError: could not connect to server
```

**해결방법:**
1. PostgreSQL 서비스가 실행 중인지 확인
2. 데이터베이스 접속 정보가 올바른지 확인
3. `.env` 파일의 DATABASE_URL 설정 확인

### 2. 실행 시 발생하는 문제

#### WebSocket 연결 오류
```
WebSocket connection failed
```

**해결방법:**
1. Redis 서버 실행 상태 확인
2. CHANNEL_LAYERS 설정 확인
3. 방화벽 설정 확인

### 3. 데이터 관련 문제

#### 데이터 포인트 저장 실패
```
IntegrityError: null value in column "session_id" violates not-null constraint
```

**해결방법:**
1. 세션이 올바르게 생성되었는지 확인
2. 데이터 포인트 생성 시 필수 필드가 모두 포함되었는지 확인

### 4. 성능 관련 문제

#### 느린 쿼리 응답
**해결방법:**
1. 데이터베이스 인덱스 확인
2. 쿼리 최적화
3. 캐싱 설정 확인

## Docker 관련 문제

### 컨테이너 실행 실패
**해결방법:**
1. Docker 서비스 상태 확인
2. 포트 충돌 확인
3. 환경 변수 설정 확인

## 로깅 및 디버깅

### 로그 확인 방법
1. Docker 로그:
```bash
docker-compose logs -f web
```

2. 애플리케이션 로그:
```bash
tail -f logs/debug.log
```

### 디버그 모드 활성화
1. `.env` 파일에서 `DEBUG=True` 설정
2. 로그 레벨 조정:
```python
LOGGING = {
    'level': 'DEBUG',
    ...
}
```

## 지원 및 도움말

문제 해결이 어려운 경우:
1. GitHub Issues 페이지 확인
2. 로그 파일 수집
3. 환경 설정 정보 준비
4. 이슈 리포트 작성
