from django.contrib import admin
from .models import Reservation
from .models import SpecialOffer

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date_time', 'number_of_people', 'phone', 'created_at')
    search_fields = ('name', 'email', 'date_time', 'created_at')
    list_filter = ('date_time', 'created_at')
    readonly_fields = ('created_at',)
    fields = (
        'name',
        'email',
        'phone',
        'date_time',
        'number_of_people',
        'inquiry',
        'is_confirmed',
        'follow_up_note',
        'created_at',
    )

#今日の一品アップ用
@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')    
