from django.db import models

from utils.mixins import TimeStampMixin


AUTO_HASZNALATI_TIPUS = (
    ("Magán", "Magán"),
    ("Céges", "Céges"),
)


class Partner(TimeStampMixin):
    """
    Partner:
    - id [number, Validator: required]
    - name [string, Validators: required, max length: 160]
    - city [string, Validator: required]
    - address [string, Validator: required]
    - company_name [string, Validator: required]
    - hozzárendelt autók [array]
    - created_at [number, Validator: required]
    - modify_at [number, Validator: required]
    - deleted_at [number|null]
    """
    name = models.CharField(
        max_length=160,
        null=False,
        blank=False
    )
    city = models.TextField(
        null=False,
        blank=False
    )
    address = models.TextField(
        null=False,
        blank=False
    )
    company_name = models.TextField(
        null=False,
        blank=False
    )
    hozzarendelt_autok = models.ManyToManyField(
        "Auto",
        through="AutoPartnerConnection"
    )

    def __str__(self):
        return self.name


class Auto(TimeStampMixin):
    """
    - id [number]
    - average_fuel [number]
    - delegation_starting [unix timestamp]
    - delegation_ending [unix timestamp]
    - driver [string]
    - owner [string]
    - type [string] (céges, magán)
    - hozzárendelt partnerek [array]
    - created_at [number, Validator: required]
    - modify_at [number, Validator: required]
    - deleted_at [number|null]
    """
    average_fuel = models.DecimalField(
        max_digits=3,
        decimal_places=1
    )
    delegation_starting = models.IntegerField(
        null=False,
        blank=False
    )
    delegation_ending = models.IntegerField(
        null=False,
        blank=False
    )
    driver = models.TextField(
        null=False,
        blank=False
    )
    owner = models.TextField(
        null=False,
        blank=False
    )
    type = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        choices=AUTO_HASZNALATI_TIPUS
    )
    hozzarendelt_partnerek = models.ManyToManyField(
        "Partner",
        through="AutoPartnerConnection"
    )

    def __str__(self):
        return f'{self.driver} - {self.type}'


class AutoPartnerConnection(TimeStampMixin):
    auto = models.ForeignKey(
        Auto,
        on_delete=models.CASCADE
    )
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('auto', 'partner',)
