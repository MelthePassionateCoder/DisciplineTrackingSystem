from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordChangeDoneView
# from .views import add_violation
from .views import (PostListView,
                    PostCreateView,
                    # PostDetailView,
                    PostCreateViolationView,
                    StudentViolationsView,
                    PostUpdateView,
                    PostUpdateViolationView,
                    DeleteViolationView,
                    DeleteStudentView,
                    ChangePassword,
                    offense_summary,
                    download_pdf)
urlpatterns = [
    # path('add-violation/',add_violation, name='add_violation'),
    # Add other URLs as needed
    path('', PostListView.as_view(), name='disciplinetracking-home'),
    path('create/',PostCreateView.as_view(), name='disciplinetracking-create'),
    # path('student_detail/<int:pk>/',PostDetailView.as_view(), name='disciplinetracking-detail'),
    path('student/<int:pk>/',StudentViolationsView.as_view(), name='disciplinetracking-list'),
    path('student/<int:pk>/create',PostCreateViolationView.as_view(), name='disciplinetracking-add-violation'),
    path('update/<int:pk>/',PostUpdateView.as_view(),name='disciplinetracking-update'),
    path('student/<int:pk>/update',PostUpdateViolationView.as_view(),name='disciplinetracking-update-violation'),
    path('student_violations/<int:pk>/delete/', DeleteViolationView.as_view(), name='delete-violation'),
    path('student/<int:pk>/delete/', DeleteStudentView.as_view(), name='delete-student'),
    path('download_pdf/<int:pk>/', download_pdf, name='download_pdf'),
    path('user/change-password/', ChangePassword.as_view(), name='change_password'),
    # path('offense-summary/', OffenseSummaryView.as_view(), name='offense_summary'),
    path('offense_summary/', offense_summary, name='offense_summary'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)