from django.db import models
from django.conf import settings

class Style(models.Model):
    CATEGORY_CHOICES = (
        ('men', 'Men'),
        ('women', 'Women'),
        ('kids', 'Kids'),
    )

    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_styles"
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="styles/")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    fabric_type = models.CharField(max_length=100, blank=True, null=True)
    occasion = models.CharField(max_length=100, blank=True, null=True)
    colour = models.CharField(max_length=50, blank=True, null=True)

    # Tailor credit info
    tailor_name = models.CharField(max_length=255, blank=True, null=True)
    tailor_whatsapp = models.CharField(max_length=20, blank=True, null=True)
    tailor_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name="credited_styles"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.uploader.username}"
