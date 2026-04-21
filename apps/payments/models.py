from django.db import models
from apps.reservations.models import Reservation


class Payment (models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=8,
        choices=[
            ('cash', 'cash'),
            ('card', 'card'),
            ('transfer', 'transfer'),
            ],)
    status = models.CharField(
        max_length=9,
        choices= [
            ('pending', 'pending'),
            ('completed', 'completed'),
            ('failed', 'failed'),
            ('refunded', 'refunded'),
            ],
            default= 'completed')
    
    reservation = models.ForeignKey(
        Reservation,
        on_delete= models.RESTRICT,
        db_column= 'reservation_id',
        related_name='payments' #permite q reserva haga consultas a payments
    )
    
    def __str__(self):
        return f"Reserva:{self.reservation} amount:{self.amount} status:{self.status}"

    class Meta:
        managed = False
        db_table = 'payments'
