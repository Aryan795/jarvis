"""Constants for the Jarvis integration."""

DOMAIN = "jarvis"

CONF_BRAIN_URL = "brain_url"
DEFAULT_BRAIN_URL = "http://10.0.0.0:8099"

#: How long to wait for the brain before giving up and saying so out loud.
#: A timeout must produce speech, never silence.
BRAIN_TIMEOUT = 8.0
