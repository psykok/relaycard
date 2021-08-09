import logging
from homeassistant.const import EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
import socket

_LOGGER = logging.getLogger(__name__)

DOMAIN = "relaycard"

CONF_HOST = "host"
CONF_PORT = "port"

CONFIG_SCHEMA = vol.Schema(
	{
		DOMAIN: vol.Schema({
			vol.Required(CONF_HOST): cv.string,
			vol.Optional(CONF_PORT, default=1234): cv.positive_int,
		})
	},
	extra=vol.ALLOW_EXTRA,
)

def setup(hass, config):
   conf = config[DOMAIN]
   HOST = conf.get(CONF_HOST)
   PORT = conf.get(CONF_PORT)

   client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   client.connect((HOST, PORT))

   print('Connexion vers ' + HOST + ':' + str(PORT) + ' reussie.')
   return True

