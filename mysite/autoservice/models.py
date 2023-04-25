from django.db import models

# Create your models here.
class VehicleModel(models.Model):
    make = models.CharField(verbose_name="Marke", max_length=100)
    model = models.CharField(verbose_name="Modelis", max_length=100)

    def __str__(self):
        return f"{self.make} {self.model}"


class Vehicle(models.Model):
    plate = models.CharField(verbose_name="Valstybinis numeris", max_length=100)
    vehicle_model = models.ForeignKey(to="VehicleModel",
                                      verbose_name="Automobilio modelis",
                                      on_delete=models.SET_NULL,
                                      null=True)
    vin = models.CharField(verbose_name="VIN kodas", max_length=100)
    owner_name = models.CharField(verbose_name="Savininkas", max_length=100)

    def __str__(self):
        return f"{self.vehicle_model} ({self.plate})"


class Service(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=100)
    price = models.IntegerField(verbose_name="Kaina")

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    date = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    vehicle = models.ForeignKey(to="Vehicle", verbose_name="Automobilis", on_delete=models.CASCADE)
    suma = models.CharField(verbose_name="Suma", max_length=100)

    def __str__(self):
        return f"{self.vehicle} ({self.date})"


class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE)
    service = models.ForeignKey(to="Service", verbose_name="Paslauga", on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(verbose_name="Kiekis")

    def __str__(self):
        return f"{self.order.vehicle} ({self.order.date}): {self.service} - {self.quantity}"

