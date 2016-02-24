from django.core.validators import EmailValidator, RegexValidator

email_validator = EmailValidator()

phone_validator = RegexValidator(regex=r'^\+?[\d\s]{6,15}$', 
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
