from django.urls import path
from question import views

urlpatterns = [
    # 書籍
    path('question/<int:category_id>/<int:question_no>', views.QuestionView.as_view(), name='question'),
    path('category', views.CategoryView.as_view(), name='category'),
    path('answer_result/<int:category_id>/<int:question_id>/<int:question_no>/<str:question_type>/<int:choice_no>', views.AnswerResultView.as_view(), name='answer_result'),
    path('session_expire', views.SessionExpireView.as_view(), name='session_expire'),
    path('top', views.TopPageView.as_view(), name='top'),
    path('question/stop', views.QuestionStopView.as_view(), name='stop'),
    path('question/preparation', views.PreparationView.as_view(), name='preparation'),
    path('sample/answer/<str:question_type>/<int:question_id>', views.SampleAnswerView.as_view(), name='sample_answer'),
]

