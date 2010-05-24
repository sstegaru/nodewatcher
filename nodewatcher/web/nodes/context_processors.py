from django.conf import settings
from django.contrib.sites.models import Site
from web.nodes.models import Subnet

def web_client_node(request):
  """
  Adds web_client_node variable to current template context
  depending on whether the current client's IP address is from
  a node's allocated subnet.
  """
  try:
    subnet = Subnet.objects.ip_filter(ip_subnet__contains = request.META["REMOTE_ADDR"]).exclude(cidr = 0)[0]
    node = subnet.node
  except IndexError:
    node = None
  
  return {
    'web_client_node' : node
  }

def global_values(request):
  """
  Adds some global values to the context.
  """
  return {
   'network' : { 'name'        : settings.NETWORK_NAME,
                 'contact'     : settings.NETWORK_CONTACT,
                 'description' : getattr(settings, 'NETWORK_DESCRIPTION', None)
               },
   'base_url'                  : "%s://%s" % ('https' if getattr(settings, 'FEEDS_USE_HTTPS', None) else 'http', Site.objects.get_current().domain),
   'reset_password_url'        : getattr(settings, 'RESET_PASSWORD_URL', None),
   'profile_configuration_url' : getattr(settings, 'PROFILE_CONFIGURATION_URL', None),
   'register_user_url'         : getattr(settings, 'REGISTER_USER_URL', None),
   'images_bindist_url'        : getattr(settings, 'IMAGES_BINDIST_URL', None),
   'documentation_links'       : getattr(settings, 'DOCUMENTATION_LINKS', {})
  }