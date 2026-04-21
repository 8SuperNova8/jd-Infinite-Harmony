from django.db.models import Sum
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
        decimal_places=2
    )
    extra_charges = models.DecimalField( #este se adicionó
        max_digits=10,
        decimal_places=2,
        default=0
    )
    #-----------------------
    #Nota: property solo se puede usar dentro de la clase modelo
    @property #atributo calculado, no guardado. solo existe en el código cuando tú accedes al objeto.
    def total_real(self):
        return self.total_amount + self.extra_charges

    @property
    def total_paid(self):
        #suma todos los amount de payments de la reserva, y luego toma del diccionario el valor de total.
        paid = self.payments.aggregate(total=Sum('amount'))['total']
        return paid or 0 #devuelve 0 si paid es none

    @property
    def balance(self):
        return self.total_real - self.total_paid
    #-------------------------------------

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
