from django.shortcuts import render, redirect
from .models import BCISession, BCIData
from .forms import BCISessionForm, BCIDataForm
from .analysis import generate_session_plots

def session_list(request):
    sessions = BCISession.objects.all()
    return render(request, 'bci_data/session_list.html', {'sessions': sessions})

def session_detail(request, session_id):
    session = BCISession.objects.get(id=session_id)
    data_points = session.data_points.all().order_by('timestamp')
    timeseries_plot, heatmap_plot = generate_session_plots(session)
    
    context = {
        'session': session,
        'data_points': data_points,
        'timeseries_plot': timeseries_plot,
        'heatmap_plot': heatmap_plot,
    }
    return render(request, 'bci_data/session_detail.html', context)

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
    session = BCISession.objects.get(id=session_id)
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