from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.conf import settings
from web.nodes.models import Event
from django.contrib.sites.models import Site

class LatestEvents(Feed):
  link = "%s://%s" % ('https' if getattr(settings, 'FEEDS_USE_HTTPS', None) else 'http', Site.objects.get_current().domain)
  description = "Latest events generated by nodes participating in the mesh."

  def get_object(self, bits):
    if len(bits) != 1:
      return None

    return User.objects.get(id = bits[0])
  
  def title(self, obj):
    if not obj:
      return "%s - Latest mesh events" % settings.NETWORK_NAME

    return "%s - Mesh events for %s" % (obj.username, settings.NETWORK_NAME)
  
  def items(self, obj):
    if not obj:
      return Event.objects.order_by('-timestamp')[:30]

    return Event.objects.filter(node__owner = obj).order_by('-timestamp')[:30]

  def item_pubdate(self, item):
    return item.timestamp

  def item_link(self, item):
    return "%s/nodes/node/%s#evt%s" % (self.link, item.node.pk, item.id)
