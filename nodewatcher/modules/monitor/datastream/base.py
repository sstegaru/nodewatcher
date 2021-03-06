import collections
import copy

from django.core import exceptions
from django.utils import datastructures


class StreamsMeta(type):
    def __new__(cls, classname, bases, attrs):
        """
        Constructs a new streams descriptor type.
        """

        if classname == "StreamsBase":
            return type.__new__(cls, classname, bases, attrs)

        # Create the actual class
        module = attrs.pop("__module__")
        new_class = type.__new__(cls, classname, bases, {"__module__": module})
        new_class._shared_fields = datastructures.SortedDict()

        from . import fields

        # Inherit all fields from parent classes
        for base in bases:
            if not hasattr(base, '_shared_fields'):
                continue

            for name, value in base._shared_fields.items():
                if not isinstance(value, fields.Field):
                    continue

                if name in new_class._shared_fields:
                    raise exceptions.ImproperlyConfigured("Duplicate field '%s' in stream descriptor '%s'!" % (name, classname))

                value = copy.deepcopy(value)
                new_class._shared_fields[name] = value

        # Add all fields to our streams descriptor
        for name, value in attrs.items():
            if not isinstance(value, fields.Field):
                setattr(new_class, name, value)
                continue

            if name in new_class._shared_fields:
                raise exceptions.ImproperlyConfigured("Duplicate field '%s' in stream descriptor '%s'!" % (name, classname))

            value.name = name
            new_class._shared_fields[name] = value

        return new_class


class StreamsBase(object):
    """
    A base class for all streams descriptors.
    """

    __metaclass__ = StreamsMeta

    def __init__(self, model):
        """
        Class constructor.

        :param model: Model class that contains the raw data
        """

        self._model = model

        # Make a local copy of all field descriptors for this model
        self._local_fields = datastructures.SortedDict()
        for name, field in self._shared_fields.iteritems():
            field = copy.deepcopy(field)
            self._local_fields[name] = field
            setattr(self, name, field)

    def insert_to_stream(self, stream):
        """
        Inserts all the fields specified in this descriptor to the datastream.

        :param stream: Instance of the datastream to insert into
        """

        for field in self._local_fields.values():
            field.to_stream(self, stream)

    def get_model(self):
        """
        Returns the underlying data model instance.
        """

        return self._model

    def get_field(self, name):
        """
        Returns a specific field descriptor.

        :param name: Field name
        :return: Field descriptor or None
        """

        return self._local_fields.get(name, None)

    def get_fields(self):
        """
        Returns a list of all field descriptors.
        """

        return self._local_fields.values()

    def get_stream_query_tags(self):
        """
        Returns a set of tags that uniquely identify this object.

        :return: A dictionary of tags that uniquely identify this object
        """

        raise NotImplementedError

    def get_stream_tags(self):
        """
        Returns the stream tags that should be included in every stream
        derived from this object.

        :return: A dictionary of tags to include
        """

        raise NotImplementedError

    def get_stream_highest_granularity(self):
        """
        Returns the highest granularity that should be used by default for
        all streams derived from this object.
        """

        raise NotImplementedError
