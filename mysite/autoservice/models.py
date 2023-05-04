from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class VehicleModel(models.Model):
    make = models.CharField(verbose_name="Marke", max_length=100)
    model = models.CharField(verbose_name="Modelis", max_length=100)

    def __str__(self):
        return f"{self.make} {self.model}"

    class Meta:
        verbose_name = "Automobilio modelis"
        verbose_name_plural = "Automobilio modeliai"


class Vehicle(models.Model):
    plate = models.CharField(verbose_name="Valstybinis numeris", max_length=100)
    vehicle_model = models.ForeignKey(to="VehicleModel",
                                      verbose_name="Automobilio modelis",
                                      on_delete=models.SET_NULL,
                                      null=True)
    vin = models.CharField(verbose_name="VIN kodas", max_length=100)
    owner_name = models.CharField(verbose_name="Savininkas", max_length=100)
    cover = models.ImageField('Vaizdas', upload_to='covers', null=True, blank=True)

    def __str__(self):
        return f"{self.vehicle_model} ({self.plate})"

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"


class Service(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=100)
    price = models.IntegerField(verbose_name="Kaina")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Paslauga"
        verbose_name_plural = "Paslaugos"


class Order(models.Model):
    date = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    vehicle = models.ForeignKey(to="Vehicle", verbose_name="Automobilis", on_delete=models.CASCADE)
    client = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    due_back = models.DateTimeField(verbose_name="Bus sutvarkyta", null=True, blank=True)

    LOAN_STATUS = (
        ('p', 'Patvirtinta'),
        ('v', 'Vykdoma'),
        ('a', 'Atšaukta'),
        ('i', 'Įvykdyta')
    )

    status = models.CharField(
        verbose_name='Būsena',
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='v',
        help_text='Status'
    )

    def __str__(self):
        return f"{self.vehicle} ({self.date}) - {self.status}"

    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def total(self):
        total = 0
        orderlines = self.orderlines.all()
        for orderline in orderlines:
            total += orderline.sum()
        return total

    class Meta:
        verbose_name = "Užsakymas"
        verbose_name_plural = "Užsakymai"



class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE, related_name="orderlines")
    service = models.ForeignKey(to="Service", verbose_name="Paslauga", on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(verbose_name="Kiekis")

    def __str__(self):
        return f"{self.order.vehicle} ({self.order.date}): {self.service} - {self.quantity}"

    def sum(self):
        return self.service.price * self.quantity

    class Meta:
        verbose_name = "Užsakymo eilutė"
        verbose_name_plural = "Užsakymo eilutės"


