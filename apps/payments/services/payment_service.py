from rest_framework.exceptions import ValidationError
from apps.payments.models import Payment

def create_payment(reservation, amount, payment_method, status='completed'):
    if reservation.status != 'finished':
        raise ValidationError({'error': 'You cannot create a payment for a closed reservation'})
    
    if amount <= 0:
        raise ValidationError({'error': 'The payment amount is invalid'})
    
    if amount > reservation.balance:
        raise ValidationError({'error': 'The payment amount exceeds the reservation total'})
    
    #sobreescribo el create esto se hace por que valide errores desde service
    payment = Payment.objects.create(
        reservation=reservation,
        amount= amount,
        payment_method=payment_method,
        status= status
    )
    return payment
    