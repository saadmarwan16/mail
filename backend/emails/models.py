from django.db import models

from backend.accounts.models import UserAccount

class Email(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="emails")
    sender = models.ForeignKey(UserAccount, on_delete=models.PROTECT, related_name="emails_sent")
    recipients = models.ManyToManyField(UserAccount, related_name="emails_received")
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    trashed = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.email,
            "recipients": [user.email for user in self.recipients.all()],
            "subject": self.subject,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "read": self.read,
            "archived": self.archived,
            "trashed": self.trashed
        }