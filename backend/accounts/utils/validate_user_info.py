class ValidateUserInfo():
    """
        This class is a utility class that is used to make sure the information
        the user entered is acceptable
    """

    def __init__(self, email, password, confirmation):
        self.email = email
        self.password = password
        self.confirmation = confirmation
    
    def do_passwords_match(self):
        return self.password == self.confirmation

    def does_email_exist(self, User):
        return User.objects.filter(email=self.email).exists()

    def is_password_length_valid(self):
        return len(self.password) >= 8