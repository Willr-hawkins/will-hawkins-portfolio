from django.db import models
from django.core.validators import RegexValidator

class Contact(models.Model):
    """ Store contact form submissions from portfolio wesbsite visitors. """

    # UK phone number validator
    phone_regex = RegexValidator(
        regex = r'^(\+44\s?7\d{3}|\(?07\d{3}\)?)\s?\d{3}\s?\d{3}$',
        message = "Phone number must be a valid UK number (e.g., 07123456789, +447123456789, or (07123) 456789)"
    )

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length = 20,
        blank=True,
        null=True,
    )
    message = models.TextField(help_text="Add your message here...")

    # Metadata fields
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.full_name} - {self.email} ({self.created_at.strftime('%y-%m-%d')})"


