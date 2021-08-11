import logging
import socket

import voluptuous as vol

from homeassistant.components.switch import SwitchEntity, PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, CONF_SWITCHES
import homeassistant.helpers.config_validation as cv

from . import DOMAIN, CONF_PORT, CONF_HOST

_LOGGER = logging.getLogger(__name__)

CONF_RELAYS = "relays"
CONF_RELAY_NAME = "relay_name"
CONF_RELAY_NB = "relay_nb"

RELAY_SCHEMA = vol.Schema(
	{
		vol.Required(CONF_RELAY_NAME): cv.string, 
		vol.Required(CONF_RELAY_NB): cv.positive_int,
	}
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
	{
		vol.Required(CONF_RELAYS): vol.Schema({cv.string: RELAY_SCHEMA}),
	}
)

def setup_platform(hass, config, add_entities, discovery_info=None):
	#relaycard = hass.data[DOMAIN]

	relays = config.get(CONF_RELAYS)
	devices = []
	for dev_name, properties in relays.items():
		devices.append(
			relaySwitch(
				dev_name,
	#			relaycard,
				properties
				)
			)
	add_entities(devices)


class relaySwitch(SwitchEntity):
  def __init__(self, name, properties):
     self._name = properties[CONF_RELAY_NAME]
     self._nb = properties[CONF_RELAY_NB]
     self._host = '192.168.0.166'
     self._port = 1234
     self._attr_is_on = self.relayAction("R")


  def relayAction(self, action):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((self._host, self._port))
    
    message=action+str(self._nb)
    n = client.send(bytes(message, 'utf-8'))
        
    data = client.recv(1024)
    client.shutdown(2)
    
    res=data.decode("utf-8").strip() 
    if "Relayoff" in res:
      return False
    else: 
      return True
  
  def turn_off(self, **kwargs):
     res=self.relayAction("D")
     self._attr_is_on = res
  def turn_on(self, **kwargs):
     res=self.relayAction("L")
     self._attr_is_on = res

  @property
  def name(self):
      """Get the name of the pin."""
      return self._name

