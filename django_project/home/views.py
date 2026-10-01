import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import AccessToken

from .models import User


def hello_world(request):
    return JsonResponse({
        "message": "Hello World"
    })


@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({
            "message": "Chỉ hỗ trợ phương thức POST"
        }, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "message": "Dữ liệu JSON không hợp lệ"
        }, status=400)

    username = data.get("userName")
    password = data.get("password")

    if not username or not password:
        return JsonResponse({
            "message": "Vui lòng nhập userName và password"
        }, status=400)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({
            "message": "Tài khoản không tồn tại"
        }, status=401)

    if user.password != password:
        return JsonResponse({
            "message": "Sai mật khẩu"
        }, status=401)

    token = AccessToken()
    token["user_id"] = user.id_user
    token["username"] = user.username

    user.token = str(token)
    user.save()

    return JsonResponse({
        "message": "Đăng nhập thành công",
        "userName": user.username,
        "token": str(token)
    })