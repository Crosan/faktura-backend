from rest_framework import serializers
from backend.backend.models import ReceiptFile

class ReceiptFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptFile
        fields = "__all__"