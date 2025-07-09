# reservations/urls.py
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import MenuItemViewSet, ReservationViewSet
from .views import admin_reservation_list

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

router = DefaultRouter()
router.register(r'menu', MenuItemViewSet)
router.register(r'reservations', ReservationViewSet)

urlpatterns = [
    #path('', include(router.urls)),
    path('', views.home, name='home'), # トップページ
    path('menu', views.menu, name='menu'),
    path('reservation', views.reservation, name='reservation'),

    # API用のURL設定
    path('api/', include(router.urls)),  # APIエンドポイント

     # ✅ 管理用ビューのURLを追加
    path('control/', views.admin_dashboard, name='admin_dashboard'),

    path('admin/reservation/<int:reservation_id>/update/', views.update_reservation, name='update_reservation'),
    path('admin/reservations/', admin_reservation_list, name='admin_reservation_list'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]


#urlpatterns += [
#    path('admin/reservations/', admin_reservation_list, name='admin_reservation_list'),
#]

# 画像アップロード対応（MEDIA）
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
