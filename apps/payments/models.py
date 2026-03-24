# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from apps.reservations.models import Reservation


class Payment (models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    payment_method = models.CharField(
        max_length=8,
        choices=[
            ('cash', 'cash'),
            ('card', 'card'),
            ('transfer', 'transfer'),
            ],)
    payment_type = models.CharField(
        max_length=7,
        choices= [
            ('deposit', 'deposit'),
            ('final', 'final'),
            ('penalty', 'penalty'),
            ],)
    status = models.CharField(
        max_length=9,
        choices= [
            ('pending', 'pending'),
            ('completed', 'completed'),
            ('failed', 'failed'),
            ('refunded', 'refunded'),
            ],
            default= 'pending')
    card_last_four = models.CharField(max_length=4, blank=True, null=True)

    reservation = models.ForeignKey(
        Reservation,
        on_delete= models.RESTRICT,
        db_column= 'reservation_id')
    
    def __str__(self):
        return f"Reserva:{self.reservation} amount:{self.amount} status:{self.status}"

    class Meta:
        managed = False
        db_table = 'payments'
