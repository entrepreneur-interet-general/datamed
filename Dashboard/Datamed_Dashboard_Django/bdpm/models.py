from django.db import models

# Create your models here.


class Component(models.Model):
    name = models.CharField(max_length=1024)

    class Meta:
        verbose_name = "Composant"
        verbose_name_plural = "Composants"


class CompositionType(models.Model):
    name = models.CharField(max_length=512)

    class Meta:
        verbose_name = "Type de de composition"
        verbose_name_plural = "Types de compositions"


class Specialty(models.Model):
    name = models.CharField(max_length=1024)
    bdpm_id = models.IntegerField()
    cis_code = models.IntegerField()
    authorization_holder = models.CharField(max_length=512)
    composition_components = models.ManyToManyField(Component, through='ComponentRelation')
    composition_quantity = models.CharField(max_length=1024)
    composition_type = models.ForeignKey(CompositionType, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Spécialité"
        verbose_name_plural = "Specialités"


class ComponentRelation(models.Model):
    component = models.ForeignKey(Component, on_delete=models.PROTECT)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=512)


class SMR(models.Model):
    abstract = models.CharField(max_length=2048)
    advice = models.CharField(max_length=2048)
    reason = models.CharField(max_length=2048)
    value = models.CharField(max_length=2048)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Avis SMR"
        verbose_name_plural = "Avis SMR"


class ASMR(models.Model):
    abstract = models.CharField(max_length=2048)
    advice = models.CharField(max_length=2048)
    reason = models.CharField(max_length=2048)
    value = models.CharField(max_length=2048)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Avis ASMR"
        verbose_name_plural = "Avis ASMR"


class Presentations(models.Model):
    name = models.CharField(max_length=2048)
    cip_7 = models.IntegerField()
    cip_13 = models.IntegerField()
    marketing_start_date = models.DateField()
    marketing_stop_date = models.DateField()
    price = models.IntegerField()
    refund_rate = models.IntegerField()
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Présentation"
        verbose_name_plural = "Présentations"
