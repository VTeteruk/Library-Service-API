from django.db import models


class Book(models.Model):
    class CoverTypeChoices(models.TextChoices):
        HARD = "Hard"
        SOFT = "Soft"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=10, choices=CoverTypeChoices.choices)
    inventory = models.IntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.title} ({self.author})"
