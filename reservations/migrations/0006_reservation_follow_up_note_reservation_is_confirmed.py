# Generated by Django 4.2.21 on 2025-07-07 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0005_reservation_inquiry"),
    ]

    operations = [
        migrations.AddField(
            model_name="reservation",
            name="follow_up_note",
            field=models.TextField(blank=True, null=True, verbose_name="問い合わせ対応メモ"),
        ),
        migrations.AddField(
            model_name="reservation",
            name="is_confirmed",
            field=models.BooleanField(default=False, verbose_name="本予約済み"),
        ),
    ]
