from rest_framework import serializers
from .models import Brand, Instrument

class BrandSerializer(serializers.ModelSerializer):
    instruments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = ['id', 'name', 'serial_number', 'instruments']  # Expose the relevant fields

class InstrumentSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()  # Shows the brand's name
    brand_id = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), source="brand")

    class Meta:
        model = Instrument
        fields = [
            'id',
            'name',
            'code',
            'brand',
            'brand_id',
            'last_updated_at',
            'address',
            'lat_lng',
            'created_at',
            'installation_date',
        ]
