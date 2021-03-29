from django.core.paginator import Paginator

class Mailbox():
    """ Returns a mailbox after making sure it is valid """
    
    def __init__(self, email, request, mailbox):
        self.email = email
        self.request = request
        self.mailbox = mailbox

    def is_mailbox_valid(self):
        return (self.mailbox == "inbox" or 
                    self.mailbox == "sent" or 
                    self.mailbox == "archive" or 
                    self.mailbox == "trash"
            )

    def serialize_data(self):

        # Filter emails returned based on mailbox
        if self.mailbox == "inbox":
            queryset = self.email.objects.filter(
                user=self.request.user, recipients=self.request.user, archived=False, trashed=False
            )
        elif self.mailbox == "sent":
            queryset = self.email.objects.filter(
                user=self.request.user, sender=self.request.user, trashed=False
            )
        elif self.mailbox == "archive":
            queryset = self.email.objects.filter(
                user=self.request.user, recipients=self.request.user, archived=True
            )
        elif self.mailbox == "trash":
            queryset = self.email.objects.filter(
                user=self.request.user, trashed=True
            )

        # Return emails in reverse chronologial order
        emails = queryset.order_by("-timestamp").all()
        return [email.serialize() for email in emails]