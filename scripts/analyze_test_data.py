import os
import sys
import django
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Django 설정 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bci_platform.settings')
django.setup()

from bci_platform.models import Session, DataPoint

def analyze_session_data(session_id=None):
    """세션 데이터 분석"""
    print("데이터 분석 시작...")

    # 세션 선택
    if session_id:
        sessions = Session.objects.filter(id=session_id)
    else:
        sessions = Session.objects.all()

    if not sessions.exists():
        print("분석할 세션이 없습니다.")
        return

    for session in sessions:
        print(f"\n=== 세션 분석: {session.name} ===")
        
        # 데이터 포인트 가져오기
        data_points = DataPoint.objects.filter(session=session)
        
        if not data_points.exists():
            print("데이터 포인트가 없습니다.")
            continue

        # 데이터 추출
        channel_data_list = []
        timestamps = []
        quality_scores = []

        for dp in data_points:
            channel_data_list.append(dp.channel_data)
            timestamps.append(dp.timestamp)
            quality_scores.append(dp.quality_score)

        # DataFrame 생성
        df = pd.DataFrame(channel_data_list)
        df['timestamp'] = timestamps
        df['quality_score'] = quality_scores

        # 기본 통계
        print("\n기본 통계:")
        print(df.describe())

        # 품질 점수 분포
        plt.figure(figsize=(10, 6))
        plt.hist(quality_scores, bins=20)
        plt.title(f'Quality Score Distribution - {session.name}')
        plt.xlabel('Quality Score')
        plt.ylabel('Frequency')
        plt.savefig(f'quality_dist_session_{session.id}.png')
        plt.close()

        # 채널 간 상관관계
        plt.figure(figsize=(12, 8))
        channel_cols = [col for col in df.columns if 'channel' in col]
        correlation_matrix = df[channel_cols].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
        plt.title(f'Channel Correlation - {session.name}')
        plt.savefig(f'correlation_session_{session.id}.png')
        plt.close()

        # 시계열 데이터 플롯
        plt.figure(figsize=(15, 8))
        for channel in channel_cols[:3]:  # 처음 3개 채널만 표시
            plt.plot(df['timestamp'], df[channel], label=channel)
        plt.title(f'Time Series Data (First 3 Channels) - {session.name}')
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'timeseries_session_{session.id}.png')
        plt.close()

        print(f"\n분석 결과가 이미지 파일로 저장되었습니다:")
        print(f"- quality_dist_session_{session.id}.png")
        print(f"- correlation_session_{session.id}.png")
        print(f"- timeseries_session_{session.id}.png")

if __name__ == '__main__':
    session_id = sys.argv[1] if len(sys.argv) > 1 else None
    analyze_session_data(session_id)
