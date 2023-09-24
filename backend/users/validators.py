from django.core.exceptions import ValidationError


class MaximumLengthValidator:
    def __init__(self, max_length=150):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                (f'Этот пароль длиннее {self.max_length} символов'),
                code='password_too_long',
                params={'max_length': self.max_length},
            )

    def get_help_text(self):
        return (f"Ваш пароль должен быть менее {self.max_length} символов.")
