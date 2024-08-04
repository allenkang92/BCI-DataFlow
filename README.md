# BCI-DataFlow: 통합 BCI를 위한 데이터 처리 플랫폼

## 프로젝트 개요

BCI-DataFlow는 뇌-컴퓨터 인터페이스(BCI) 연구를 위한 데이터 처리 및 분석 플랫폼입니다. BCI를 위한 EEZ 데이터의 처리, 분석 및 시각화를 위한 통합 솔루션을 제공합니다.

## 주요 기능

1. **데이터 관리**
   * BCI 세션 생성 및 관리
   * 실시간 데이터 포인트 추가
   * 데이터베이스 기반 데이터 저장 (PostgreSQL 사용)
   * 세션 및 데이터 포인트 삭제 기능 (CRUD 완성)

2. **데이터 시각화**
   * 실시간 데이터 스트리밍 차트 (Chart.js 사용)
   * 시계열 데이터 플롯
   * 채널 간 상관관계 히트맵

3. **웹 인터페이스**
   * 세션 목록 및 상세 정보 표시
   * 데이터 포인트 추가를 위한 폼
   * 검색 및 필터링 기능

4. **실시간 데이터 처리**
   * WebSocket을 이용한 실시간 데이터 전송
   * 실시간 차트 업데이트

5. **데이터 가져오기/내보내기**
   * CSV 형식으로 세션 데이터 내보내기
   * CSV 파일에서 데이터 가져오기

6. **성능 최적화**
   * 데이터베이스 쿼리 최적화 (Prefetch 사용)
   * 캐싱 시스템 구현

7. **대시보드**
   * 전체 세션 및 데이터 포인트 통계
   * 최근 세션 활동 표시
   * 채널별 평균 활성도 시각화

## 기술 스택

* Backend: Django
* Database: PostgreSQL
* Frontend: HTML, CSS, JavaScript, Bootstrap
* 실시간 통신: Django Channels (WebSocket)
* 차트 라이브러리: Chart.js, Matplotlib
* 캐싱: Django's caching framework

## 설치 및 실행 방법


1. 가상 환경 생성 및 활성화:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. 의존성 설치:
   ```
   pip install -r requirements.txt
   ```

3. PostgreSQL 데이터베이스 생성:
   ```
   createdb bci_dataflow
   ```

4. 환경 변수 설정:
   `.env` 파일을 생성하고 다음 내용을 추가하세요:
   ```
   DEBUG=True
   SECRET_KEY=your_secret_key
   DATABASE_URL=postgresql://username:password@localhost/bci_dataflow
   ```

5. 데이터베이스 마이그레이션:
   ```
   python manage.py migrate
   ```

6. 개발 서버 실행:
   ```
   python manage.py runserver
   ```

8. 브라우저에서 `http://localhost:8000`으로 접속하여 애플리케이션 사용

