from nodewatcher.core.generator.cgm import base as cgm_base, protocols as cgm_protocols, routers as cgm_routers

class TPLinkWR741ND(cgm_routers.RouterBase):
    """
    TP-Link WR741ND device descriptor.
    """

    identifier = "wr741nd"
    name = "WR741ND"
    manufacturer = "TP-Link"
    url = "http://www.tp-link.com/"
    architecture = "ar71xx"
    radios = [
        cgm_routers.IntegratedRadio("wifi0", "Wifi0", [
            cgm_protocols.IEEE80211N(
                cgm_protocols.IEEE80211N.SHORT_GI_20,
                cgm_protocols.IEEE80211N.SHORT_GI_40,
                cgm_protocols.IEEE80211N.RX_STBC1,
                cgm_protocols.IEEE80211N.DSSS_CCK_40,
            )
        ], [
            cgm_routers.AntennaConnector("a1", "Antenna0")
        ])
    ]
    ports = [
        cgm_routers.EthernetPort("wan0", "Wan0"),
        cgm_routers.EthernetPort("lan0", "Lan0")
    ]
    antennas = [
        # TODO this information is probably not correct
        cgm_routers.InternalAntenna(
            identifier = "a1",
            polarization = "horizontal",
            angle_horizontal = 360,
            angle_vertical = 75,
            gain = 2
        )
    ]
    features = [
        cgm_routers.Features.MultipleSSID,
    ]
    port_map = {
        "openwrt": {
            "wifi0" : "radio0",
            "wan0"  : "eth1",
            "lan0"  : "eth0",
        }
    }
    profiles = {
        "openwrt": {
            "name" : "TLWR741",
            "files": [
                "openwrt-ar71xx-generic-tl-wr741nd-v1-squashfs-factory.bin",
                "openwrt-ar71xx-generic-tl-wr741nd-v2-squashfs-factory.bin",
                "openwrt-ar71xx-generic-tl-wr741nd-v4-squashfs-factory.bin"
            ]
        }
    }

# Register the TP-Link WR741ND router
cgm_base.register_router("openwrt", TPLinkWR741ND)