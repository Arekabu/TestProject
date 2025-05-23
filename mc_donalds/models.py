from tkinter.constants import CASCADE
from django.db import models
from datetime import datetime, timezone


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add = True)
    time_out = models.DateTimeField(null = True)
    cost = models.FloatField(default = 0.0)
    pickup = models.BooleanField(default = False)
    complete = models.BooleanField(default = False)
    staff = models.ForeignKey('Staff', on_delete = models.CASCADE)
    products = models.ManyToManyField('Product', through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now(timezone.utc)
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:
            return (self.time_out - self.time_in).total_seconds() // 60
        else:
            return (datetime.now(timezone.utc) - self.time_in).total_seconds() // 60

class Product(models.Model):
    name = models.CharField(max_length = 255)
    price = models.FloatField(default = 0.0)
    composition = models.TextField(default = "Состав не указан")

    def __str__(self):
        return self.name + "/" + str(self.price)

class Staff(models.Model):
    director = 'DI'
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'

    POSITIONS = [
        (director, 'Директор'),
        (admin, 'Администратор'),
        (cook, 'Повар'),
        (cashier, 'Кассир'),
        (cleaner, 'Уборщик')
    ]
    full_name = models.CharField(max_length = 255)
    position = models.CharField(max_length = 2, choices = POSITIONS, default = cashier)
    labor_contract = models.IntegerField()

    def __str__(self):
        return f'{self.full_name}'

    def get_last_name(self):
        return self.full_name.split()[0]

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    amount = models.IntegerField(default = 1, db_column='amount')

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self.amount = int(value) if value >= 0 else 0
        self.save()