class Compose():
    """ Sanitize an email to be sent """

    def __init__(self, data):
        self.data = data

    def get_recipients(self):
        return [email.strip() for email in self.data.get("recipients").split(",")]

    def get_users(self, emails, users, recipients):

        # Convert email addresses to users
        for email in emails:
            try:
                user = users.objects.get(email=email)
                recipients.append(user)
            except users.DoesNotExist:
                return (False, email)

        return (True, recipients)

    def send_mail(self, recipients, user, email_class, users):

        # Get contents of email
        subject = self.data.get("subject", "")
        body = self.data.get("body", "")

        # Create one email for each recipient, plus sender
        users.add(user)
        users.update(recipients)
        for single_user in users:
            email = email_class(
                user=single_user,
                sender=user,
                subject=subject,
                body=body,
                read=single_user == user
            )
            email.save()
            
            for recipient in recipients:
                email.recipients.add(recipient)
            email.save()