from django.urls import path, include
from . import views
app_name = 'logs'
urlpatterns = [
    path('', views.index, name='index'),
    path('public-topics/', views.public_topics, name='public_topics'),
    path('topics/', views.topics, name='topics'),
    path('topic/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),

]
