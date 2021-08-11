import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
import socket


from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    EVENT_HOMEASSISTANT_START,
    EVENT_HOMEASSISTANT_STOP,
    EVENT_STATE_CHANGED,
)

from homeassistant.helpers import state


_LOGGER = logging.getLogger(__name__)

DOMAIN = "relaycard"

CONFIG_SCHEMA = vol.Schema(
	{
		DOMAIN: vol.Schema({
			vol.Required(CONF_HOST): cv.string,
			vol.Optional(CONF_PORT, default=1234): cv.port,
		})
	},
	extra=vol.ALLOW_EXTRA,
)

def setup(hass, config):
   conf = config[DOMAIN]
   host = conf.get(CONF_HOST)
   port = conf.get(CONF_PORT)
 
   try:
     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     client.connect((host, port))
     client.shutdown(2)
     _LOGGER.info("Connection to relaycard possible") 
     hass.states.set('relaycard.connection', 'Works!')
 
   except OSError:
     _LOGGER.error("Unable to connect to relaycard")
     return False

   #print('Connection to ' + HOST + ':' + str(PORT) + ' ok')
   return True

