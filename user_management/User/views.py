import json
import logging
from django.forms import ValidationError
from django.http import JsonResponse, QueryDict
from django.views import View
from .forms import CreateUserForm
from .models import User
from .constants import user_properties_constants as UserProperty


class UserView(View):
    def post(self, request):
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user: User = form.save(commit=False)
            try:
                user.set_password(user.password)
            except ValidationError as ve:
                logging.error(f"Error while setting password: {ve.message}")
                return JsonResponse({"error": ve.messages}, status=400)
            token = user.generate_jwt_token()
            user.save()
            logging.info(f"New user with email: {user.email} created sucessfully")
            return JsonResponse(
                {"token": token, "email": user.email, "full_name": user.full_name}
            )
        else:
            logging.error(f"Error in creating user, error: {form.errors}")
            return JsonResponse({"error": form.errors}, status=400)

    def patch(self, request):
        token = request.META.get("HTTP_AUTHORIZATION", "").split(" ")[-1]
        payload = User.decode_jwt_token(token)
        if not payload:
            logging.warn("Invalid Token")
            return JsonResponse({"error": "Invalid token"}, status=400)

        email = payload.get(UserProperty.email)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        data = json.loads(request.body)

        if UserProperty.password in data:
            try:
                user.set_password(data[UserProperty.password])
            except ValidationError as ve:
                logging.error(
                    f"Error while updating password for user:{email} and error: {ve.message}"
                )
                return JsonResponse({"error": ve.messages}, status=400)
        if UserProperty.full_name in data:
            user.full_name = data[UserProperty.full_name]
        if UserProperty.bio in data:
            user.bio = data[UserProperty.bio]

        user.save()

        return JsonResponse({"message": "User updated successfully"})
