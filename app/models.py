from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import PermissionDenied

from EpicEvent import settings

MANAGEMENT = "MANAGEMENT"
SALES = "SALES"
SUPPORT = "SUPPORT"

TEAM_LIMIT = 3


class Team(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if Team.objects.all().count() <= TEAM_LIMIT or self.pk is not None:
            raise PermissionDenied(
                detail="You are not permitted to create or edit teams."
            )

    def delete(self, using=None, keep_parents=False):
        raise PermissionDenied(detail="You are not permitted to delete teams.")


class User(AbstractUser):
    phone = models.CharField(max_length=12, blank=True, null=True)

    team = models.ForeignKey(Team, on_delete=models.PROTECT, default=1)

    def __str__(self):
        return f"{self.username} ({self.team.name})"

    def save(self, *args, **kwargs):
        if self.team.name == MANAGEMENT:
            self.is_superuser = True
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = False

        user = super(User, self)
        user.save()

        return user


class Client(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True, null=True)
    mobile = models.CharField(max_length=30, blank=True, null=True)
    company_name = models.CharField(max_length=250, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"team_id": 2},
    )
    status = models.BooleanField(default=False, verbose_name="Converted")

    def __str__(self):
        if self.status is False:
            stat = "PROSPECT"
        else:
            stat = "CONVERTED"
        return f"Client #{self.id} : {self.last_name}, {self.first_name} ({stat})"


class Contract(models.Model):
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"team_id":2},
    )
    client = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE,
        limit_choices_to={"status": True},
        related_name="contract",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False, verbose_name="Signed")
    amount = models.FloatField()
    payment_due = models.DateField()

    def __str__(self):
        name = f"{self.client.last_name}, {self.client.first_name}"
        if self.status is False:
            stat = "NOT SIGNED"
        else:
            stat = "SIGNED"

        return f"Contract #{self.id} : {name} ({stat})"


class Event(models.Model):
    contract = models.OneToOneField(
        to=Contract,
        on_delete=models.CASCADE,
        limit_choices_to={"status": True},
        related_name="event",
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"team_id": 3},
    )
    event_status = models.BooleanField(default=False, verbose_name="Completed")
    attendees = models.PositiveIntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        name = f"{self.contract.client.last_name}, {self.contract.client.first_name}"
        date = self.event_date.strftime("%Y-%m-%d")
        if self.event_status is False:
            stat = "UPCOMING"
        else:
            stat = "COMPLETED"

        return f"Event #{self.id} : {name} | Date : {date} ({stat})"