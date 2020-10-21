from django.urls import path
from question import views

urlpatterns = [
    # 書籍
    path('question/<int:question_id>', views.QuestionView.as_view(), name='question'),   # 一覧
]