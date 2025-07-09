from rest_framework import serializers
from .models import MenuItem, Reservation

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'image']

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'name', 'email', 'phone', 'date_time', 'number_of_people', 'inquiry', 'created_at']

        read_only_fields = ['created_at']  # ← 編集不可にする（オプション）