from django.urls import path
from . import views


app_name = 'taskmaster'
urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('master/', views.MasterView.as_view(), name="master"),
    path('master/create/', views.MasterCreateView.as_view(), name="master_create"),
    path('master/<int:pk>/detail', views.MasterDetailView.as_view(), name="master_detail"),
    path('master/<int:pk>/update/', views.MasterUpdateView.as_view(), name="master_update"),
    path('master/<int:pk>/delete/', views.MasterDeleteView.as_view(), name="master_delete"),
    
    path('task/', views.InboxView.as_view(), name="inbox"),
    path('task/create/', views.TaskCreateView.as_view(), name="task_create"),
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name="task_update"),
    path('task/<int:pk>/detail/', views.TaskDetailView.as_view(), name="task_detail"),
]