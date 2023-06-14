import json
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from .models import User
from .constants import raw_path
from django.core.files.uploadedfile import SimpleUploadedFile


class UserViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("user")

    def test_create_user_sucess(self):
        form_data = {
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "abcd wxzy",
            "bio": "Test bio",
            "profile_picture": SimpleUploadedFile(
                name="test_image.jpg",
                content=open(
                    raw_path.TEST_IMAGE_SOURCE,
                    "rb",
                ).read(),
                content_type="image/jpeg",
            ),
        }

        with patch("User.views.User.decode_jwt_token"):
            response = self.client.post(self.url, form_data)
            self.assertEqual(response.status_code, 200)
            self.assertIn("token", response.json())
            self.assertIn("email", response.json())
            self.assertIn("full_name", response.json())

    def test_create_user_error_no_email(self):
        form_data = {
            "email": "",
            "password": "testpassword",
            "full_name": "abcd wxzy",
            "bio": "Test bio",
            "profile_picture": SimpleUploadedFile(
                name="test_image.jpg",
                content=open(
                    "C:\\Users\\aryan2\\Desktop\\docs\\projects\\django-user-management\\user_management\\media\\images\\profiles\\github_avatar.png",
                    "rb",
                ).read(),
                content_type="image/jpeg",
            ),
        }
        with patch("User.views.User.decode_jwt_token"):
            response = self.client.post(self.url, form_data)
            self.assertEqual(response.status_code, 400)
        # missing parameter no User created

    def test_update_user_success(self):
        user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            full_name="John Doe",
            bio="Test bio",
        )

        request_data = {
            "password": "strongpassword1234",
            "full_name": "Updated Name",
            "bio": "Updated bio",
        }

        # Mock the JWT token decoding
        with patch("User.views.User.decode_jwt_token") as mock_decode_token:
            mock_decode_token.return_value = {
                "email": user.email,
                "full_name": user.full_name,
            }

            response = self.client.patch(
                self.url,
                json.dumps(request_data),
                HTTP_AUTHORIZATION="Bearer fake-token",
            )
            self.assertEqual(response.status_code, 200)
            # update successful
            self.assertIn("message", response.json())

            user.refresh_from_db()
            self.assertEqual(user.full_name, "Updated Name")
            self.assertEqual(user.bio, "Updated bio")

    def test_update_user_error_weak_password(self):
        # Create a test user in the database
        user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            full_name="John Doe",
            bio="Test bio",
        )

        request_data = {
            "password": "abcd",
            "full_name": "Updated Name",
            "bio": "Updated bio",
        }

        with patch("User.views.User.decode_jwt_token") as mock_decode_token:
            mock_decode_token.return_value = {
                "email": user.email,
                "full_name": user.full_name,
            }

            response = self.client.patch(
                self.url,
                json.dumps(request_data),
                HTTP_AUTHORIZATION="Bearer fake-token",
            )
            self.assertEqual(response.status_code, 400)
        # weak password not accepted

    def test_update_user_no_user(self):
        # Create a test user in the database
        user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            full_name="John Doe",
            bio="Test bio",
        )
        request_data = {
            "password": "strongpassword1234",
            "full_name": "Updated Name",
            "bio": "Updated bio",
        }
        with patch("User.views.User.decode_jwt_token") as mock_decode_token:
            mock_decode_token.return_value = {
                "email": "inavlid_mail@company.com",
                "full_name": user.full_name,
            }

            response = self.client.patch(
                self.url,
                json.dumps(request_data),
                HTTP_AUTHORIZATION="Bearer fake-token",
            )
            self.assertEqual(response.status_code, 404)
            # user not found 404
