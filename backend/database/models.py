from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True) 
    serial_number = models.CharField(max_length=100, unique=True,)

    class Meta:
        db_table = 'brands'  # Custom table name

    def __str__(self):
        return self.name


class Instrument(models.Model):
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="instruments"
    )
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    last_updated_at = models.DateTimeField() 
    address = models.TextField()
    lat_lng = models.CharField(max_length=255, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    installation_date = models.DateField()

    class Meta:
        db_table = 'instruments'  # Custom table name

    def __str__(self):
        return f"{self.name} - {self.code}"
