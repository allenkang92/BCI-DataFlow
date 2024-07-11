from django.shortcuts import render, redirect, get_object_or_404
from .models import BCISession, BCIData
from .forms import BCIDataForm, BCISessionForm
from .analysis import generate_session_plots
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.db.models import Count, Avg, Model
from django.utils import timezone
import json
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Model):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
    
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

@cache_page(60 * 15)
def session_list(request):
    sessions = BCISession.objects.all()
    return render(request, 'bci_data/session_list.html', {'sessions': sessions})


import logging
logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect, get_object_or_404
from .models import BCISession, BCIData
from .forms import BCIDataForm, BCISessionForm
from .analysis import generate_session_plots
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.db.models import Count, Avg, Model
from django.utils import timezone
import json
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Model):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
    
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

@cache_page(60 * 15)
def session_list(request):
    sessions = BCISession.objects.all()
    return render(request, 'bci_data/session_list.html', {'sessions': sessions})


import logging
logger = logging.getLogger(__name__)

def session_detail(request, session_id):
    cache_key = f'session_detail_{session_id}'
    cache.delete(cache_key)  # 기존 캐시 삭제
    
    session = BCISession.objects.prefetch_related(
        Prefetch('data_points', queryset=BCIData.objects.order_by('-timestamp'))
    ).get(id=session_id)
    
    data_points = list(session.data_points.all()[:50])
    timeseries_plot, heatmap_plot = generate_session_plots(session)
    
    # 실시간 차트를 위한 초기 데이터
    initial_data = list(session.data_points.order_by('-timestamp')[:100].values(
        'timestamp', 'channel_1', 'channel_2', 'channel_3', 'channel_4'
    ))
    initial_data.reverse()  # 시간순으로 정렬
    
    for data in initial_data:
        data['timestamp'] = timezone.localtime(data['timestamp']).isoformat()

    logger.debug(f"Initial data first item: {initial_data[0] if initial_data else 'No data'}")
    
    timeseries_plot, heatmap_plot = generate_session_plots(session)
    
    context = {
        'session': session,
        'data_points': data_points,
        'timeseries_plot': json.dumps(timeseries_plot, cls=DjangoJSONEncoder),
        'heatmap_plot': json.dumps(heatmap_plot, cls=DjangoJSONEncoder),
        'initial_chart_data': json.dumps(initial_data, cls=DjangoJSONEncoder)
    }
    
    paginator = Paginator(data_points, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context['page_obj'] = page_obj
    
    return render(request, 'bci_data/session_detail.html', context)

def dashboard(request):
    # 기본 통계 계산
    total_sessions = BCISession.objects.count()
    total_data_points = BCIData.objects.count()
    recent_sessions = BCISession.objects.filter(date_recorded__gte=timezone.now() - timezone.timedelta(days=7)).count()
    avg_data_points_per_session = BCISession.objects.annotate(data_count=Count('data_points')).aggregate(Avg('data_count'))['data_count__avg']

    context = {
        'total_sessions': total_sessions,
        'total_data_points': total_data_points,
        'recent_sessions': recent_sessions,
        'avg_data_points_per_session': avg_data_points_per_session,
    }
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

    context.update({
        'daily_sessions': json.dumps(list(daily_sessions)),
        'channel_activity': json.dumps(channel_activity)
    })
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

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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

def dashboard(request):
    # 기본 통계 계산
    total_sessions = BCISession.objects.count()
    total_data_points = BCIData.objects.count()
    recent_sessions = BCISession.objects.filter(date_recorded__gte=timezone.now() - timezone.timedelta(days=7)).count()
    avg_data_points_per_session = BCISession.objects.annotate(data_count=Count('data_points')).aggregate(Avg('data_count'))['data_count__avg']

    context = {
        'total_sessions': total_sessions,
        'total_data_points': total_data_points,
        'recent_sessions': recent_sessions,
        'avg_data_points_per_session': avg_data_points_per_session,
    }
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

    context.update({
        'daily_sessions': json.dumps(list(daily_sessions)),
        'channel_activity': json.dumps(channel_activity)
    })
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

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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