from django.urls import path
from .views import CategoryView,CourseView,CourseDetailView,CourseChapterView
urlpatterns = [
    path('category',CategoryView.as_view()),
    path('list',CourseView.as_view()),
    path('detail/<int:pk>',CourseDetailView.as_view()),
    path('coursechapter/<int:pk>',CourseChapterView.as_view()),
]