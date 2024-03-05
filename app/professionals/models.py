from django.db import models
from rest_framework import serializers
from app.common.mixins import BaseModel

from app.professionals.validators import *


MAX_LENGTH = 256
MAX_LENGTH_NUMERIC = 8


class Address(BaseModel):
    street = models.CharField(
        max_length=MAX_LENGTH,
        validators=[string_name_validator],
        null=False,
        blank=False,
    )
    number = models.CharField(
        max_length=MAX_LENGTH_NUMERIC,
        validators=[number_validator],
        null=False,
        blank=False,
    )
    neighborhood = models.CharField(
        max_length=MAX_LENGTH,
        validators=[string_name_validator],
        null=False,
        blank=False,
    )
    zipcode = models.CharField(
        max_length=MAX_LENGTH_NUMERIC,
        validators=[zipcode_validator],
        null=False,
        blank=False,
    )
    city = models.CharField(
        max_length=MAX_LENGTH,
        validators=[string_name_validator],
        null=False,
        blank=False,
    )
    state = models.CharField(
        max_length=MAX_LENGTH,
        validators=[string_name_validator],
        null=False,
        blank=False,
    )
    country = models.CharField(
        max_length=MAX_LENGTH,
        validators=[string_name_validator],
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "tb_address"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class Contact(BaseModel):
    mobile_number = models.CharField(
        max_length=MAX_LENGTH, validators=[phone_validator], null=True
    )
    comercial_number = models.CharField(
        max_length=MAX_LENGTH, validators=[phone_validator], null=True
    )
    email = models.CharField(
        max_length=MAX_LENGTH, validators=[email_validator], null=True
    )

    def clean(self):
        super().clean()

        if not any([self.mobile_number, self.comercial_number, self.email]):
            raise serializers.ValidationError(
                "At least one contact source must be provided."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "tb_contact"


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class Occupation(BaseModel):
    name = models.CharField(
        max_length=MAX_LENGTH,
        validators=[string_name_validator],
        null=True,
        blank=False,
    )

    class Meta:
        db_table = "tb_occupation"


class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields = "__all__"


class Professional(BaseModel):
    social_name = models.CharField(
        max_length=MAX_LENGTH,
        validators=[string_name_validator],
        null=True,
        blank=False,
    )
    full_name = models.CharField(
        max_length=MAX_LENGTH,
        validators=[string_name_validator],
        null=False,
        blank=False,
    )
    occupation = models.ForeignKey(to=Occupation, on_delete=models.PROTECT, null=False)
    address = models.ForeignKey(to=Address, on_delete=models.PROTECT, null=False)
    contact = models.ForeignKey(to=Contact, on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "tb_professional"
        unique_together = ("full_name", "occupation", "address", "contact")


class ProfessionalSerializer(serializers.ModelSerializer):
    occupation = OccupationSerializer()
    address = AddressSerializer()
    contact = ContactSerializer()

    class Meta:
        model = Professional
        fields = "__all__"

    def create(self, validated_data):
        occupation_data = validated_data.pop("occupation")
        address_data = validated_data.pop("address")
        contact_data = validated_data.pop("contact")

        occupation = Occupation.objects.filter(**occupation_data).first()
        address = Address.objects.filter(**address_data).first()
        contact = Contact.objects.filter(**contact_data).first()

        if not address:
            address = AddressSerializer(data=address_data)
            address.is_valid(raise_exception=True)
            address = address.save()

        if not contact:
            contact = ContactSerializer(data=contact_data)
            contact.is_valid(raise_exception=True)
            contact = contact.save()

        if not occupation:
            occupation = OccupationSerializer(data=occupation_data)
            occupation.is_valid(raise_exception=True)
            occupation = occupation.save()

        if validated_data.get("full_name"):
            validated_data["full_name"] = validated_data["full_name"].title()

        if validated_data.get("social_name"):
            validated_data["social_name"] = validated_data["social_name"].title()

        professional = Professional.objects.filter(
            full_name=validated_data["full_name"],
            address=address,
            contact=contact,
            occupation=occupation,
        ).first()
        if professional:
            raise serializers.ValidationError(
                "Professional with the same name, occupation, address, and contact already exists."
            )

        professional = Professional.objects.create(
            occupation=occupation, address=address, contact=contact, **validated_data
        )

        return professional

    def merge(self, instance, validated_data):
        occupation_data = validated_data.pop("occupation", {})
        address_data = validated_data.pop("address", {})
        contact_data = validated_data.pop("contact", {})

        occupation = OccupationSerializer(instance.address, data=occupation_data)
        if occupation.is_valid():
            occupation.save()

        address = AddressSerializer(instance.address, data=address_data, partial=True)
        if address.is_valid():
            address.save()

        contact = ContactSerializer(instance.contact, data=contact_data, partial=True)
        if contact.is_valid():
            contact.save()

        if validated_data.get("full_name"):
            validated_data["full_name"] = validated_data["full_name"].title()

        if validated_data.get("social_name"):
            validated_data["social_name"] = validated_data["social_name"].title()

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance

    def update(self, instance, validated_data):
        self.merge(instance, validated_data)

        instance.save()
        return instance
