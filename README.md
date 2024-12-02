# BCI-DataFlow: BCI를 위한 데이터 처리 플랫폼

## 프로젝트 개요

BCI-DataFlow는 뇌-컴퓨터 인터페이스(BCI) 연구를 위한 데이터 처리 및 분석 플랫폼입니다. 실시간 EEG 데이터의 수집, 처리, 분석 및 시각화를 위한 통합 솔루션을 제공합니다.

## 시스템 요구사항

- Docker 및 Docker Compose
- PostgreSQL 데이터베이스
- Python 3.9 이상
- Redis (WebSocket 지원용)

## 주요 기능

1. **데이터 수집 및 관리**
   * BCI 세션 생성 및 관리
   * 실시간 EEG 데이터 스트리밍 수집
   * PostgreSQL 기반의 안정적인 데이터 저장
   * REST API를 통한 데이터 CRUD 작업

2. **실시간 처리 및 분석**
   * WebSocket 기반 실시간 데이터 스트리밍
   * 실시간 신호 처리 및 필터링
   * 데이터 정규화 및 전처리
   * 과학적 분석을 위한 통계 처리

3. **데이터 시각화**
   * 실시간 EEG 데이터 모니터링
   * 다채널 시계열 데이터 시각화
   * 주파수 영역 분석 결과 표시
   * 채널 간 상관관계 분석 및 시각화

4. **시스템 관리**
   * 사용자 인증 및 권한 관리
   * 세션 기록 및 로그 관리
   * 시스템 상태 모니터링
   * 데이터 백업 및 복구

## 설치 및 실행

1. 저장소 클론:
   ```bash
   git clone https://github.com/yourusername/BCI-DataFlow.git
   cd BCI-DataFlow
   ```

2. 환경 설정:
   * `.env.template`를 `.env`로 복사하고 필요한 설정 입력
   * 데이터베이스 접속 정보 설정
   * Django 보안 설정 구성

3. Docker 실행:
   ```bash
   docker-compose up --build
   ```

4. 데이터베이스 마이그레이션:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

## 프로젝트 구조

```
BCI-DataFlow/
├── bci_platform/          # 메인 Django 프로젝트
│   ├── bci_data/         # 데이터 처리 앱
│   ├── config/           # 프로젝트 설정
│   └── tests/            # 테스트 코드
├── scripts/              # 유틸리티 스크립트
├── docker-compose.yml    # Docker 구성
└── requirements.txt      # Python 의존성
```

## 개발 환경 설정

1. 가상환경 생성 및 활성화:
   ```bash
   python -m venv bci_env
   source bci_env/bin/activate  # Linux/Mac
   ```

2. 의존성 설치:
   ```bash
   pip install -r requirements.txt
   ```

## 문제 해결

문제 해결 가이드는 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)를 참조하세요.

