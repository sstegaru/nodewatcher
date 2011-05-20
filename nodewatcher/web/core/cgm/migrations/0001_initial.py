# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    depends_on = (
        ("core", "0001_initial"),
    )
    needed_by = (
        ("core", "0002_create_pool"),
    )
    
    def forwards(self, orm):
        
        # Adding model 'CgmGeneralConfig'
        db.create_table('cgm_cgmgeneralconfig', (
            ('platform', self.gf('registry.fields.SelectorKeyField')(max_length=50, regpoint='node.config', enum_id='core.general#platform')),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('generalconfig_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.GeneralConfig'], unique=True, primary_key=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('router', self.gf('registry.fields.SelectorKeyField')(max_length=50, regpoint='node.config', enum_id='core.general#router')),
        ))
        db.send_create_signal('cgm', ['CgmGeneralConfig'])

        # Adding model 'CgmPackageConfig'
        db.create_table('cgm_cgmpackageconfig', (
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('root', self.gf('django.db.models.fields.related.ForeignKey')(related_name='config_cgm_cgmpackageconfig', to=orm['nodes.Node'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal('cgm', ['CgmPackageConfig'])

        # Adding model 'CgmInterfaceConfig'
        db.create_table('cgm_cgminterfaceconfig', (
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('root', self.gf('django.db.models.fields.related.ForeignKey')(related_name='config_cgm_cgminterfaceconfig', to=orm['nodes.Node'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal('cgm', ['CgmInterfaceConfig'])

        # Adding model 'EthernetInterfaceConfig'
        db.create_table('cgm_ethernetinterfaceconfig', (
            ('cgminterfaceconfig_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cgm.CgmInterfaceConfig'], unique=True, primary_key=True)),
            ('eth_port', self.gf('registry.fields.SelectorKeyField')(max_length=50, regpoint='node.config', enum_id='core.interfaces#eth_port')),
        ))
        db.send_create_signal('cgm', ['EthernetInterfaceConfig'])

        # Adding model 'WifiInterfaceConfig'
        db.create_table('cgm_wifiinterfaceconfig', (
            ('bitrate', self.gf('django.db.models.fields.IntegerField')(default=11)),
            ('cgminterfaceconfig_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cgm.CgmInterfaceConfig'], unique=True, primary_key=True)),
            ('protocol', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('wifi_radio', self.gf('registry.fields.SelectorKeyField')(max_length=50, regpoint='node.config', enum_id='core.interfaces#wifi_radio')),
            ('channel', self.gf('django.db.models.fields.IntegerField')(default=8)),
        ))
        db.send_create_signal('cgm', ['WifiInterfaceConfig'])

        # Adding model 'CgmNetworkConfig'
        db.create_table('cgm_cgmnetworkconfig', (
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('interface', self.gf('registry.fields.IntraRegistryForeignKey')(related_name='networks', to=orm['cgm.CgmInterfaceConfig'])),
            ('root', self.gf('django.db.models.fields.related.ForeignKey')(related_name='config_cgm_cgmnetworkconfig', to=orm['nodes.Node'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('cgm', ['CgmNetworkConfig'])

        # Adding model 'StaticNetworkConfig'
        db.create_table('cgm_staticnetworkconfig', (
            ('cgmnetworkconfig_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cgm.CgmNetworkConfig'], unique=True, primary_key=True)),
            ('family', self.gf('registry.fields.SelectorKeyField')(max_length=50, regpoint='node.config', enum_id='core.interfaces.network#family')),
        ))
        db.send_create_signal('cgm', ['StaticNetworkConfig'])

        # Adding model 'AllocatedNetworkConfig'
        db.create_table('cgm_allocatednetworkconfig', (
            ('usage', self.gf('registry.fields.SelectorKeyField')(max_length=50, regpoint='node.config', enum_id='core.interfaces.network#usage')),
            ('cgmnetworkconfig_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cgm.CgmNetworkConfig'], unique=True, primary_key=True)),
            ('cidr', self.gf('django.db.models.fields.IntegerField')(default=27)),
            ('pool', self.gf('registry.fields.ModelSelectorKeyField')(to=orm['nodes.Pool'])),
            ('family', self.gf('registry.fields.SelectorKeyField')(max_length=50, regpoint='node.config', enum_id='core.interfaces.network#family')),
        ))
        db.send_create_signal('cgm', ['AllocatedNetworkConfig'])

        # Adding model 'PPPoENetworkConfig'
        db.create_table('cgm_pppoenetworkconfig', (
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('cgmnetworkconfig_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cgm.CgmNetworkConfig'], unique=True, primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('cgm', ['PPPoENetworkConfig'])

        # Adding model 'WifiNetworkConfig'
        db.create_table('cgm_wifinetworkconfig', (
            ('cgmnetworkconfig_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cgm.CgmNetworkConfig'], unique=True, primary_key=True)),
            ('role', self.gf('registry.fields.SelectorKeyField')(max_length=50, regpoint='node.config', enum_id='core.interfaces.network#role')),
            ('essid', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('bssid', self.gf('registry.fields.MACAddressField')(max_length=17)),
        ))
        db.send_create_signal('cgm', ['WifiNetworkConfig'])

        # Adding model 'VpnServerConfig'
        db.create_table('cgm_vpnserverconfig', (
            ('protocol', self.gf('registry.fields.SelectorKeyField')(max_length=50, regpoint='node.config', enum_id='core.vpn.server#protocol')),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('port', self.gf('django.db.models.fields.IntegerField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('root', self.gf('django.db.models.fields.related.ForeignKey')(related_name='config_cgm_vpnserverconfig', to=orm['nodes.Node'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('cgm', ['VpnServerConfig'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'CgmGeneralConfig'
        db.delete_table('cgm_cgmgeneralconfig')

        # Deleting model 'CgmPackageConfig'
        db.delete_table('cgm_cgmpackageconfig')

        # Deleting model 'CgmInterfaceConfig'
        db.delete_table('cgm_cgminterfaceconfig')

        # Deleting model 'EthernetInterfaceConfig'
        db.delete_table('cgm_ethernetinterfaceconfig')

        # Deleting model 'WifiInterfaceConfig'
        db.delete_table('cgm_wifiinterfaceconfig')

        # Deleting model 'CgmNetworkConfig'
        db.delete_table('cgm_cgmnetworkconfig')

        # Deleting model 'StaticNetworkConfig'
        db.delete_table('cgm_staticnetworkconfig')

        # Deleting model 'AllocatedNetworkConfig'
        db.delete_table('cgm_allocatednetworkconfig')

        # Deleting model 'PPPoENetworkConfig'
        db.delete_table('cgm_pppoenetworkconfig')

        # Deleting model 'WifiNetworkConfig'
        db.delete_table('cgm_wifinetworkconfig')

        # Deleting model 'VpnServerConfig'
        db.delete_table('cgm_vpnserverconfig')
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cgm.allocatednetworkconfig': {
            'Meta': {'object_name': 'AllocatedNetworkConfig', '_ormbases': ['cgm.CgmNetworkConfig']},
            'cgmnetworkconfig_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cgm.CgmNetworkConfig']", 'unique': 'True', 'primary_key': 'True'}),
            'cidr': ('django.db.models.fields.IntegerField', [], {'default': '27'}),
            'family': ('registry.fields.SelectorKeyField', [], {'max_length': '50', 'regpoint': "'node.config'", 'enum_id': "'core.interfaces.network#family'"}),
            'pool': ('registry.fields.ModelSelectorKeyField', [], {'to': "orm['nodes.Pool']"}),
            'usage': ('registry.fields.SelectorKeyField', [], {'max_length': '50', 'regpoint': "'node.config'", 'enum_id': "'core.interfaces.network#usage'"})
        },
        'cgm.cgmgeneralconfig': {
            'Meta': {'object_name': 'CgmGeneralConfig', '_ormbases': ['core.GeneralConfig']},
            'generalconfig_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.GeneralConfig']", 'unique': 'True', 'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'platform': ('registry.fields.SelectorKeyField', [], {'max_length': '50', 'regpoint': "'node.config'", 'enum_id': "'core.general#platform'"}),
            'router': ('registry.fields.SelectorKeyField', [], {'max_length': '50', 'regpoint': "'node.config'", 'enum_id': "'core.general#router'"}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'cgm.cgminterfaceconfig': {
            'Meta': {'object_name': 'CgmInterfaceConfig'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'config_cgm_cgminterfaceconfig'", 'to': "orm['nodes.Node']"})
        },
        'cgm.cgmnetworkconfig': {
            'Meta': {'object_name': 'CgmNetworkConfig'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interface': ('registry.fields.IntraRegistryForeignKey', [], {'related_name': "'networks'", 'to': "orm['cgm.CgmInterfaceConfig']"}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'config_cgm_cgmnetworkconfig'", 'to': "orm['nodes.Node']"})
        },
        'cgm.cgmpackageconfig': {
            'Meta': {'object_name': 'CgmPackageConfig'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'config_cgm_cgmpackageconfig'", 'to': "orm['nodes.Node']"})
        },
        'cgm.ethernetinterfaceconfig': {
            'Meta': {'object_name': 'EthernetInterfaceConfig', '_ormbases': ['cgm.CgmInterfaceConfig']},
            'cgminterfaceconfig_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cgm.CgmInterfaceConfig']", 'unique': 'True', 'primary_key': 'True'}),
            'eth_port': ('registry.fields.SelectorKeyField', [], {'max_length': '50', 'regpoint': "'node.config'", 'enum_id': "'core.interfaces#eth_port'"})
        },
        'cgm.pppoenetworkconfig': {
            'Meta': {'object_name': 'PPPoENetworkConfig', '_ormbases': ['cgm.CgmNetworkConfig']},
            'cgmnetworkconfig_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cgm.CgmNetworkConfig']", 'unique': 'True', 'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'cgm.staticnetworkconfig': {
            'Meta': {'object_name': 'StaticNetworkConfig', '_ormbases': ['cgm.CgmNetworkConfig']},
            'cgmnetworkconfig_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cgm.CgmNetworkConfig']", 'unique': 'True', 'primary_key': 'True'}),
            'family': ('registry.fields.SelectorKeyField', [], {'max_length': '50', 'regpoint': "'node.config'", 'enum_id': "'core.interfaces.network#family'"})
        },
        'cgm.vpnserverconfig': {
            'Meta': {'object_name': 'VpnServerConfig'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('django.db.models.fields.IntegerField', [], {}),
            'protocol': ('registry.fields.SelectorKeyField', [], {'max_length': '50', 'regpoint': "'node.config'", 'enum_id': "'core.vpn.server#protocol'"}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'config_cgm_vpnserverconfig'", 'to': "orm['nodes.Node']"})
        },
        'cgm.wifiinterfaceconfig': {
            'Meta': {'object_name': 'WifiInterfaceConfig', '_ormbases': ['cgm.CgmInterfaceConfig']},
            'bitrate': ('django.db.models.fields.IntegerField', [], {'default': '11'}),
            'cgminterfaceconfig_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cgm.CgmInterfaceConfig']", 'unique': 'True', 'primary_key': 'True'}),
            'channel': ('django.db.models.fields.IntegerField', [], {'default': '8'}),
            'protocol': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'wifi_radio': ('registry.fields.SelectorKeyField', [], {'max_length': '50', 'regpoint': "'node.config'", 'enum_id': "'core.interfaces#wifi_radio'"})
        },
        'cgm.wifinetworkconfig': {
            'Meta': {'object_name': 'WifiNetworkConfig', '_ormbases': ['cgm.CgmNetworkConfig']},
            'bssid': ('registry.fields.MACAddressField', [], {'max_length': '17'}),
            'cgmnetworkconfig_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cgm.CgmNetworkConfig']", 'unique': 'True', 'primary_key': 'True'}),
            'essid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'role': ('registry.fields.SelectorKeyField', [], {'max_length': '50', 'regpoint': "'node.config'", 'enum_id': "'core.interfaces.network#role'"})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.generalconfig': {
            'Meta': {'object_name': 'GeneralConfig'},
            'altitude': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'geolocation': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'project': ('registry.fields.ModelSelectorKeyField', [], {'to': "orm['nodes.Project']"}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'config_core_generalconfig'", 'to': "orm['nodes.Node']"})
        },
        'dns.zone': {
            'Meta': {'object_name': 'Zone'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'expire': ('django.db.models.fields.IntegerField', [], {}),
            'minimum': ('django.db.models.fields.IntegerField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'primary_ns': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'refresh': ('django.db.models.fields.IntegerField', [], {}),
            'resp_person': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'retry': ('django.db.models.fields.IntegerField', [], {}),
            'serial': ('django.db.models.fields.IntegerField', [], {}),
            'zone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'})
        },
        'nodes.link': {
            'Meta': {'object_name': 'Link'},
            'dst': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dst'", 'to': "orm['nodes.Node']"}),
            'etx': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ilq': ('django.db.models.fields.FloatField', [], {}),
            'lq': ('django.db.models.fields.FloatField', [], {}),
            'src': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'src'", 'to': "orm['nodes.Node']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True', 'blank': 'True'}),
            'vtime': ('django.db.models.fields.FloatField', [], {})
        },
        'nodes.node': {
            'Meta': {'object_name': 'Node'},
            'ant_external': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'ant_polarization': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ant_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'awaiting_renumber': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'border_router': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'bssid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'captive_portal_status': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'channel': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'clients': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'clients_so_far': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'conflicting_subnets': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'dns_works': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'essid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'firmware_version': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'first_seen': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'geo_lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'geo_long': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'loadavg_15min': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'loadavg_1min': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'loadavg_5min': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'local_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'loss_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'memfree': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True'}),
            'node_type': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'numproc': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'peer_history': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'peer_history_rel_+'", 'to': "orm['nodes.Node']"}),
            'peer_list': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['nodes.Node']", 'through': "orm['nodes.Link']", 'symmetrical': 'False'}),
            'peers': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'pkt_loss': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'null': 'True', 'to': "orm['nodes.Project']"}),
            'redundancy_link': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'redundancy_req': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'reported_uuid': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'rtt_avg': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'rtt_max': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'rtt_min': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'system_node': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'thresh_frag': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'thresh_rts': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'uptime': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'uptime_last': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'uptime_so_far': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'vpn_mac': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'vpn_mac_conf': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True', 'null': 'True'}),
            'vpn_server': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'warnings': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'wifi_error_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'wifi_mac': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
        },
        'nodes.pool': {
            'Meta': {'object_name': 'Pool'},
            'cidr': ('django.db.models.fields.IntegerField', [], {}),
            'default_prefix_len': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'family': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_subnet': ('web.nodes.util.IPField', [], {'null': 'True'}),
            'max_prefix_len': ('django.db.models.fields.IntegerField', [], {'default': '28', 'null': 'True'}),
            'min_prefix_len': ('django.db.models.fields.IntegerField', [], {'default': '24', 'null': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': "orm['nodes.Pool']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'nodes.project': {
            'Meta': {'object_name': 'Project'},
            'captive_portal': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'channel': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'geo_lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'geo_long': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'geo_zoom': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pool': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nodes.Pool']"}),
            'pools': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects'", 'symmetrical': 'False', 'to': "orm['nodes.Pool']"}),
            'ssid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ssid_backbone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ssid_mobile': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sticker': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dns.Zone']", 'null': 'True'})
        }
    }
    
    complete_apps = ['cgm']
