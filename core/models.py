from django.db import models
from django.utils.translation import gettext_lazy as _

from pik.core.models import BasePHistorical as PikBasePHistorical
from pik.core.models import SoftDeleted as PikSoftDeleted


class SoftDeleted(PikSoftDeleted):
    deleted = models.DateTimeField(
        editable=False, null=True, blank=True,
        db_index=True, verbose_name=_('deleted')
    )

    class Meta:
        abstract = True


class BasePHistorical(PikBasePHistorical):
    pass

    class Meta:
        abstract = True
