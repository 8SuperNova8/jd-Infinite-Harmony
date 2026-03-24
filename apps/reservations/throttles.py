from rest_framework.throttling import AnonRateThrottle

class ReservationThrottle(AnonRateThrottle):
    scope = 'reservation'