from datetime import datetime
from django.db import models
import pytz
from rest_framework import serializers

from app.common.mixins import BaseModel
from app.professionals.models import Professional


class Appointment(BaseModel):
    professional = models.ForeignKey(
        to=Professional, on_delete=models.CASCADE, null=False
    )
    scheduled_date = models.DateTimeField(null=False)
    subject = models.TextField(null=True, blank=False)

    class Meta:
        db_table = "tb_appointment"


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

    def create(self, validated_data):
        scheduled_date = validated_data["scheduled_date"]
        current_datetime = datetime.now(tz=pytz.timezone("America/Sao_Paulo"))

        if scheduled_date <= current_datetime:
            raise serializers.ValidationError("Scheduled date must be in the future.")

        appointment = Appointment.objects.filter(**validated_data).first()

        if appointment:
            raise serializers.ValidationError(
                "Appointment with the same professional and scheduled_date already exists."
            )

        appointment = Appointment.objects.create(**validated_data)

        return appointment

    def update(self, instance, validated_data):
        scheduled_date = validated_data.get("scheduled_date")
        if scheduled_date:
            current_datetime = datetime.now(tz=pytz.timezone("America/Sao_Paulo"))

            if scheduled_date <= current_datetime:
                raise serializers.ValidationError("Scheduled date must be in the future.")

            instance.scheduled_date = scheduled_date
            
        instance.subject = validated_data.get("subject")

        instance.save()
        return instance
