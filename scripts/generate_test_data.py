import os
import sys
import django
import random
import numpy as np
from datetime import datetime, timedelta
import json

# Django 설정 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bci_platform.settings')
django.setup()

from django.contrib.auth.models import User
from bci_platform.models import Session, DataPoint

def generate_channel_data(num_channels=8, base_frequency=10):
    """실제 EEG와 유사한 시계열 데이터 생성"""
    time_points = np.linspace(0, 1, 256)  # 1초 동안의 데이터
    channel_data = {}
    
    for i in range(num_channels):
        # 기본 알파파 (8-13 Hz) 시뮬레이션
        alpha = np.sin(2 * np.pi * base_frequency * time_points)
        
        # 베타파 (13-30 Hz) 노이즈 추가
        beta = 0.5 * np.sin(2 * np.pi * 20 * time_points)
        
        # 랜덤 노이즈 추가
        noise = 0.1 * np.random.randn(len(time_points))
        
        # 채널 데이터 조합
        signal = alpha + beta + noise
        
        # 특정 시점의 값만 선택
        value = float(signal[random.randint(0, len(signal)-1)])
        channel_data[f'channel_{i+1}'] = round(value, 3)
    
    return channel_data

def create_test_data(num_sessions=5, points_per_session=100):
    """테스트 데이터 생성"""
    print("테스트 데이터 생성 시작...")
    
    # 테스트 사용자 생성
    try:
        user = User.objects.get(username='test_user')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='test_user',
            password='test1234',
            email='test@example.com'
        )
        print("테스트 사용자 생성됨")

    # 세션 생성
    for i in range(num_sessions):
        session_name = f"Test Session {i+1}"
        session = Session.objects.create(
            name=session_name,
            description=f"자동 생성된 테스트 세션 #{i+1}",
            created_by=user,
            status='active' if i % 2 == 0 else 'completed'
        )
        print(f"세션 생성됨: {session_name}")

        # 데이터 포인트 생성
        base_time = datetime.now() - timedelta(hours=i)
        for j in range(points_per_session):
            timestamp = base_time + timedelta(seconds=j)
            channel_data = generate_channel_data()
            
            DataPoint.objects.create(
                session=session,
                timestamp=timestamp,
                channel_data=channel_data,
                quality_score=random.uniform(0.7, 1.0)
            )
        
        print(f"세션 {i+1}에 대해 {points_per_session}개의 데이터 포인트 생성됨")

    print("\n테스트 데이터 생성 완료!")
    print(f"총 {num_sessions}개의 세션과 {num_sessions * points_per_session}개의 데이터 포인트가 생성되었습니다.")
    print("\n테스트 계정 정보:")
    print("사용자명: test_user")
    print("비밀번호: test1234")

if __name__ == '__main__':
    # 기본값: 5개 세션, 각 100개의 데이터 포인트
    num_sessions = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    points_per_session = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    
    create_test_data(num_sessions, points_per_session)
