__author__ = 'kohn'

from mendeleycache.mendeleycache import MendeleyCache
import logging
import sys

app = MendeleyCache(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)
app.logger.debug("MendeleyCache started")
