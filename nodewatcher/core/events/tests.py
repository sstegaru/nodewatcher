from django.conf import settings
from django.utils import unittest
from django import test as django_test

from . import base, exceptions, events
from .pool import pool


class TestEventSink(base.EventSink):
    def __init__(self, **kwargs):
        super(TestEventSink, self).__init__(**kwargs)
        self.events = []

    def deliver(self, event):
        self.events.append(event)


class TestEventFilter(base.EventFilter):
    def __init__(self, pass_everything=False, **kwargs):
        super(TestEventFilter, self).__init__(**kwargs)

        # An argument for testing if arguments work
        self.pass_everything = pass_everything

    def filter(self, event):
        if self.pass_everything:
            return True

        if getattr(event, 'c', None) is True:
            return False

        return True


class TestNodeEvent(events.NodeEventRecord):
    foo = events.CharAttribute()
    bar = events.CharAttribute()

    def __init__(self, foo, bar):
        super(TestNodeEvent, self).__init__(
            None,
            events.NodeEventRecord.SEVERITY_INFO,
            "Test event",
            foo=foo,
            bar=bar
        )


class TestInvalidSubclass(object):
    pass


class EventsTestCase(unittest.TestCase):
    def setUp(self):
        # Unregister any other sinks
        self._previous_sinks = [sink.__class__ for sink in pool.get_all_sinks()]
        pool.unregister(self._previous_sinks)
        # Setup a test sink
        pool.register(TestEventSink)
        pool.get_sink('TestEventSink').add_filter(TestEventFilter)
        # Fake discovery
        pool._discovered = True

    def tearDown(self):
        pool.unregister(TestEventSink)
        # Register the previous sinks back
        for sink in self._previous_sinks:
            pool.register(sink)

    def test_event_processing(self):
        # Check basic event propagation
        base.EventRecord(a=1, b=2, message="Hello event world!").post()
        base.EventRecord(a=3, b=4, message="Hello event world!").post()
        base.EventRecord(a=5, b=6, c=True, message="Hello event world!").post()
        base.EventRecord(a=7, b=8, message="Hello event world!").post()

        sink = pool.get_sink('TestEventSink')
        self.assertEqual(len(sink.events), 3)
        for x in sink.events:
            self.assertEqual(x.message, "Hello event world!")
        self.assertEqual(sink.events[0].a, 1)
        self.assertEqual(sink.events[0].b, 2)
        self.assertEqual(sink.events[1].a, 3)
        self.assertEqual(sink.events[1].b, 4)
        self.assertEqual(sink.events[2].a, 7)
        self.assertEqual(sink.events[2].b, 8)

        # Check that sinks can be disabled and enabled
        sink.set_enabled(False)
        base.EventRecord(a=1, b=2, message="Hello event world!").post()
        self.assertEqual(len(sink.events), 3)

        sink.set_enabled(True)
        base.EventRecord(a=1, b=2, message="Hello event world!").post()
        self.assertEqual(len(sink.events), 4)

        # Check that filters can be removed
        sink.remove_filter('TestEventFilter')
        base.EventRecord(a=1, b=2, c=True, message="Hello event world!").post()
        self.assertEqual(len(sink.events), 5)

        # Check that we can't override the 'disable' argument
        with self.assertRaises(exceptions.FilterArgumentReserved):
            sink.add_filter(TestEventFilter, disable=True)

        # Check that filter arguments can be overriden
        sink.add_filter(TestEventFilter, pass_everything=True)
        base.EventRecord(a=1, b=2, c=True, message="Hello event world!").post()
        self.assertEqual(len(sink.events), 6)

    def test_exceptions(self):
        with self.assertRaises(exceptions.InvalidEventSink):
            pool.register(TestInvalidSubclass)

        with self.assertRaises(exceptions.InvalidEventFilter):
            pool.get_sink('TestEventSink').add_filter(TestEventFilter())

        with self.assertRaises(exceptions.InvalidEventFilter):
            pool.get_sink('TestEventSink').add_filter(TestInvalidSubclass)

        with self.assertRaises(exceptions.EventSinkAlreadyRegistered):
            pool.register(TestEventSink)

        with self.assertRaises(exceptions.EventSinkNotRegistered):
            pool.get_sink('TestUnregisteredSink')

        with self.assertRaises(exceptions.EventFilterAlreadyAttached):
            pool.get_sink('TestEventSink').add_filter(TestEventFilter)

        with self.assertRaises(exceptions.EventFilterNotFound):
            pool.get_sink('TestEventSink').remove_filter('TestUnattachedFilter')

    def test_node_events(self):
        self.assertEqual([a.name for a in TestNodeEvent.get_attributes()], ['foo', 'bar'])
        self.assertEqual(TestNodeEvent.get_attribute('foo').name, 'foo')
        self.assertEqual(TestNodeEvent.get_attribute('bar').name, 'bar')
        with self.assertRaises(KeyError):
            TestNodeEvent.get_attribute('does_not_exist')


class EventsSettingsTestCase(django_test.TestCase):
    def setUp(self):
        # Unregister any other sinks
        self._previous_sinks = [sink.__class__ for sink in pool.get_all_sinks()]
        pool.unregister(self._previous_sinks)
        # Fake discovery
        pool._discovered = True

    def tearDown(self):
        # Register the previous sinks back
        for sink in self._previous_sinks:
            pool.register(sink)

    def test_settings(self):
        # Test disabled sink via settings
        with self.settings(EVENT_SINKS={
            'TestEventSink': {
                'disable': True
            }
        }):
            pool.register(TestEventSink)
            try:
                base.EventRecord(a=1, b=2, message="Hello event world!").post()
                sink = pool.get_sink('TestEventSink')
                self.assertEqual(len(sink.events), 0)
            finally:
                pool.unregister(TestEventSink)

        # Test settings argument override
        with self.settings(EVENT_SINKS={
            'TestEventSink': {
                'filters': {
                    'TestEventFilter': {
                        'pass_everything': False
                    }
                }
            }
        }):
            pool.register(TestEventSink)
            pool.get_sink('TestEventSink').add_filter(TestEventFilter, pass_everything=True)
            try:
                base.EventRecord(a=1, b=2, c=True, message="Hello event world!").post()
                sink = pool.get_sink('TestEventSink')
                self.assertEqual(len(sink.events), 1)
            finally:
                pool.unregister(TestEventSink)

        # Test disabled filter via settings
        with self.settings(EVENT_SINKS={
            'TestEventSink': {
                'filters': {
                    'TestEventFilter': {
                        'disable': True
                    }
                }
            }
        }):
            pool.register(TestEventSink)
            pool.get_sink('TestEventSink').add_filter(TestEventFilter)
            try:
                base.EventRecord(a=1, b=2, c=True, message="Hello event world!").post()
                sink = pool.get_sink('TestEventSink')
                self.assertEqual(len(sink.events), 1)
            finally:
                pool.unregister(TestEventSink)
