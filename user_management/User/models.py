from django.db import models
from jwt import encode, decode
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password


class User(models.Model):
    email = models.EmailField(primary_key=True, db_index=True)
    password = models.CharField(max_length=128)
    full_name = models.CharField(max_length=100)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to="images/profiles")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        validate_password(raw_password)
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def generate_jwt_token(self):
        payload = {"email": self.email, "full_name": self.full_name}
        return encode(payload, settings.SECRET_KEY, algorithm="HS256")

    @staticmethod
    def decode_jwt_token(token):
        try:
            return decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except:
            return None
