
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Warehouse(models.Model):

    name = models.CharField(
        _('Warehouse name'),
        max_length=255,
        unique=True,
        db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Warehouse')
        verbose_name_plural = _('Warehouses')


class WarehouseField(models.ForeignKey):

    def __init__(
            self,
            to=Warehouse,
            on_delete=models.SET_NULL,
            verbose_name=_('Warehouse'),
            blank=True,
            null=True,
            *args, **kwargs):
        super().__init__(
            to=to,
            on_delete=on_delete,
            verbose_name=verbose_name,
            blank=blank,
            null=null,
            *args, **kwargs)
