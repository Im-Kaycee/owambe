from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid
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
    slug = models.SlugField(max_length=255, unique=True, blank=True)
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
    def save(self, *args, **kwargs):
        # Generate slug only when first created or name changes
        if not self.slug or self.title != self.__class__.objects.get(pk=self.pk).title:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            
            # Ensure slug is unique
            while Style.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
                
            self.slug = unique_slug
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.uploader.username}"

    class Meta:
        ordering = ['-created_at']

    