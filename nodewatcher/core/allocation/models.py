from django.contrib.contenttypes import generic, models as contenttypes_models
from django.db import models


class AddressAllocator(models.Model):
    """
    An abstract class defining an API for address allocator items.
    """

    class Meta:
        abstract = True

    def exactly_matches(self, other):
        """
        Returns true if this allocation request exactly matches the other. This
        should only return true if both requests share the same allocated
        resource.
        """

        raise NotImplementedError

    def is_satisfied(self):
        """
        Returns true if this allocation request is satisfied.
        """

        raise NotImplementedError

    def satisfy(self, obj):
        """
        Attempts to satisfy this allocation request by obtaining a new allocation
        for the specified object.

        :param obj: A valid Django model instance
        """

        raise NotImplementedError

    def satisfy_from(self, other):
        """
        Attempts to satisfy this request by taking resources from an existing one.

        :param other: AddressAllocator instance
        :return: True if request has been satisfied, False otherwise
        """

        raise NotImplementedError

    def free(self):
        """
        Frees this allocation.
        """

        raise NotImplementedError

    def get_routerid_family(self):
        """
        Returns the router-id family identifier for this allocator.
        """

        raise NotImplementedError

    def get_routerid(self):
        """
        Generates and returns a router-id from this allocation.
        """

        raise NotImplementedError


class PoolAllocationError(Exception):
    pass


class PoolBase(models.Model):
    """
    An abstract base class for all pool implementations.
    """

    class Meta:
        abstract = True

    parent = models.ForeignKey('self', null=True, related_name='children')

    # Bookkeeping for allocated pools
    allocation_content_type = models.ForeignKey(contenttypes_models.ContentType, null=True)
    allocation_object_id = models.CharField(max_length=50, null=True)
    allocation_content_object = generic.GenericForeignKey('allocation_content_type', 'allocation_object_id')
    allocation_timestamp = models.DateTimeField(null=True)

    @classmethod
    def modifies_pool(cls, f):
        def decorator(self, *args, **kwargs):
            # Lock our own instance
            locked_instance = self.__class__.objects.select_for_update().get(pk=self.pk)
            return f(locked_instance, *args, **kwargs)

        return decorator

    def top_level(self):
        """
        Returns the root of this pool tree.
        """

        if self.parent:
            return self.parent.top_level()

        return self

    def free(self):
        """
        Frees this allocated item and returns it to the parent pool.
        """

        raise NotImplementedError
