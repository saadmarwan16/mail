from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from .utils.validate_user_info import ValidateUserInfo

User = get_user_model()


class SignUpView(APIView):
    """ Registers a new user """
    
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        confirmation = data.get("confirmation")

        # Make sure all the fields was filled by the user
        if not (name and email and password and confirmation):
            return Response({"error": "Something went wrong, please try again"})

        validate_user = ValidateUserInfo(email=email, password=password, confirmation=confirmation)

        # Make sure the passwords are the same
        if not validate_user.do_passwords_match():
            return Response({"error": "Passwords do not match"})

        # Make sure the email the user entered is not already in the database
        if validate_user.does_email_exist(User):
            return Response({"error": "Email already exists"})

        # Make sure the password is at least 8 characters long
        if not validate_user.is_password_length_valid():
            return Response({"error": "Password must be at least 8 characters"})

        # Create a new user and return success
        user = User.objects.create_user(email=email, password=password, name=name)
        user.save()

        return Response({"success": "User created successfully"})