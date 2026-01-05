from rest_framework_simplejwt.tokens import RefreshToken


def generate_refresh_token(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": refresh, "access": refresh.access_token}
