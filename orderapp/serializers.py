from rest_framework import serializers

class SimpleItemOrderSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True, required=False)
    order_id = serializers.UUIDField(read_only=True, required=False)
    good_id = serializers.UUIDField(read_only=True, required=False)
    quantity = serializers.DecimalField(max_digits=15, decimal_places=3)
    price = serializers.DecimalField(max_digits=15, decimal_places=2)
    summ = serializers.DecimalField(max_digits=15, decimal_places=2)

class SimpleOrderSerializer(serializers.Serializer):
    number = serializers.IntegerField(read_only=True, required=False)
    date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True, required=False)
    first_name = serializers.CharField(max_length=30, read_only=True, required=False)
    items = SimpleItemOrderSerializer(many=True, required=False)
    comment = serializers.CharField(max_length=None, required=False, allow_blank=True, allow_null=True)
    orderType = serializers.CharField(max_length=1, required=False)
    name = serializers.CharField(max_length=255, required=False)
    phone = serializers.CharField(max_length=20, required=False)
    email = serializers.EmailField(max_length=255, required=False, allow_blank=True, allow_null=True)
    address = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    cookTime = serializers.TimeField(format="H%:s%", required=False)
    pickupType = serializers.CharField(max_length=1, required=False) 