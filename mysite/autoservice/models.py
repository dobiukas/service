from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime
from tinymce.models import HTMLField
from PIL import Image
from django.utils.translation import gettext_lazy as _

from datetime import date


class Service(models.Model):
    name = models.CharField(verbose_name='Name', max_length=200)
    price = models.FloatField(verbose_name="Price")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'


class CarModel(models.Model):
    manufacturer = models.CharField(verbose_name='Manufacturer', max_length=200)
    model = models.CharField(verbose_name='Model', max_length=200)

    def __str__(self):
        return f"{self.manufacturer} {self.model}"

    class Meta:
        verbose_name = 'Car Model'
        verbose_name_plural = 'Car Models'


class Car(models.Model):
    owner = models.CharField(verbose_name="Owner", null=True, max_length=200)
    year = models.IntegerField(verbose_name='Year', null=True)
    car_model = models.ForeignKey('CarModel', verbose_name="Model", on_delete=models.SET_NULL, null=True)
    licence_plate = models.CharField(verbose_name='Licence plate', max_length=200)
    vin_code = models.CharField(verbose_name='VIN code', max_length=200)
    photo = models.ImageField('Photo', upload_to='covers', null=True)
    description = HTMLField('Aprašymas', null=True)


    def __str__(self):
        return f"{self.owner}: {self.car_model}, {self.licence_plate}, {self.vin_code}"

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'


class Order(models.Model):
    car = models.ForeignKey('Car', verbose_name=_("Car"), on_delete=models.SET_NULL, null=True)
    due_date = models.DateTimeField(verbose_name=_('Due Date'), null=True, blank=True)
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.SET_NULL, null=True, blank=True)
    #reader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            if self.due_date and datetime.today().replace > self.due_date.replace():
             return True
        return False


    @property
    def total(self):
        uzsakymo_eilutes = OrderLine.objects.filter(order=self.id)
        suma = 0
        for eilute in uzsakymo_eilutes:
            suma += eilute.service.price * eilute.qty
        return suma

    STATUS = (
        ('p', _('Approved')),
        ('v', _('In Progress')),
        ('a', _('Done')),
        ('t', _('Canceled')),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        blank=True,
        default='p',
        help_text=_('Status'),
    )

    def __str__(self):
        return f"{self.car}: {self.car.owner}, {self.due_date}"

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderLine(models.Model):
    order = models.ForeignKey('Order', verbose_name=_("Order"), on_delete=models.SET_NULL, null=True, related_name='lines')
    service = models.ForeignKey('Service', verbose_name=_("Service"), on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField(verbose_name=_("Quantity"))

    @property
    def suma(self):
        return self.service.price * self.qty


    class Meta:
        verbose_name = _('Order Line')
        verbose_name_plural = _('Order Lines')

    def __str__(self):
        return f"{self.order}: {self.service}, {self.qty}"


class OrderComment(models.Model):
    order = models.ForeignKey('Order', verbose_name=_("Order"), on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(verbose_name=_("Date created"), auto_now_add=True)
    comment = models.TextField(verbose_name=_('Comment'), max_length=2000)


    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)