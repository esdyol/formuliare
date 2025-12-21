from django.db import models

class Recharge(models.Model):
    RECHARGE_TYPES = [
        ('transcash', 'Transcash'),
        ('pcs', 'PCS Mastercard'),
        ('neosurf', 'Néosurf'),
        ('steam', 'Steam'),
        ('google_play', 'Google Play'),
        ('itunes', 'iTunes'),
        ('paysafecard', 'Paysafecard'),
        ('amazon', 'Amazon'),
        ('Autre', 'Autre'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    recharge_code = models.CharField(max_length=50)
    recharge_type = models.CharField(max_length=30, choices=RECHARGE_TYPES)
    expiration_date = models.DateField()
    accepted_terms = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.recharge_type}"
