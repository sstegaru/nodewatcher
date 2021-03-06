from nodewatcher.core.generator.cgm import base as cgm_base, protocols as cgm_protocols, devices as cgm_devices


class AsusWL500GPremiumV1(cgm_devices.DeviceBase):
    """
    Asus WL500G Premium v1 device descriptor.
    """

    identifier = 'wl500gpv1'
    name = "WL500G Premium v1"
    manufacturer = "Asus"
    url = 'http://www.asus.com/'
    architecture = 'brcm47xx'
    radios = [
        cgm_devices.IntegratedRadio('wifi0', "Wifi0", [cgm_protocols.IEEE80211BG], [
            cgm_devices.AntennaConnector('a1', "Antenna0")
        ])
    ]
    switches = [
        cgm_devices.Switch(
            'sw0', "Switch0",
            ports=5,
            cpu_port=0,
            vlans=16,
        )
    ]
    ports = [
        cgm_devices.EthernetPort('wan0', "Wan0"),
        cgm_devices.EthernetPort('lan0', "Lan0")
    ]
    antennas = [
        # TODO: this information is probably not correct
        cgm_devices.InternalAntenna(
            identifier='a1',
            polarization='horizontal',
            angle_horizontal=360,
            angle_vertical=75,
            gain=2,
        )
    ]
    port_map = {
        'openwrt': {
            'wifi0': 'wlan0',
            'sw0': 'eth0',
            'wan0': 'eth1',
            'lan0': 'eth0',
        }
    }

    @cgm_devices.register_module()
    def network(node, cfg):
        """
        Network configuration CGM for Asus WL500G Premium v1.
        """

        pass

# Register the Asus WL500G Premium v1 device
cgm_base.register_device('openwrt', AsusWL500GPremiumV1)
