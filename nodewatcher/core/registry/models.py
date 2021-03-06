from django import forms

import polymorphic


class RegistryItemBase(polymorphic.PolymorphicModel):
    """
    An abstract registry configuration item.
    """

    root = None
    _registry_regpoint = None

    class RegistryMeta:
        registry_id = None

    class Meta:
        abstract = True
        ordering = ['id']

    @classmethod
    def get_form(cls):
        """
        Returns the form used for this model.
        """

        form = getattr(cls, '_forms', {}).get(cls, None)

        if form is None:
            class DefaultRegistryItemForm(forms.ModelForm):
                class Meta:
                    model = cls

            form = DefaultRegistryItemForm

        return form

    @classmethod
    def get_registry_lookup_chain(cls):
        """
        Returns a query filter "chain" that can be used for performing root lookups with
        fields that are part of some registry object.
        """

        if cls.__base__ == cls._registry_regpoint.item_base:
            return cls._registry_regpoint.namespace + '_' + cls._meta.app_label + '_' + cls._meta.module_name
        else:
            for base in cls.__bases__:
                if hasattr(base, 'get_registry_lookup_chain'):
                    return base.get_registry_lookup_chain() + '__' + cls._meta.module_name

    @classmethod
    def get_registry_id(cls):
        """
        Returns the item's registry identifier.
        """

        return cls.RegistryMeta.registry_id

    @classmethod
    def get_registry_toplevel(cls):
        """
        Returns the toplevel item for its registry id.
        """

        return cls._registry_regpoint.get_top_level_class(cls.get_registry_id())

    @classmethod
    def can_add(cls, user):
        """
        Returns True if the user has permissions to add this registry item.
        """

        return user.has_perm(
            "%(app_label)s.add_%(module_name)s" % {
                "app_label": cls._meta.app_label,
                "module_name": cls._meta.module_name,
            }
        )

    @classmethod
    def has_registry_multiple(cls):
        """
        Returns true if the item's registry id can contain multiple items.
        """

        return getattr(cls.RegistryMeta, 'multiple', False)

    @classmethod
    def is_registry_toplevel(cls):
        """
        Returns true if the item is a toplevel item for its registry id.
        """

        return cls.__base__ == cls._registry_regpoint.item_base

    def cast(self):
        """
        Casts this registry item into the proper downwards type.
        """

        # TODO: The cast method should not be needed anymore and should be removed
        return self.get_real_instance()

    def save(self, *args, **kwargs):
        """
        Sets up and saves the configuration item.
        """

        super(RegistryItemBase, self).save(*args, **kwargs)

        # If only one configuration instance should be allowed, we
        # should delete existing ones
        if not getattr(self.RegistryMeta, 'multiple', False) and self.root:
            cfg, _ = self._registry_regpoint.get_top_level_queryset(self.root, self.RegistryMeta.registry_id)
            cfg.exclude(pk=self.pk).delete()
