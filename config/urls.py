from django.contrib import admin
from django.urls import path, include
from pybo.views import base_views # url매핑 위해 임포트해줌.

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('pybo/', views.index),
    # 위 코드는 urls.py파일에서 /pybo/ 페이지에 해당하는 URL 매핑 등록해서 주소와 화면 연결 시켜줌. pybo/ URL과 views.index를 매핑해 연결하는 코드. views.index는 views.py 파일의 index함수를 의미함. 그러나 pybo앱에 URL 매핑하는데 config 디렉터리에 들어와야 하는 건 짜임새가 부족하므로 다른 방법을 사용해보자.
    path('pybo/', include('pybo.urls')),
    # 위 코드는 pybo/로 시작되는 페이지 요청은 전부 pybo/urls.py 파일에 있는 URL 매핑을 참고해 처리하라는 의미임. 즉, pybo 앱과 관련된 URL 요청은 앞으로 pybo/urls.py 파일에서 관리하라는 뜻. pybo 디렉터리 안에 urls.py 파일 생성하자.
    path('common/', include('common.urls')),
    path('', base_views.index, name='index')
]
