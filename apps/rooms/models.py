from django.db import models

class RoomType (models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'room_types'

class Room (models.Model):
    room_number = models.IntegerField(unique=True)
    floor = models.IntegerField()
    status = models.CharField(
        max_length=11,
         choices= [
            ('active', 'active'),
            ('maintenance', 'maintenance'),
            ('inactive', 'inactive'), 
            ('reserved', 'reserved'), 
            ('busy', 'busy')
            ], default='active')

    room_type = models.ForeignKey(
        'RoomType',
        on_delete=models.RESTRICT,
        db_column='room_type_id')
    
    def __str__(self):
        return f"Room {self.room_number}"

    class Meta:
        managed = False
        db_table = 'rooms'

