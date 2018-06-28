import logging, mymodule

logging.basicConfig()

log = logging.getLogger("MyApp")
log.setLevel(logging.DEBUG) #set verbosity to show all messages of severity >= DEBUG
log.info("Starting my app")
try:
    mymodule.doIt()
except Exception, e:
    log.exception("There was a problem.")
log.info("Ending my app")

