from django.db import models

class IBGEBase(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True



class Region(IBGEBase):
    acronym = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class State(IBGEBase):
    acronym = models.CharField(max_length=2)
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='states'
    )

    def __str__(self):
        return self.name
    

class Mesoregion(IBGEBase):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='mesoregions')

    def __str__(self):
        return self.name


class Microregion(IBGEBase):
    mesoregion = models.ForeignKey(
        Mesoregion,
        on_delete=models.CASCADE,
        related_name='microregions'
    )


class IntermediateRegion(IBGEBase):
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name='intermediate_regions'
    )


class ImmediateRegion(IBGEBase):
    intermediate_region = models.ForeignKey(
        IntermediateRegion,
        on_delete=models.CASCADE,
        related_name='immediate_regions'
    )


class Municipality(IBGEBase):
    microregion = models.ForeignKey(
        Microregion,
        on_delete=models.CASCADE,
        related_name='municipalities',
        null=True,
        blank=True
    )
    immediate_region = models.ForeignKey(
        ImmediateRegion,
        on_delete=models.CASCADE,
        related_name='municipalities',
        null=True,
        blank=True
    )


class District(IBGEBase):
    municipality = models.ForeignKey(
        Municipality,
        on_delete=models.CASCADE,
        related_name='districts'
    )