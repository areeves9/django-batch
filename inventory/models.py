from django.db import models

# Create your models here.


class Manufacturer(models.Model):
    date_added = models.DateField(auto_now=False, auto_now_add=True)
    name = models.CharField(max_length=30, blank=False, null=False)
    rep = models.CharField(blank=True, null=True, max_length=148)
    rep_phone = models.CharField(max_length=16, blank=True, null=True)
    rep_email = models.EmailField(blank=False, null=False)
    support_phone = models.CharField(max_length=16, blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Vendor(models.Model):
    date_added = models.DateField(auto_now=False, auto_now_add=True)
    name = models.CharField(max_length=30, blank=False, null=False)
    rep = models.CharField(max_length=148, blank=True, null=True)
    rep_phone = models.CharField(max_length=16, blank=True, null=True)
    rep_email = models.EmailField(blank=False, null=False)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Unit(models.Model):
    name = models.CharField(blank=False, Null=False, max_length=30)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    date_added = models.DateField(auto_now=False, auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    manufacturer = models.ForeignKey(
        'Manufacturer',
        on_delete=models.SET_NULL
    )
    price = models.DecimalField(
        blank=True,
        null=True,
        max_digits=8,
        decimal_places=2
    )
    vendor = models.ForeignKey(
        'Vendor',
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Equipment(Item):
    READY = 'RDY'
    STANDBY = 'STDBY'
    EQUIPMENT_STATUS_CHOICES = [
        (READY, 'Ready'),
        (STANDBY, 'Standby')
    ]
    equipment_status = models.CharField(
        max_length=5,
        choices=EQUIPMENT_STATUS_CHOICES,
        default=STANDBY
    )
    equipment_id = models.CharField(
        blank=False,
        null=False,
        max_length=30,
        unique=True
    )
    equipment_model_number = models.CharField(
        blank=False,
        null=False,
        max_length=30
    )
    parent_equipment = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Example: for Diode Array Detector, select HPLC."
    )
    previous_calibration = models.DateField()
    next_calibration = models.DateField()
    serial_number = models.CharField(
        blank=False,
        null=False,
        unique=True,
        max_length=30
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Consumable(Item):
    cas_number = models.CharField(
        blank=True,
        null=True,
        max_length=20
    )
    formula = models.CharField(
        blank=True,
        null=True,
        max_length=50
    )
    parent_equipment = models.ForeignKey(
        'Equipment',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Example: for  analytical column, select HPLC."
    )
    lot_number = models.CharField(max_length=30)
    size = models.IntegerField(blank=False, null=False)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)
