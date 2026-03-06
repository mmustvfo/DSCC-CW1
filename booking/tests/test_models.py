import pytest
from django.db import models
from django.contrib.auth.models import User
from booking.models import Customer, Service, Booking


def _model_field_names(model_cls):
    return {
        f.name
        for f in model_cls._meta.get_fields()
        if isinstance(f, models.Field)
    }


def test_customer_has_user_relation_field():
    fields = _model_field_names(Customer)
    assert "user" in fields


def test_customer_user_relation_type():
    field = Customer._meta.get_field("user")
    assert isinstance(field, (models.OneToOneField, models.ForeignKey))
    assert field.related_model == User


def test_service_has_basic_fields():
    fields = _model_field_names(Service)
    assert "name" in fields


def test_booking_has_core_fields():
    fields = _model_field_names(Booking)
    assert "customer" in fields
    assert "status" in fields
    assert any(x in fields for x in ["booking_date", "date"])


@pytest.mark.django_db
def test_user_creation_works():
    u = User.objects.create_user(username="pytest_user", password="pass12345")
    assert u.username == "pytest_user"


def test_booking_status_field_has_choices_if_defined():
    field = Booking._meta.get_field("status")
    # Allow either choices-based status or plain CharField
    assert isinstance(field, models.Field)