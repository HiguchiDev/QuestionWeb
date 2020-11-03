from django.urls import path
from . import views


urlpatterns = [
    path('category/list/', views.CategoryList.as_view(), name='category_list'),
    path('question/list/', views.QuestionList.as_view(), name='question_list'),
    path('category_question/list/<int:category_id>', views.CategoryQuestionList.as_view(), name='category_question_list'),
    path('detail/<int:pk>/', views.QuestionDetail.as_view(), name='question_detail'),
    path('detail/<int:category_id>/<int:pk>/', views.QuestionDetail.as_view(), name='question_detail'),
    path('detail_img/<int:pk>/', views.ImageQuestionDetail.as_view(), name='question_detail_img'),
    path('detail_img/<int:category_id>/<int:pk>/', views.ImageQuestionDetail.as_view(), name='question_detail_img'),
    path('create/', views.QuestionCreateFormsetView.as_view(), name='question_create'),
    path('create_img/', views.ImageQuestionCreateFormsetView.as_view(), name='question_create_img'),
    path('update/<int:pk>', views.QuestionUpdateFormsetView.as_view(), name='question_update'),
    path('update_img/<int:pk>', views.ImageQuestionUpdateFormsetView.as_view(), name='question_update_img'),
    path('delete/<int:pk>', views.QuestionDeleteView.as_view(), name='question_delete'),
    path('delete_img/<int:pk>', views.ImageQuestionDeleteView.as_view(), name='question_delete_img'),
    path('question/add/<int:category_id>', views.QuestionAddView.as_view(), name='question_add'),
    path('question/add/<int:category_id>/<str:add_result>', views.QuestionAddView.as_view(), name='question_add'),
    path('question/exclusion/<int:category_id>', views.QuestionExclusionView.as_view(), name='question_exclusion'),
    path('question/exclusion/<int:category_id>/<str:exclusion_result>', views.QuestionExclusionView.as_view(), name='question_exclusion'),
]