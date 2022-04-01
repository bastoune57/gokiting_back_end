from django.db import models

# Create your models here.

# define category choices
KITEBOARD = 'KB'
WING = 'WI'
KITEFOIL = 'KF'
SUP = 'SP'
SURF = 'SF'
# define  choices / value relations
WATER_SPORT_CHOICES = [
    (KITEBOARD, 'Kiteboard'),
    (WING, 'Wingfoil'),
    (KITEFOIL, 'Kitefoil'),
    (SUP, 'SUP'),
    (SURF, 'Surf'),
]

class Category (models.Model):
    """
    Category model (move to Category app?)
    """
    # add a category field
    category = models.CharField(
        max_length=2,
        choices=WATER_SPORT_CHOICES,
        default=KITEBOARD,
    )
    # add corresponding user field
    user = models.ForeignKey(
        'instructors.User',
        on_delete=models.CASCADE,
        blank=False,
        related_name='categories',
    )
    class Meta:
        # make the user/category a unique pair in the db 
        unique_together = ("user", "category")
    def __str__(self):
        return self.category