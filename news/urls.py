from django.urls import path
from news.views import CreateNewsView, ListNewsView, DestroyNewsView, CreateCommentsView, ListCommentsView, \
    DestroyCommentsView

urlpatterns = [
    path('news/create', CreateNewsView.as_view()),
    path('news/list', ListNewsView.as_view()),
    path('news/<pk>', DestroyNewsView.as_view()),

    path('comment/create', CreateCommentsView.as_view()),
    path('comment/list', ListCommentsView.as_view()),
    path('comment/<pk>', DestroyCommentsView.as_view()),

]
