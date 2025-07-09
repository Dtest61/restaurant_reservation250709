from django.contrib import admin
from django.urls import path, include
from reservations import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # トップページのURL
    path('menu', views.menu, name='menu'),  # メニュー表示ページ
    path('reservation', views.reservation, name='reservation'),  # 予約ページ
    path('api/', include('reservations.urls')),
    path('', include('reservations.urls')),  # reservationsアプリケーションのURLをインクルード
    path('control/reservation/<int:reservation_id>/update/', views.update_reservation, name='update_reservation'),
]