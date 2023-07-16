from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),  # django.contrib.auth앱의 LoginView클래스를 활용하므로 별도의 views.py파일 수정할 필요 없음. template_name을 'common/login.html'로 설정하면 registration 디렉터리가 아닌 common 디렉터리에서 login.html 템플릿 파일을 참조하게 됨.
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup')
    ]