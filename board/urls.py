from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'board'
urlpatterns = [
    path('', views.board_list, name='board_list'),
    path('write/', views.board_write, name='board_write'),
    path('detail/<int:pk>/', views.board_detail, name='board_detail'),
    path('detail/<int:pk>/delete/', views.board_delete, name='board_delete'),
    path('detail/<int:pk>/modify/', views.board_modify, name='board_modify'),

    #과학자 페이지
    path('science/', views.board_science_list, name='board_science_list'),
    path('science/write/', views.board_science_write, name='board_science_write'),
    path('science/detail/<int:pk>/', views.board_science_detail, name='board_science_detail'),
    #파일 다운로드
    path('science/download/', views.file_download, name='file_download'),
]