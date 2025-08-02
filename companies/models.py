from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator


class Company(models.Model):
    COMPANY_SIZE_CHOICES = [
            ('00', 'Not Informed'),
            ('01', 'Micro Company'),
            ('03', 'Small Company'),
            ('05', 'Other'),
        ]

    cnpj = models.CharField(primary_key=True, max_length=14)
    name = models.CharField(max_length=200)
    legal_nature = models.CharField(max_length=4)
    qualification = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(99)]
    )
    capital = models.DecimalField(
        max_digits =15,
        decimal_places=2  
    )
    size = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        choices=COMPANY_SIZE_CHOICES
    )
    federative_entity = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return self.name


