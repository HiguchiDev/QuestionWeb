from django.urls import path
from question import views

urlpatterns = [
    # 書籍
    path('question/<int:category_id>/<int:question_no>', views.QuestionView.as_view(), name='question'),
    path('category', views.CategoryView.as_view(), name='category'),
    path('answer_result/<int:category_id>/<int:question_id>/<int:question_no>/<int:choice_no>', views.AnswerResultView.as_view(), name='answer_result'),
]