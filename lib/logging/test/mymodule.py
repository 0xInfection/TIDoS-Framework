import logging
log = logging.getLogger("MyModule")

def doIt():
	log.debug("Doin' stuff...")
	#do stuff...
	raise TypeError, "Bogus type error for testing"

