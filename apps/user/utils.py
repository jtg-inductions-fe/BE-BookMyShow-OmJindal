from rest_framework_simplejwt.tokens import RefreshToken


def generate_refresh_token(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": refresh, "access": refresh.access_token}


def set_refresh_cookie(response, refresh_token):
    response.set_cookie(
        key="refresh",
        value=str(refresh_token),
        httponly=True,
        secure=True,
        samesite="strict",
    )
