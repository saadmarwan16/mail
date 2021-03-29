class SingleEmail():
    """ Validata if a single mail send proceed to be sent """

    def __init__(self, email):
        self.email = email

    def does_email_exist(self, user, email_id):

        # Query for requested email
        try:
            email = self.email.objects.get(user=user, pk=email_id)
            return email
        except self.email.DoesNotExist:
            return None

    def is_update_method_allowed(self, data):
        return (data.get("read") is not None or 
                data.get("archived") is not None or 
                data.get("trashed") is not None
    )

    def update_email(self, data, user, email_id):
        email = self.email.objects.get(user=user, pk=email_id)

        # Update whether email is read, trashed or should be archived
        if data.get("read") is not None:
            email.read = data["read"]
        if data.get("archived") is not None:
            email.archived = data["archived"]
        if data.get("trashed") is not None:
            email.trashed = data["trashed"]
        email.save()