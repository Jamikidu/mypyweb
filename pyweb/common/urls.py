from django.contrib.auth import views as auth_views
from django.urls import path
from common import views

app_name = 'common'
#순서 url 먼저 따주고 views 만들어주고 html 사이트 만들고

urlpatterns = [
    # 클래스형 LoginView를 사용
    path('login/', auth_views.LoginView.as_view(
        template_name='common/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 함수형 view를 사용
    path('signup/', views.signup, name='signup'),
]