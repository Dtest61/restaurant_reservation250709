from rest_framework import viewsets
from .models import MenuItem, Reservation
from .serializers import MenuItemSerializer, ReservationSerializer
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import Reservation
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.urls import path
from .models import SpecialOffer
from .forms import SpecialOfferForm

from django.core.mail import send_mail
from django.conf import settings

from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer    

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        print("✅ POST受信：", request.data)  # ←ここでログ出るか確認
        from rest_framework.response import Response
        from rest_framework import status

        # 予約保存処理
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            print("🛑 バリデーションエラー:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # 入力データ取得
        data = serializer.validated_data
        name = data.get('name')
        email = data.get('email')
        date_time = data.get('date_time')
        number = data.get('number_of_people')
        inquiry = data.get('inquiry', '')

        # メール本文（HTML + プレーン）
        html_message = render_to_string('emails/reservation_customer.html', {
            'name': name,
            'date_time': date_time,
            'number': number,
            'inquiry': inquiry,
        })

        plain_message = f"""
【SUMI base やおや 浜松店】仮予約内容

お名前: {name}
メール: {email}
予約日時: {date_time}
人数: {number}名
お問い合わせ: {inquiry}

※この予約は仮予約です。当店からのご連絡をもって本予約が成立します。
"""

        # ✅ お客様へメール
        customer_msg = EmailMultiAlternatives(
            subject='【SUMI base やおや】仮予約のご確認',
            body=plain_message,
            from_email='your@email.com',
            to=[email]
        )
        customer_msg.attach_alternative(html_message, "text/html")
        customer_msg.send()

        # ✅ 店舗側へ通知メール
        send_mail(
            subject='【仮予約通知】新しい予約が入りました',
            message=plain_message,
            from_email='your@email.com',
            recipient_list=['store@email.com']
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

#def home(request):
#    return render(request, 'home.html')

def menu(request):
    return render(request, 'menu.html')

def reservation(request):
    return render(request, 'reservation.html')

#管理者用予約確認ページ
@staff_member_required
def admin_reservation_list(request):
    reservations = Reservation.objects.all().order_by('-created_at')
    return render(request, 'reservations/admin_reservation_list.html', {
        'reservations': reservations,
        'special_offer_form': form,
        'special_offer': special_offer
    })

def admin_dashboard(request):
    reservations = Reservation.objects.all().order_by('-created_at')
    special_offer = SpecialOffer.objects.last()

    if request.method == 'POST':
        form = SpecialOfferForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = SpecialOfferForm()
        special_offer = SpecialOffer.objects.last()

    return render(request, 'reservations/admin_reservation_list.html', {
        'reservations': Reservation.objects.all().order_by('-created_at'),
        'special_offer_form': form,
        'special_offer': special_offer
    })

#管理画面
@staff_member_required
def update_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    success = False  # モーダル表示フラグ

    if request.method == "POST":
        old_confirmed = reservation.is_confirmed  # 更新前の状態を記録
        # 変更前の確認状態を保持
        was_confirmed = reservation.is_confirmed
        
        reservation.is_confirmed = 'is_confirmed' in request.POST
        reservation.follow_up_note = request.POST.get('follow_up_note', '')
        reservation.save()
    
          # ✅ 「本予約に変更された」かつ「まだメール送っていない」場合のみ送信
        if reservation.is_confirmed and not reservation.confirmation_email_sent:
            # 本予約完了メール送信
            subject = "【SUMI base やおや】本予約完了のお知らせ"
            message = f"""{reservation.name}様

この度はご予約いただきありがとうございます。
以下の内容にて、ご予約が確定しました。

――――――――――――――
ご予約日時：{reservation.date_time.strftime('%Y/%m/%d %H:%M')}
ご来店人数：{reservation.number_of_people}名様
お問い合わせ：{reservation.inquiry or '（なし）'}
――――――――――――――

ご来店を心よりお待ちしております。
SUMI base やおや 浜松店
"""

            send_mail(
                subject=subject,
                message=message,
                from_email='your@email.com',  # 必ず有効なメールを指定
                recipient_list=[reservation.email],
                fail_silently=False
            )

        success = True

    reservations = Reservation.objects.all().order_by('-created_at')
    special_offer_form = SpecialOfferForm()
    special_offer = SpecialOffer.objects.last()

    return render(request, 'reservations/admin_reservation_list.html', {
        'reservations': reservations,
        'updated': success,
        'updated_id': reservation.id,
        'special_offer_form': special_offer_form,  # ✅ 忘れず追加！
        'special_offer': special_offer             # ✅ 忘れず追加！
    })

#一品プレゼント
def home(request):
    special_offer = SpecialOffer.objects.last()  # 最新のものを1つ取得
    return render(request, 'home.html', {
        'special_offer': special_offer
    })
