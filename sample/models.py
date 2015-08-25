from django.db import models


class Human(models.Model):

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Human"
        verbose_name_plural = "Humans"

    def __str__(self):
        return self.name


class Pet(models.Model):

    name = models.CharField(max_length=100)
    ownner = models.ForeignKey(Human, related_name='pets')

    class Meta:
        verbose_name = "Pet"
        verbose_name_plural = "Pets"

    def __str__(self):
        pass
