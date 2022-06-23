from django.urls import path, include
from . import views
app_name = 'logs'
urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('topics/<str:public>/', views.topics.as_view(), name='topics'),
    path('topics/', views.topics.as_view(), name='topics'),
    path('topic/<int:topic_id>/', views.topic.as_view(), name='topic'),
    path('topic/<int:topic_id>/<int:entry_id>/',
         views.topic.as_view(), name='topic'),
    path('topics/<str:public>/<str:new_topic>/',
         views.topics.as_view(), name='topics'),
    #path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),

]
