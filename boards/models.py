from django.db import models
from django.conf import settings
from styles.models import Style

class Board(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="boards"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    styles = models.ManyToManyField(Style, blank=True, related_name="boards")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.owner.username})"
