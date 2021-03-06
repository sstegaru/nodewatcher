# pylint: skip-file

from nodewatcher.core.registry.rules.scope import *
from nodewatcher.core.generator.cgm.predicates import *

# Variables
project = value("core.project#project.name")
device = device_descriptor("core.general#platform", "core.general#router")

first_radio = dict(_item="core.interfaces", _cls="WifiRadioDeviceConfig", _index=0)

# Rules
rule(count(device.radios) == 1,
    remove("core.interfaces", "WifiRadioDeviceConfig"),
    append("core.interfaces", "WifiRadioDeviceConfig", wifi_radio=device.radios[0].identifier),

    rule(contains(device.features, "multiple_ssid"),
        remove("core.interfaces", "WifiInterfaceConfig", first_radio),
        append("core.interfaces", "WifiInterfaceConfig", first_radio, mode="ap", essid="open.wlan-si.net"),
        append("core.interfaces", "WifiInterfaceConfig", first_radio, mode="mesh", bssid="02:CA:FF:EE:BA:BE", essid="mesh.wlan-si.net", routing_protocol="olsr"),
    ),

    rule(~contains(device.features, "multiple_ssid"),
        remove("core.interfaces", "WifiInterfaceConfig", first_radio),
        append("core.interfaces", "WifiInterfaceConfig", first_radio, mode="mesh", bssid="02:CA:FF:EE:BA:BE", essid="open.wlan-si.net", routing_protocol="olsr"),
    )
)

rule(count(device.radios) == 0,
    remove("core.interfaces", "WifiRadioDeviceConfig")
)

# Project defaults for all projects that don't configure anything
rule(changed("core.project#project.name"),
    rule(contains(device.features, "multiple_ssid"),
        assign("core.interfaces", "WifiInterfaceConfig", first_radio, mode="ap", _set=dict(essid="open.wlan-si.net")),
        assign("core.interfaces", "WifiInterfaceConfig", first_radio, mode="mesh", _set=dict(essid="mesh.wlan-si.net"))
    ),
    rule(~contains(device.features, "multiple_ssid"),
        assign("core.interfaces", "WifiInterfaceConfig", first_radio, mode="mesh", _set=dict(essid="open.wlan-si.net"))
    )
)

# Per-project rules
rule(project == "Ljubljana",
    rule(contains(device.features, "multiple_ssid"),
        assign("core.interfaces", "WifiInterfaceConfig", first_radio, mode="ap", _set=dict(essid="open.wlan-lj.net")),
        assign("core.interfaces", "WifiInterfaceConfig", first_radio, mode="mesh", _set=dict(essid="mesh.wlan-lj.net"))
    ),
    rule(~contains(device.features, "multiple_ssid"),
        assign("core.interfaces", "WifiInterfaceConfig", first_radio, mode="mesh", _set=dict(essid="open.wlan-lj.net"))
    )
)
