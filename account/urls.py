from django.urls import path
from account.views import TeacherLoginAPIView, StudentLoginAPIView, TeacherRegistrationAPIView, \
    StudentRegistrationAPIView, TeacherProfileAPIView, AddStudentToTeacher, AddNewToTeacher, AddExerciseToTeacher, \
    TeacherUpdateAPIView, TeacherLogoutAPIView, StudentLogoutAPIView, StudentExerciseList, StudentNewList, \
    ExerciseResponseListCreate, StudentProfileAPIView, UpdateExercise, UpdateNew, ExerciseResponseUpdate

urlpatterns = [
    path("register/teacher/", TeacherRegistrationAPIView.as_view(), name="register-teacher"),
    path("register/student/", StudentRegistrationAPIView.as_view(), name="register-student"),
    path("login/teacher/", TeacherLoginAPIView.as_view(), name="login-teacher"),
    path("login/student/", StudentLoginAPIView.as_view(), name="login-student"),
    path('logout/teacher/', TeacherLogoutAPIView.as_view(), name="logout-teacher"),
    path('logout/student/', StudentLogoutAPIView.as_view(), name="logout-student"),
    path("profile/teacher/", TeacherProfileAPIView.as_view(), name="profile-teacher"),
    path("profile/student/", TeacherProfileAPIView.as_view(), name="profile-teacher"),
    path("profile/teacher/update/", TeacherUpdateAPIView.as_view(), name="update-teacher"),
    path("profile/student/update/", StudentProfileAPIView.as_view(), name="update-teacher"),
    path("teacher/add_student/", AddStudentToTeacher.as_view(), name="add-student"),
    path("teacher/add_new/", AddNewToTeacher.as_view(), name="add-new"),
    path("teacher/add_exercise/", AddExerciseToTeacher.as_view(), name="add-exercise"),
    path("teacher/update_exercise/", UpdateExercise.as_view(), name="update-exercise"),
    path("teacher/update_new/", UpdateNew.as_view(), name="update-exercise"),
    path("student/exercises_list/", StudentExerciseList.as_view(), name='student_exercise_list'),
    path("student/exercises/response/", ExerciseResponseListCreate.as_view(), name='student_exercise_response'),
    path("student/exercises/response/update/", ExerciseResponseUpdate.as_view(), name='exercise_response_update'),
    path("student/news_list/", StudentNewList.as_view(), name='student_news_list'),

    # path("teacher/news/update/<slug:slug>/", EditNewByTeacherAPIView.as_view(), name="update-new-by-teacher"),

    # path("change-password/", UserChangePasswordAPIView.as_view(), name="change-password"),
    # path("send-reset-email/", SendPasswordResetEmailAPIView.as_view(), name="send-reset-email"),
    # path("reset-password/<uid>/<token>/", UserResetPasswordView.as_view(), name="reset-password")

]
