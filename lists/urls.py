from django.urls import path

from lists import views

app_name = 'lists'
urlpatterns = [
    path('', views.index, name='alllist'),
    path('tasklist/delete/<int:tasklist_id>/', views.task_delete, name='delete'),
    path('tasklist/update/<int:id>/', views.task_update, name='update'),
    path('tasklist/create', views.create_task, name='new_tasklist'),
    path('todolist/status/<int:id>/', views.status_update, name='status'),
    # path('todo/add/<int:todolist_id>/', views.add_todo, name='add_todo'),
    path('profile/', views.profile, name='profile'),
]
