from django.shortcuts import render, redirect, get_object_or_404
from .models import BCISession, BCIData
from .forms import BCIDataForm
from .analysis import generate_session_plots
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.core.cache import cache
from django.views.decorators.cache import cache_page


@cache_page(60 * 15) 
def session_list(request):
    sessions = BCISession.objects.all()
    return render(request, 'bci_data/session_list.html', {'sessions': sessions})

def session_detail(request, session_id):
    cache_key = f'session_detail_{session_id}'
    session_data = cache.get(cache_key)
    
    if not session_data:
        session = BCISession.objects.prefetch_related(
            Prefetch('data_points', queryset=BCIData.objects.order_by('-timestamp'))
        ).get(id=session_id)
        
        data_points = list(session.data_points.all()[:50])
        
        session_data = {
            'session': session,
            'data_points': data_points,
        }
        cache.set(cache_key, session_data, 60 * 5)  # 5분 동안 캐시
    
    return render(request, 'bci_data/session_detail.html', session_data)

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
            data_point = form.save(commit=False)
            data_point.session = session
            data_point.save()
            return redirect('session_detail', session_id=session.id)
    else:
        form = BCIDataForm()
    return render(request, 'bci_data/add_data_point.html', {'form': form, 'session': session})

def add_data_point(request, session_id):
    if request.method == 'POST':
        form = BCIDataForm(request.POST)
        if form.is_valid():
            try:
                data_point = form.save(commit=False)
                data_point.session_id = session_id
                data_point.full_clean()  # 추가 유효성 검사
                data_point.save()
                # 웹소켓을 통해 데이터 전송 (기존 코드)
                return redirect('session_detail', session_id=session_id)
            except ValidationError as e:
                form.add_error(None, e.message_dict)
    else:
        form = BCIDataForm()
    
    return render(request, 'bci_data/add_data_point.html', {'form': form, 'session_id': session_id})

def session_detail(request, session_id):
    session = BCISession.objects.get(id=session_id)
    data_points = session.data_points.order_by('-timestamp')
    paginator = Paginator(data_points, 50)  # 페이지당 50개 데이터 포인트
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'session': session,
        'page_obj': page_obj,
    }
    return render(request, 'bci_data/session_detail.html', context)