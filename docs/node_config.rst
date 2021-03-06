.. _registry-node-config-schema:

Node Configuration Registry Schema
==================================

The following table represents the node configuration registry schema that is bundled with core nodewatcher modules. This schema is used to configure various per-node attributes and is used by the firmware image generation module (see :ref:`firmware-image-generation`) to configure firmware images for diffrent platforms.

+-------------------------+------------+-------+------------------+----------------------------------+
| Registry ID             | Multiple   | Class | Field            | Type                             |
+=========================+============+=======+==================+==================================+
| core.general            | no         |                                                             |
+-------------------------+------------+-------------------------------------------------------------+
|                                      || GeneralConfig                                              |
|                                      || *provided by:* ``core``                                    |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | name             | string                           |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      || CgmGeneralConfig(GeneralConfig)                            |
|                                      || *provided by:* ``core.generator.cgm``                      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | router           | | registered choice              |
|                                      |       |                  | | (see :ref:`device-descriptors`)|
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | platform         | | registered choice              |
|                                      |       |                  | | (see :ref:`cgm-platforms`)     |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | version          | foreign key                      |
+-------------------------+------------+-------+------------------+----------------------------------+
| core.type               | no         |                                                             |
+-------------------------+------------+-------------------------------------------------------------+
|                                      || TypeConfig                                                 |
|                                      || *provided by:* ``modules.administration.types``            |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | type             | registered choice                |
+-------------------------+------------+-------+------------------+----------------------------------+
| core.project            | no         |                                                             |
+-------------------------+------------+-------------------------------------------------------------+
|                                      || ProjectConfig                                              |
|                                      || *provided by:* ``modules.administration.projects``         |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | project          | foreign key                      |
+-------------------------+------------+-------+------------------+----------------------------------+
| core.description        | no         |                                                             |
+-------------------------+------------+-------------------------------------------------------------+
|                                      || DescriptionConfig                                          |
|                                      || *provided by:* ``modules.administration.description``      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | notes            | text                             |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | url              | url                              |
+-------------------------+------------+-------+------------------+----------------------------------+
| core.location           | no         |                                                             |
+-------------------------+------------+-------------------------------------------------------------+
|                                      || LocationConfig                                             |
|                                      || *provided by:* ``modules.administration.location``         |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | address          | string                           |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | city             | string                           |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | country          | country                          |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | timezone         | timezone                         |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | geolocation      | geospatial                       |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | altitude         | float                            |
+-------------------------+------------+-------+------------------+----------------------------------+
| core.routerid           | yes        |                                                             |
+-------------------------+------------+-------------------------------------------------------------+
|                                      || RouterIdConfig                                             |
|                                      || *provided by:* ``core``                                    |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | family           | registered choice                |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | router_id        | string                           |
+-------------------------+------------+-------+------------------+----------------------------------+
| core.authentication     | yes        |                                                             |
+-------------------------+------------+-------------------------------------------------------------+
|                                      || *AuthenticationConfig (hidden parent)*                     |
|                                      || *provided by:* ``core.generator.cgm``                      |
+--------------------------------------+-------------------------------------------------------------+
|                                      || PasswordAuthenticationConfig(AuthenticationConfig)         |
|                                      || *provided by:* ``core.generator.cgm``                      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | password         | string                           |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      || PublicKeyAuthenticationConfig(AuthenticationConfig)        |
|                                      || *provided by:* ``modules.authentication.public_key``       |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | public_key       | string                           |
+-------------------------+------------+-------+------------------+----------------------------------+
| core.roles              | yes/static |                                                             |
+-------------------------+------------+-------------------------------------------------------------+
|                                      || *RoleConfig (hidden parent)*                               |
|                                      || *provided by:* ``modules.administration.roles``            |
+--------------------------------------+-------------------------------------------------------------+
|                                      || SystemRoleConfig(RoleConfig)                               |
|                                      || *provided by:* ``modules.administration.roles``            |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | system           | boolean                          |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      || BorderRouterRoleConfig(RoleConfig)                         |
|                                      || *provided by:* ``modules.administration.roles``            |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | border_router    | boolean                          |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      || VpnServerRoleConfig(RoleConfig)                            |
|                                      || *provided by:* ``modules.administration.roles``            |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | vpn_server       | boolean                          |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      || RedundancyRequiredRoleConfig(RoleConfig)                   |
|                                      || *provided by:* ``modules.administration.roles``            |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | redundancy       | boolean                          |
+-------------------------+------------+-------+------------------+----------------------------------+
| core.interfaces         | yes        |                                                             |
+-------------------------+------------+-------------------------------------------------------------+
|                                      || InterfaceConfig                                            |
|                                      || *provided by:* ``core.generator.cgm``                      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | enabled          | boolean                          |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      || EthernetInterfaceConfig(InterfaceConfig)                   |
|                                      || *provided by:* ``core.generator.cgm``                      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | eth_port         | | registered choice              |
|                                      |       |                  | | *(depends on router model)*    |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | uplink           | boolean                          |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      || WifiRadioDeviceConfig(InterfaceConfig)                     |
|                                      || *provided by:* ``core.generator.cgm``                      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | wifi_radio       | | registered choice              |
|                                      |       |                  | | *(depends on router model)*    |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | protocol         | | registered choice              |
|                                      |       |                  | | *(depends on wifi radio)*      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | channel          | | registered choice              |
|                                      |       |                  | | *(depends on protocol)*        |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | channel_width    | | registered choice              |
|                                      |       |                  | | *(depends on protocol)*        |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | bitrate          | | registered choice              |
|                                      |       |                  | | *(depends on protocol)*        |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | ack_distance     | integer                          |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | rts_threshold    | integer                          |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | frag_threshold   | integer                          |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      || WifiInterfaceConfig(InterfaceConfig, RoutableInterface)    |
|                                      || *provided by:* ``core.generator.cgm``                      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | device           | foreign key                      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | mode             | registered choice                |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | essid            | string                           |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | bssid            | mac string                       |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      || VpnInterfaceConfig(InterfaceConfig, RoutableInterface)     |
|                                      || *provided by:* ``core.generator.cgm``                      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | protocol         | registered choice                |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | mac              | mac string                       |
+-------------------------+------------+-------+------------------+----------------------------------+
| core.basic_addressing   | yes        |                                                             |
+-------------------------+------------+-------------------------------------------------------------+
|                                      || BasicAddressingConfig(IpAddressAllocator)                  |
|                                      || *provided by:* ``modules.administration.addressing``       |
|                                      ||                                                            |
|                                      ||                                                            |
|                                      | **Note:** *Only available if* ``core.generator.cgm``        |
|                                      | *module is not enabled. Otherwise this registry item is     |
|                                      | replaced by core.interfaces.network per-interface           |
|                                      | allocators.*                                                |
+-------------------------+------------+-------------------------------------------------------------+
| core.interfaces.network | yes        |                                                             |
+-------------------------+------------+-------------------------------------------------------------+
|                                      || NetworkConfig                                              |
|                                      || *provided by:* ``core.generator.cgm``                      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | enabled          | boolean                          |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | interface        | foreign key                      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | description      | string                           |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      || StaticNetworkConfig(NetworkConfig)                         |
|                                      || *provided by:* ``core.generator.cgm``                      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | address          | ip address                       |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | gateway          | ip address                       |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      || AllocatedNetworkConfig(NetworkConfig, IpAddressAllocator)  |
|                                      || *provided by:* ``core.generator.cgm``                      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | routing_announce | registered choice                |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      || DHCPNetworkConfig(NetworkConfig)                           |
|                                      || *provided by:* ``core.generator.cgm``                      |
+--------------------------------------+-------------------------------------------------------------+
|                                      || PPPoENetworkConfig(NetworkConfig)                          |
|                                      || *provided by:* ``core.generator.cgm``                      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | username         | string                           |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | password         | string                           |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      || VPNNetworkConfig(NetworkConfig)                            |
|                                      || *provided by:* ``core.generator.cgm``                      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | address          | ip address                       |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | port             | integer                          |
+-------------------------+------------+-------+------------------+----------------------------------+
| core.interfaces.limits  | yes        |                                                             |
+-------------------------+------------+-------------------------------------------------------------+
|                                      || InterfaceLimitConfig                                       |
|                                      || *provided by:* ``core.generator.cgm``                      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | enabled          | boolean                          |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | interface        | foreign key                      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      || ThroughputInterfaceLimitConfig(InterfaceLimitConfig)       |
|                                      || *provided by:* ``core.generator.cgm``                      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | limit_in         | registered choice                |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | limit_out        | registered choice                |
+-------------------------+------------+-------+------------------+----------------------------------+
| core.servers.dns        | yes        |                                                             |
+-------------------------+------------+-------------------------------------------------------------+
|                                      | DnsServerConfig                                             |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | address          | ip address                       |
+-------------------------+------------+-------+------------------+----------------------------------+
| core.servers.time       | yes        |                                                             |
+-------------------------+------------+-------------------------------------------------------------+
|                                      | TimerServerConfig                                           |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | protocol         | registered choice                |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | address          | ip address                       |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | port             | integer                          |
+-------------------------+------------+-------+------------------+----------------------------------+
| core.packages           | yes        |                                                             |
+-------------------------+------------+-------------------------------------------------------------+
|                                      || PackageConfig                                              |
|                                      || *provided by:* ``core.generator.cgm``                      |
+--------------------------------------+-------+------------------+----------------------------------+
|                                      |       | enabled          | boolean                          |
+--------------------------------------+-------+------------------+----------------------------------+
