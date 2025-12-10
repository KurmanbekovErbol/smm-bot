from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import UserAccess
from .serializers import UserAccessSerializer

@api_view(["POST"])
def new_user(request):
    """
    Создаём или обновляем запись пользователя при /start
    Ожидает: telegram_id, username, full_name
    """
    telegram_id = request.data.get("telegram_id")
    if not telegram_id:
        return Response({"error": "telegram_id required"}, status=400)

    obj, created = UserAccess.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={
            "username": request.data.get("username"),
            "full_name": request.data.get("full_name"),
            "is_active": False
        }
    )
    if not created:
        # Обновляем поля, если они изменились
        changed = False
        if request.data.get("username") and obj.username != request.data.get("username"):
            obj.username = request.data.get("username"); changed = True
        if request.data.get("full_name") and obj.full_name != request.data.get("full_name"):
            obj.full_name = request.data.get("full_name"); changed = True
        if changed:
            obj.save()

    return Response({"status": "ok", "created": created})

@api_view(["POST"])
def check_access(request):
    """
    Проверяем доступ: отправляем { access: True/False, expires_at: ... }
    """
    telegram_id = request.data.get("telegram_id")
    if not telegram_id:
        return Response({"error": "telegram_id required"}, status=400)

    try:
        user = UserAccess.objects.get(telegram_id=telegram_id)
    except UserAccess.DoesNotExist:
        return Response({"access": False})

    if user.is_active and user.expires_at and user.expires_at > timezone.now():
        return Response({"access": True, "expires_at": user.expires_at})
    else:
        # автоматическая деактивация, если срок прошёл
        if user.expires_at and user.expires_at <= timezone.now():
            user.is_active = False
            user.save()
        return Response({"access": False})



