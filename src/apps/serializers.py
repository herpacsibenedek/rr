
from django.db.models import Prefetch, Q
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from .models import (
    Auto,
    Partner,
    AutoPartnerConnection
)
from utils.mixins import NestedOrFlatSerializerMixin


class AutoPartnerConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoPartnerConnection
        fields = ['id',
                  'auto',
                  'partner',
                  'created_at',
                  'modify_at',
                  'deleted_at'
                  ]


class AutoSerializer(serializers.ModelSerializer):

    hozzarendelt_partnerek = serializers.SerializerMethodField()

    class Meta:
        model = Auto
        fields = ['id',
                  'average_fuel',
                  'delegation_starting',
                  'delegation_ending',
                  'driver',
                  'owner',
                  'type',
                  'hozzarendelt_partnerek',
                  'created_at',
                  'modify_at',
                  'deleted_at'
                  ]

    def get_hozzarendelt_partnerek(self, instance):
        instances = instance.hozzarendelt_partnerek.filter(deleted_at=None)
        if self.context.get("query", None) == 'nested':
            return PartnerSerializer(instances, many=True).data
        else:
            return [obj.id for obj in instances.all()]


class PartnerSerializer(serializers.ModelSerializer):

    hozzarendelt_autok = serializers.SerializerMethodField()

    class Meta:
        model = Partner
        fields = ['id',
                  'name',
                  'city',
                  'address',
                  'company_name',
                  'hozzarendelt_autok',
                  'created_at',
                  'modify_at',
                  'deleted_at'
                  ]

    def get_hozzarendelt_autok(self, instance):
        instances = instance.hozzarendelt_autok.filter(deleted_at=None)
        if self.context.get("query", None) == 'nested':
            return AutoSerializer(instances, many=True).data
        else:
            return [obj.id for obj in instances.all()]
