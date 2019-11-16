from django.urls import path
from . import views
from .views import (ProjectListView,
                    ProjectDetailView,
                    ProjectCreateView,
                    ProjectUpdateView,
                    ProjectDeleteView
                    )


urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('new/', ProjectCreateView.as_view(), name='project-create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
]
