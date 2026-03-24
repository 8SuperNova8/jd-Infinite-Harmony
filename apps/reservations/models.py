# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from apps.rooms.models import Room
import uuid


class Reservation (models.Model):
    check_in = models.DateField()
    check_out = models.DateField()
    reservation_date = models.DateTimeField(auto_now_add=True) 
    status = models.CharField(
        max_length=10,
        choices= [
            ('confirmed', 'Confirmed'),
            ('checked_in', 'Checked In'),
            ('cancelled', 'Cancelled'),
            ('no_show', 'No Show'),
            ('finished', 'Finished'),
            ],
        default= 'confirmed')
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2)
    guest_name = models.CharField(max_length=100)
    guest_email = models.CharField(max_length=100)
    guest_phone = models.CharField(max_length=20)
    guest_document = models.CharField(max_length=50)
    #para el token de reserva 
    token = models.UUIDField(
        default=uuid.uuid4, #genera automaticamente token aleatorio seguro
        editable=False, #evita que se modifique manualmente
        unique=True
    )
    '''
    card_last_four = models.CharField(max_length=4)
    card_holder_name = models.CharField(max_length=100)
    card_brand = models.CharField(max_length=20)
    tokenization_id = models.CharField(max_length=100)
    authorization_code = models.CharField(max_length=100)
    '''

    room = models.ForeignKey(
        Room,
        on_delete = models.RESTRICT,
        db_column='room_id')
    
    def __str__(self):
        return f"{self.guest_name} = Hab: {self.room.room_number} (CheckIn {self.check_in} - CheckOut {self.check_out})"

    class Meta:
        managed = False
        db_table = 'reservations'
        unique_together = (('room', 'check_in', 'check_out'),)
