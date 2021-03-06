from django.db import models

from nodewatcher.core.registry import registration


class Thing(models.Model):
    foo = models.CharField(max_length=30, null=True)
    bar = models.IntegerField(null=True)

registration.create_point(Thing, 'first')
registration.create_point(Thing, 'second')


class SimpleRegistryItem(registration.bases.ThingFirstRegistryItem):
    interesting = models.CharField(max_length=30, default='nope', null=True)

    class RegistryMeta:
        registry_id = 'foo.simple'

registration.point('thing.first').register_item(SimpleRegistryItem)


class ChildRegistryItem(SimpleRegistryItem):
    additional = models.IntegerField(null=True)

registration.point('thing.first').register_item(ChildRegistryItem)


class RelatedModel(models.Model):
    name = models.CharField(max_length=30)


class DoubleChildRegistryItem(ChildRegistryItem):
    another = models.IntegerField(null=True)
    related = models.ForeignKey(RelatedModel, null=True)

    class RegistryMeta(ChildRegistryItem.RegistryMeta):
        lookup_proxies = ['another']

registration.point('thing.first').register_item(DoubleChildRegistryItem)
