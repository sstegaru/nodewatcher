# Here we augment South migrations

from south import signals as south_signals

from nodewatcher.core.generator.cgm import base as cgm_base
from nodewatcher.utils import loader

from .. import models as antennas_models

_core_migrated = False


def install_antenna_fixtures(sender, **kwargs):
    """
    Installs fixtures for all registered internal antennas.
    """

    global _core_migrated
    if kwargs['app'] == 'core':
        _core_migrated = True

    if not _core_migrated:
        return

    # Ensure that all CGMs are registred
    loader.load_modules('cgm')

    for device in cgm_base.iterate_devices():
        for antenna in device.antennas:
            try:
                mdl = antennas_models.Antenna.objects.get(internal_for=device.identifier, internal_id=antenna.identifier)
            except antennas_models.Antenna.DoesNotExist:
                mdl = antennas_models.Antenna(internal_for=device.identifier, internal_id=antenna.identifier)

            # Update antenna model
            mdl.name = device.name
            mdl.manufacturer = device.manufacturer
            mdl.url = device.url
            mdl.polarization = antenna.polarization
            mdl.angle_horizontal = antenna.angle_horizontal
            mdl.angle_vertical = antenna.angle_vertical
            mdl.gain = antenna.gain
            mdl.save()

south_signals.post_migrate.connect(install_antenna_fixtures)
