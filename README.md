# BCI-DataFlow: 통합 BCI 데이터 처리 플랫폼

## 프로젝트 개요

BCI-DataFlow는 뇌-컴퓨터 인터페이스(BCI) 연구를 위한 종합적인 데이터 처리 및 분석 플랫폼입니다. 이 플랫폼은 BCI 데이터의 수집, 저장, 처리, 분석 및 시각화를 위한 통합 솔루션을 제공합니다.

## 주요 기능

1. **데이터 관리**
   - BCI 세션 생성 및 관리
   - 실시간 데이터 포인트 추가
   - 데이터베이스 기반 데이터 저장 (PostgreSQL 사용)
   - 세션 및 데이터 포인트 삭제 기능 (CRUD 완성)

2. **데이터 시각화**
   - 실시간 데이터 스트리밍 차트 (Chart.js 사용)
   - 시계열 데이터 플롯
   - 채널 간 상관관계 히트맵

3. **웹 인터페이스**
   - 세션 목록 및 상세 정보 표시
   - 데이터 포인트 추가를 위한 폼
   - 검색 및 필터링 기능

4. **실시간 데이터 처리**
   - WebSocket을 이용한 실시간 데이터 전송
   - 실시간 차트 업데이트

5. **데이터 가져오기/내보내기**
   - CSV 형식으로 세션 데이터 내보내기
   - CSV 파일에서 데이터 가져오기

6. **성능 최적화**
   - 데이터베이스 쿼리 최적화 (Prefetch 사용)
   - 캐싱 시스템 구현

7. **대시보드**
   - 전체 세션 및 데이터 포인트 통계
   - 최근 세션 활동 표시
   - 채널별 평균 활성도 시각화

## 기술 스택

- Backend: Django
- Database: PostgreSQL
- Frontend: HTML, CSS, JavaScript, Bootstrap
- 실시간 통신: Django Channels (WebSocket)
- 차트 라이브러리: Chart.js, Matplotlib
- 캐싱: Django's caching framework

## BCI 연구에서의 역할

1. **데이터 수집 및 저장**: 연구자들이 BCI 실험 데이터를 효율적으로 수집하고 중앙 집중식으로 저장할 수 있게 합니다.

2. **실시간 모니터링**: 실험 중 뇌파 데이터를 실시간으로 시각화하여 즉각적인 피드백을 제공합니다.

3. **데이터 분석 지원**: 기본적인 시계열 분석과 채널 간 상관관계 분석을 제공하여 초기 데이터 해석을 돕습니다.

4. **협업 촉진**: 중앙화된 플랫폼을 통해 연구팀 간의 데이터 공유와 협업을 용이하게 합니다.

5. **데이터 관리 유연성**: 데이터 가져오기/내보내기 기능을 통해 다양한 소스의 데이터를 통합하고 외부 도구와의 호환성을 제공합니다.

6. **확장성**: 다양한 BCI 장치와 실험 프로토콜에 적용할 수 있는 유연한 구조를 제공합니다.

## 최근 업데이트

- 세션 및 데이터 포인트 삭제 기능 추가 (CRUD 완성)
- 데이터 검색 및 필터링 기능 구현
- CSV 형식의 데이터 가져오기/내보내기 기능 추가
- 사용자 인터페이스 개선 (부트스트랩 적용)
- 시스템 메시지 표시 기능 추가

## 향후 계획

1. **데이터 분석 기능 강화**
   - 주파수 분석, 상관 분석 등 고급 통계 도구 추가
   - 머신러닝 모델 통합 (신호 분류, 패턴 인식)
   - 사용자 정의 분석 스크립트 실행 기능

2. **데이터 시각화 개선**
   - 인터랙티브한 차트 및 그래프 기능 (줌, 구간 선택 등)
   - 3D 두피 맵핑 시각화

3. **사용자 관리 시스템**
   - 사용자 인증 및 권한 관리
   - 개인화된 대시보드

4. **API 개발**
   - RESTful API 구현으로 외부 애플리케이션과의 연동 지원

5. **성능 및 확장성 개선**
   - 대규모 데이터셋 처리를 위한 최적화
   - 분산 처리 시스템 고려

## 설치 및 실행 방법

(설치 및 실행 방법에 대한 상세 지침을 여기에 추가하세요)

## 기여 방법

(프로젝트에 기여하는 방법에 대한 지침을 여기에 추가하세요)

## 라이선스

(프로젝트의 라이선스 정보를 여기에 추가하세요)

## 연락처

(프로젝트 책임자 또는 팀의 연락처 정보를 여기에 추가하세요)