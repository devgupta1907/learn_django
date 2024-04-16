from django.urls import path
from .views import home, create_student, log_out, login_student, create_teacher, login_teacher, userListView, update_user
from .views import CreateStudent, UserListView


urlpatterns = [
    path('', home, name='home'),
    # path('csession/', create_session, name='create_session'),
    # path('gsession/', get_session, name='get_session'),
    path('create_s/', create_student, name='create_student'),
    path('logout/', log_out, name='logout'),
    # path('create_s/', CreateStudent.as_view(), name='create_student_class'),
    # path('view_users', UserListView.as_view(), name='view_users'),
    # path('view_users', userListView, name='view_users'),
    path('create_t/', create_teacher, name='create_teacher'),
    path('login_s/', login_student, name='login_student'),
    path('login_t/', login_teacher, name='login_teacher'),
    path('update/', update_user, name="update_user")
]
