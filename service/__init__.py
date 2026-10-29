"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and SQL database
"""
import sys
from flask import Flask
from flask_cors import CORS
from talisman import Talisman
from service import config
from service.common import log_handlers

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# Set up CORS
CORS(app)

# Set up Talisman security headers
talisman = Talisman(app)

# Dependencies require we import the routes AFTER the Flask app is created
# pylint: disable=wrong-import-position, wrong-import-order
from service import routes, models
from service.common import error_handlers

# Set up logging for production
log_handlers.init_app(app)

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    models.init_db(app)
except Exception as error:
    app.logger.critical("%s: Cannot continue", error)
    sys.exit(4)

app.logger.info("Service initialized!")
