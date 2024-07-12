from django.urls import path
from . import views

urlpatterns = [
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/<int:session_id>/', views.session_detail, name='session_detail'),
    path('sessions/create/', views.create_session, name='create_session'),
    path('sessions/<int:session_id>/add_data/', views.add_data_point, name='add_data_point'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sessions/<int:session_id>/export/', views.export_session_data, name='export_session_data'),
    path('sessions/<int:session_id>/import/', views.import_session_data, name='import_session_data'),
]