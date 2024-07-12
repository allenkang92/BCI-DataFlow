from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Prefetch, Count, Avg, Q
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils import timezone
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import csv
import logging
from django.contrib import messages
from django.urls import reverse
from .models import BCISession, BCIData
from .forms import BCIDataForm, BCISessionForm, DataImportForm
from .analysis import generate_session_plots

logger = logging.getLogger(__name__)

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Model):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

@cache_page(60 * 15)
def session_list(request):
    sessions = BCISession.objects.all()
    return render(request, 'bci_data/session_list.html', {'sessions': sessions})

def delete_session(request, session_id):
    session = get_object_or_404(BCISession, id=session_id)
    if request.method == 'POST':
        session.delete()
        messages.success(request, f"Session {session.session_name} has been deleted.")
        return redirect('session_list')
    return render(request, 'bci_data/delete_session.html', {'session': session})

def delete_data_point(request, session_id, data_point_id):
    data_point = get_object_or_404(BCIData, id=data_point_id, session_id=session_id)
    if request.method == 'POST':
        data_point.delete()
        messages.success(request, "Data point has been deleted.")
        return redirect('session_detail', session_id=session_id)
    return render(request, 'bci_data/delete_data_point.html', {'data_point': data_point})

def session_detail(request, session_id):
    cache_key = f'session_detail_{session_id}'
    cache.delete(cache_key)  # 기존 캐시 삭제
    
    session = BCISession.objects.prefetch_related(
        Prefetch('data_points', queryset=BCIData.objects.order_by('-timestamp'))
    ).get(id=session_id)
    
    # 검색 및 필터링
    search_query = request.GET.get('search', '')
    min_value = request.GET.get('min_value', '')
    max_value = request.GET.get('max_value', '')
    
    data_points = session.data_points.all().order_by('-timestamp')
    
    if search_query:
        data_points = data_points.filter(
            Q(timestamp__icontains=search_query) |
            Q(channel_1__icontains=search_query) |
            Q(channel_2__icontains=search_query) |
            Q(channel_3__icontains=search_query) |
            Q(channel_4__icontains=search_query)
        )
    
    if min_value:
        data_points = data_points.filter(
            Q(channel_1__gte=min_value) |
            Q(channel_2__gte=min_value) |
            Q(channel_3__gte=min_value) |
            Q(channel_4__gte=min_value)
        )
    
    if max_value:
        data_points = data_points.filter(
            Q(channel_1__lte=max_value) |
            Q(channel_2__lte=max_value) |
            Q(channel_3__lte=max_value) |
            Q(channel_4__lte=max_value)
        )
    
    timeseries_plot, heatmap_plot = generate_session_plots(session)
    
    # 실시간 차트를 위한 초기 데이터
    initial_data = list(data_points[:100].values(
        'timestamp', 'channel_1', 'channel_2', 'channel_3', 'channel_4'
    ))
    initial_data.reverse()  # 시간순으로 정렬
    
    for data in initial_data:
        data['timestamp'] = timezone.localtime(data['timestamp']).isoformat()

    logger.debug(f"Initial data first item: {initial_data[0] if initial_data else 'No data'}")
    
    # 페이지네이션
    paginator = Paginator(data_points, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'session': session,
        'page_obj': page_obj,
        'timeseries_plot': timeseries_plot,
        'heatmap_plot': heatmap_plot,
        'initial_chart_data': json.dumps(initial_data, cls=CustomJSONEncoder),
        'search_query': search_query,
        'min_value': min_value,
        'max_value': max_value,
    }
    
    return render(request, 'bci_data/session_detail.html', context)

def dashboard(request):
    # 기본 통계 계산
    total_sessions = BCISession.objects.count()
    total_data_points = BCIData.objects.count()
    recent_sessions = BCISession.objects.filter(date_recorded__gte=timezone.now() - timezone.timedelta(days=7)).count()
    avg_data_points_per_session = BCISession.objects.annotate(data_count=Count('data_points')).aggregate(Avg('data_count'))['data_count__avg']

    # 최근 7일간의 일별 세션 수 계산
    last_week = timezone.now().date() - timezone.timedelta(days=6)
    daily_sessions = BCISession.objects.filter(date_recorded__gte=last_week)\
        .annotate(date=TruncDate('date_recorded'))\
        .values('date')\
        .annotate(count=Count('id'))\
        .order_by('date')
    
    # 채널별 평균 활성도 계산
    channel_activity = BCIData.objects.aggregate(
        channel_1_avg=Avg('channel_1'),
        channel_2_avg=Avg('channel_2'),
        channel_3_avg=Avg('channel_3'),
        channel_4_avg=Avg('channel_4')
    )

    context = {
        'total_sessions': total_sessions,
        'total_data_points': total_data_points,
        'recent_sessions': recent_sessions,
        'avg_data_points_per_session': avg_data_points_per_session,
        'daily_sessions': json.dumps(list(daily_sessions), cls=CustomJSONEncoder),
        'channel_activity': json.dumps(channel_activity, cls=CustomJSONEncoder)
    }
    return render(request, 'bci_data/dashboard.html', context)

def create_session(request):
    if request.method == 'POST':
        form = BCISessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('session_list')
    else:
        form = BCISessionForm()
    return render(request, 'bci_data/create_session.html', {'form': form})

def add_data_point(request, session_id):
    session = get_object_or_404(BCISession, id=session_id)
    if request.method == 'POST':
        form = BCIDataForm(request.POST)
        if form.is_valid():
            try:
                data_point = form.save(commit=False)
                data_point.session = session
                data_point.full_clean()  # 추가 유효성 검사
                data_point.save()
                
                # 웹소켓을 통해 데이터 전송
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"bci_session_{session_id}",
                    {
                        "type": "bci_message",
                        "message": {
                            "timestamp": data_point.timestamp.isoformat(),
                            "channel_1": data_point.channel_1,
                            "channel_2": data_point.channel_2,
                            "channel_3": data_point.channel_3,
                            "channel_4": data_point.channel_4,
                        }
                    }
                )
                
                cache.delete(f'session_detail_{session_id}')  # 캐시 삭제
                return redirect('session_detail', session_id=session.id)
            except ValidationError as e:
                form.add_error(None, e.message_dict)
    else:
        form = BCIDataForm()
    
    return render(request, 'bci_data/add_data_point.html', {'form': form, 'session': session})

def import_session_data(request, session_id):
    if request.method == 'POST':
        form = DataImportForm(request.POST, request.FILES)
        if form.is_valid():
            session = BCISession.objects.get(id=session_id)
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            for row in reader:
                BCIData.objects.create(
                    session=session,
                    timestamp=row['Timestamp'],
                    channel_1=float(row['Channel 1']),
                    channel_2=float(row['Channel 2']),
                    channel_3=float(row['Channel 3']),
                    channel_4=float(row['Channel 4'])
                )
            return redirect('session_detail', session_id=session_id)
    else:
        form = DataImportForm()
    return render(request, 'bci_data/import_data.html', {'form': form})

def export_session_data(request, session_id):
    session = BCISession.objects.get(id=session_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="session_{session_id}_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Timestamp', 'Channel 1', 'Channel 2', 'Channel 3', 'Channel 4'])

    data_points = session.data_points.all().order_by('timestamp')
    for point in data_points:
        writer.writerow([point.timestamp, point.channel_1, point.channel_2, point.channel_3, point.channel_4])

    return response