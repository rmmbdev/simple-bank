from __future__ import (
    annotations,
)

from datetime import (
    datetime,
)
from uuid import (
    uuid4,
)

from django.contrib.auth.models import (
    AbstractUser,
)
from django.db.models import (
    CharField,
    DateTimeField,
    EmailField,
    Model,
    TextChoices,
    UUIDField,
)
from django.utils import (
    timezone,
)


class BaseAbstractModel(Model):
    id: UUIDField = UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        db_index=True,
    )
    created_at: DateTimeField[datetime] = DateTimeField(
        default=timezone.now,
        db_index=True,
    )
    modified_at: DateTimeField[datetime] = DateTimeField(
        auto_now=True,
        db_index=True,
    )

    class Meta:
        abstract = True


class User(AbstractUser):
    id: UUIDField[str] = UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        db_index=True,
    )
    username: CharField[str] = CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
    )
