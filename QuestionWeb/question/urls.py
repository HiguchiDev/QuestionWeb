from django.urls import path
from question import views

app_name = 'question'
urlpatterns = [
    # 書籍
    path('create/', views.QuestionCreateFormsetView.as_view(), name='q_create'),   # 一覧
    path('detail/<int:pk>/', views.QuestionDetailView.as_view(), name='q_detail'),
    path('update/<int:pk>/', views.QuestionUpdateFormsetView.as_view(), name='q_update'),
]