from django.contrib.contenttypes import models as contenttypes_models

from . import exceptions


class RegistryResolver(object):
    """
    Resolves registry identifiers in a hierarchical manner.
    """

    def __init__(self, regpoint, root, registry_id=None):
        """
        Class constructor.

        :param regpoint: Registration point
        :param root: Root model instance
        :param registry_id: Current registry identifier in the hierarchy
        """

        self._regpoint = regpoint
        self._root = root
        self._registry_id = registry_id

    def to_partial(self):
        """
        Formats the root's registry hierarchy to partial config format.
        """

        partial = {}
        for registry_id in self._regpoint.get_all_registry_ids():
            partial[registry_id] = [x.cast() for x in self.by_registry_id(registry_id, queryset=True)]

        return partial

    def by_registry_id(self, registry_id, create=None, queryset=False, onlyclass=None, **kwargs):
        """
        Resolves the registry hierarchy.
        """

        # Determine which class the root is using for configuration
        cfg, top_level = self._regpoint.get_top_level_queryset(self._root, registry_id)
        if onlyclass is not None:
            cfg = cfg.instance_of(onlyclass)
        if queryset:
            return cfg.all()

        if getattr(top_level.RegistryMeta, 'multiple', False):
            # Model supports multiple configuration options of this type
            if create is not None:
                if not issubclass(create, top_level):
                    raise TypeError("Not a valid registry item class for '{0}'!".format(registry_id))

                return create(root=self._root, **kwargs)
            else:
                return cfg.all()
        else:
            # Only a single configuration option is supported
            try:
                return cfg.all()[0]
            except (IndexError, top_level.DoesNotExist):
                if create is not None:
                    if not issubclass(create, top_level):
                        raise TypeError("Not a valid registry item class for '{0}'!".format(registry_id))

                    return create.objects.get_or_create(root=self._root, **kwargs)[0]
                else:
                    return None

    def __iter__(self):
        """
        Returns an iterator over all registry items that are present under
        this registration point.
        """

        for obj in self._root._meta.get_all_related_objects():
            if issubclass(obj.model, self._regpoint.item_base) and obj.field.name == 'root':
                for model in getattr(self._root, obj.field.rel.related_name).all():
                    yield model.cast()

    def __getattr__(self, key):
        """
        Constructs hierarchical names by simulating attribute access.
        """

        key = key if self._registry_id is None else '{0}.{1}'.format(self._registry_id, key)
        return RegistryResolver(self._regpoint, self._root, key)

    def __call__(self, **kwargs):
        """
        Resolves the registry hierarchy.
        """

        return self.by_registry_id(self._registry_id, **kwargs)


class RegistryAccessor(object):
    """
    A convenience class for accessing the registry via root models.
    """

    def __init__(self, regpoint):
        self.regpoint = regpoint

    def __get__(self, instance, owner):
        return RegistryResolver(self.regpoint, instance)
