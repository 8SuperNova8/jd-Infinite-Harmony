
def reservation_value(room, check_in, check_out):
    nights =  (check_out - check_in).days
    price = room.room_type.base_price

    return nights * price