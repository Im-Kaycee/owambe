from django.db import models
from django.conf import settings
from styles.models import Style
from django.utils.text import slugify
import uuid
class Board(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="boards"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    styles = models.ManyToManyField(Style, blank=True, related_name="boards")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        # Generate slug only when first created or name changes
        if not self.slug or self.name != self.__class__.objects.get(pk=self.pk).name:
            base_slug = slugify(self.name)
            unique_slug = base_slug
            counter = 1
            
            # Ensure slug is unique
            while Board.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
                
            self.slug = unique_slug
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} by {self.owner.username}"

    class Meta:
        ordering = ['-created_at']
