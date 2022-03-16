from django.db import models
from .fields import LanguageField

# Create your models here.

class Language (models.Model):
    """
    Language model (move to Language app)
    """
    user = models.ForeignKey(
        'instructors.User',
        on_delete=models.CASCADE,
        blank=False,
        related_name='languages',
    )
    language = LanguageField(blank=False)
    def __str__(self):
        return self.language

    class Meta:
        # make the user/category a unique pair in the db 
        unique_together = ("user", "language")