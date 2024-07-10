import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import base64

def generate_session_plots(session):
    data_points = session.data_points.all().order_by('timestamp')
    df = pd.DataFrame(list(data_points.values()))
    
    if df.empty:
        return None, None

    # 시계열 플롯
    plt.figure(figsize=(10, 6))
    for channel in ['channel_1', 'channel_2', 'channel_3', 'channel_4']:
        plt.plot(df['timestamp'], df[channel], label=channel)
    plt.legend()
    plt.title('Channel Data Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Channel Value')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    timeseries_plot = get_plot_as_base64(plt)
    plt.close()

    # 채널 상관관계 히트맵
    plt.figure(figsize=(8, 6))
    correlation = df[['channel_1', 'channel_2', 'channel_3', 'channel_4']].corr()
    plt.imshow(correlation, cmap='coolwarm', aspect='auto')
    plt.colorbar()
    plt.xticks(range(4), ['Ch 1', 'Ch 2', 'Ch 3', 'Ch 4'])
    plt.yticks(range(4), ['Ch 1', 'Ch 2', 'Ch 3', 'Ch 4'])
    plt.title('Channel Correlation Heatmap')
    for i in range(4):
        for j in range(4):
            plt.text(j, i, f'{correlation.iloc[i, j]:.2f}', ha='center', va='center')
    plt.tight_layout()
    
    heatmap_plot = get_plot_as_base64(plt)
    plt.close()
    
    return timeseries_plot, heatmap_plot

def get_plot_as_base64(plt):
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    # plt.close()
    return image_base64