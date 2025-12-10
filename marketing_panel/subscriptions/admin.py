from django.contrib import admin
from .models import UserAccess
from .telegram_notify import notify_user



@admin.register(UserAccess)
class UserAccessAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "username", "full_name", "is_active", "expires_at")
    list_filter = ("is_active",)
    search_fields = ("telegram_id", "username", "full_name")

    actions = ["give_30_days", "revoke_access"]

    def save_model(self, request, obj, form, change):
        """
        Вызывается при нажатии "Save" в админке.
        """
        if change:  # объект уже существует
            previous = UserAccess.objects.get(pk=obj.pk)

            # 1) Если is_active стал True, а раньше был False
            if not previous.is_active and obj.is_active:
                notify_user(
                    obj.telegram_id,
                    "🎉 <b>Ваш доступ был активирован!</b>\nДобро пожаловать!"
                )

            # 2) Если изменилась дата окончания подписки
            if previous.expires_at != obj.expires_at:
                notify_user(
                    obj.telegram_id,
                    f"📅 <b>Дата окончания подписки обновлена:</b>\n{obj.expires_at}"
                )

        super().save_model(request, obj, form, change)

    # --- Actions остаются без изменений ---
    def give_30_days(self, request, queryset):
        for obj in queryset:
            obj.is_active = True
            obj.extend_30_days()
            obj.save()

            notify_user(
                obj.telegram_id,
                "🎉 <b>Вам выдан доступ на 30 дней!</b>"
            )
        self.message_user(request, "Пользователю выдан доступ на 30 дней.")
    give_30_days.short_description = "Дать доступ на 30 дней"

    def revoke_access(self, request, queryset):
        for obj in queryset:
            obj.is_active = False
            obj.save()

            notify_user(
                obj.telegram_id,
                "⛔ <b>Ваш доступ был отозван.</b>"
            )
        self.message_user(request, "Доступ отозван.")
    revoke_access.short_description = "Отозвать доступ"
