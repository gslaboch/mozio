from django.core.validators import EmailValidator, RegexValidator

email_validator = EmailValidator()

phone_validator = RegexValidator(regex=r'^\+?\d{0,5}\s?\d{5,15}$', 
                message="Phone number invalid")
