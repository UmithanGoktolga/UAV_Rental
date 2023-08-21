from django.db import models
from django.contrib.auth.models import AbstractBaseUser


CAT_CHOICES = (
    ('cat1','CATEGORY-1'),
    ('cat2', 'CATEGORY-2'),
    ('cat3','CATEGORY-3'),
)

class User(AbstractBaseUser):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.CharField(max_length=100, unique=True) # unique
    phone = models.CharField(max_length=12)
    password = models.CharField(max_length=256)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'

class Category(models.Model):
    title = models.CharField(max_length=12,  choices=CAT_CHOICES, default='cat1')   

   
class UAV(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    weigth = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    is_available = models.BooleanField(default=True)  # To check if a UAV is available for rent

    def __str__(self):
        return f"{self.brand} {self.model}"

class Rental(models.Model):
    uav = models.ForeignKey(UAV, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


    def is_uav_available(self):

        overlapping_rentals = Rental.objects.filter(
            uav=self.uav,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date
        ).exclude(id=self.id)  # exclude the current rental if you're updating

        return not overlapping_rentals.exists()

    class Meta:
        ordering = ['-start_date']  # to get recent rentals first

    def __str__(self):
        return f"{self.user.name} rented {self.uav.brand} {self.uav.model} from {self.start_date} to {self.end_date}"