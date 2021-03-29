from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView

from backend.accounts.models import UserAccount

from .models import Email
from .utils.compose import Compose
from .utils.mailbox import Mailbox
from .utils.single_email import SingleEmail


class ComposeEmailView(APIView):
    """ Compose a new email """

    def post(self, request, format=None):
        compose = Compose(self.request.data)
        emails = compose.get_recipients()

        # Make sure the list of recipients is not empty
        if emails == [""]:
            return Response({"error": "At least one recipient required."})

        recipients = compose.get_users(emails, UserAccount, list())

        # Make sure the recipients(s) is valid
        if not recipients[0]:
            return Response({"error": f"User with email {recipients[1]} does not exist."})

        # Send the email and return success
        recipients = recipients[1]
        compose.send_mail(recipients, self.request.user, Email, set())

        return Response({"success": "New email composed successfully."})


class MailboxView(ListAPIView):
    """ View the user's mailbox """

    def get(self, request, mailbox, page_number, format=None):
        check_mailbox = Mailbox(Email, self.request, mailbox)

        # Make sure the mailbox is valid
        if not check_mailbox.is_mailbox_valid():
            return Response({"error": "Invalid mailbox."})

        
        emails = check_mailbox.serialize_data()

        paginator = Paginator(object_list=emails, per_page=10, allow_empty_first_page=True)
        page_object = paginator.get_page(number=page_number)

        results = {
            "has_more": page_object.has_next(),
            "next_number": page_object.next_page_number() if page_object.has_next() else None,
            "body": page_object.object_list
        }


        return Response(results)


class SingleEmailView(RetrieveUpdateAPIView):
    """ View the details for a single email """

    def __init__(self):
        self.single_mail = SingleEmail(Email)

    def get(self, request, email_id, format=None):

        # self.single_mail = SingleEmail(Email)
        email = self.single_mail.does_email_exist(self.request.user, email_id)

        # Make sure the email is available
        if not email:
            return Response({"error": "Email not found."})

        # Mark email as read and return email contents
        self.single_mail.update_email({"read": True}, self.request.user, email_id)

        return Response(email.serialize())


    def put(self, request, email_id, format=None):

        # self.single_mail = SingleEmail(Email)
        email = self.single_mail.does_email_exist(self.request.user, email_id)
        data = self.request.data

        # Make sure the email is available
        if not email:
            return Response({"error": "Email not found."})

        # Make sure the email update method is allowed
        if not self.single_mail.is_update_method_allowed(data):
            return Response({"error": "The email update method is not allowed."})

        # Update email and return success
        self.single_mail.update_email(data, self.request.user, email_id)

        return Response({"success": "The email was successfully updated."})