from django.core.mail import send_mail

#configuración para enviar correo despues de creada la reserva
def send_reservation_mail(reservation):
    send_mail(
        subject='Confirmación de Reserva',
        message=f"""
            Hola {reservation.guest_name},
            Tu reserva fue creada con éxito.

            check-in: {reservation.check_in} Hora: 3:00pm
            check-out: {reservation.check_out} Hora: 12:00pm
            habitación: {reservation.room.room_number}

            puedes ver tu reserva aqui:
            http://127.0.0.1:8000/api/public/reservations/{reservation.token}/

            """,
        from_email='vssombreange@gmail.com',
        recipient_list=[reservation.guest_email],
        fail_silently=False,
    )