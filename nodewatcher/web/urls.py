from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Nodes
    (r'^$', 'wlanlj.nodes.views.nodes'),
    (r'^nodes/node_list$', 'wlanlj.nodes.views.nodes'),
    (r'^nodes/subnet_list$', 'wlanlj.nodes.views.subnets'),
    (r'^nodes/my_nodes$', 'wlanlj.nodes.views.my_nodes'),
    (r'^nodes/new$', 'wlanlj.nodes.views.node_new'),
    (r'^nodes/node/(?P<node_ip>.*?)$', 'wlanlj.nodes.views.node'),
    (r'^nodes/remove/(?P<node_ip>.*?)$', 'wlanlj.nodes.views.node_remove'),
    (r'^nodes/do_remove/(?P<node_ip>.*?)$', 'wlanlj.nodes.views.node_do_remove'),
    (r'^nodes/edit/(?P<node_ip>.*?)$', 'wlanlj.nodes.views.node_edit'),
    (r'^nodes/allocate_subnet/(?P<node_ip>.*?)$', 'wlanlj.nodes.views.node_allocate_subnet'),
    (r'^nodes/deallocate_subnet/(?P<subnet_id>\d+)$', 'wlanlj.nodes.views.node_deallocate_subnet'),
    (r'^nodes/do_deallocate_subnet/(?P<subnet_id>\d+)$', 'wlanlj.nodes.views.node_do_deallocate_subnet'),
    (r'^nodes/whitelist_mac$', 'wlanlj.nodes.views.whitelist_mac'),
    (r'^nodes/unwhitelist_mac/(?P<item_id>\d+)$', 'wlanlj.nodes.views.unwhitelist_mac'),
    (r'^nodes/gcl$', 'wlanlj.nodes.views.gcl'),
    (r'^nodes/topology$', 'wlanlj.nodes.views.topology'),
    (r'^nodes/map$', 'wlanlj.nodes.views.map'),
    (r'^feeds/whitelist$', 'wlanlj.nodes.views.whitelist'),

    # Generator
    (r'^generator/request/(?P<node_ip>.*?)$', 'wlanlj.generator.views.request'),
    (r'^generator/image/(?P<node_ip>.*?)$', 'wlanlj.generator.views.generate'),

    # Authentication
    (r'^auth/(?:login)?$', 'django.contrib.auth.views.login',
     {'template_name' : 'auth/login.html'}),

    (r'^auth/logout$', 'django.contrib.auth.views.logout_then_login'),

    (r'^auth/lost_pass$', 'django.contrib.auth.views.password_reset', 
     {'template_name' : 'auth/lost_pass.html', 'email_template_name' : 'auth/lost_pass_email.html'}),
)