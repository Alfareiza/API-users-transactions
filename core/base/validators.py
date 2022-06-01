from rest_framework import serializers


def validate_amount(value):
    if value["type"].lower() == "outflow" and value["amount"] > 0:
        raise serializers.ValidationError(
            {"type": "Outflow entries can not be positive."}
        )
    elif value["type"].lower() == "inflow" and value["amount"] < 0:
        raise serializers.ValidationError(
            {"type": "Inflow entries can not be negative ."}
        )


def validate_reference(value):
    if not value["reference"].isnumeric():
        raise serializers.ValidationError(
            {"reference": "The reference only must contain numbers."}
        )
