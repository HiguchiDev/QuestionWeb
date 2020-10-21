from django.urls import path
from . import views


urlpatterns = [
    path('category/list/', views.CategoryList.as_view(), name='category_list'),
    path('question/list/<int:category_id>', views.QuestionList.as_view(), name='question_list'),
    path('detail/<int:pk>/', views.QuestionDetail.as_view(), name='question_detail'),
    path('create/<int:category_id>', views.QuestionCreateFormsetView.as_view(), name='question_create'),
    path('update/<int:category_id>/<int:pk>', views.QuestionUpdateFormsetView.as_view(), name='question_update'),
    path('question/sort_delete/<int:pk>/', views.QuestionSortOrDeleteFormSetView.as_view(), name='question_delete_sort'),
]