from django.urls import path
# from .views import add_violation
from .views import (PostListView,
                    PostCreateView,
                    PostDetailView,
                    PostCreateViolationView,
                    StudentViolationsView,
                    PostUpdateView,
                    PostUpdateViolationView,
                    DeleteViolationView,
                    DeleteStudentView)
urlpatterns = [
    # path('add-violation/',add_violation, name='add_violation'),
    # Add other URLs as needed
    path('', PostListView.as_view(), name='disciplinetracking-home'),
    path('create/',PostCreateView.as_view(), name='disciplinetracking-create'),
    path('student_detail/<int:pk>/',PostDetailView.as_view(), name='disciplinetracking-detail'),
    path('student/<int:pk>/',StudentViolationsView.as_view(), name='disciplinetracking-list'),
    path('student/<int:pk>/create',PostCreateViolationView.as_view(), name='disciplinetracking-add-violation'),
    path('update/<int:pk>/',PostUpdateView.as_view(),name='disciplinetracking-update'),
    path('student/<int:pk>/update',PostUpdateViolationView.as_view(),name='disciplinetracking-update-violation'),
    path('student_violations/<int:pk>/delete/', DeleteViolationView.as_view(), name='delete-violation'),
    path('student/<int:pk>/delete/', DeleteStudentView.as_view(), name='delete-student'),
]