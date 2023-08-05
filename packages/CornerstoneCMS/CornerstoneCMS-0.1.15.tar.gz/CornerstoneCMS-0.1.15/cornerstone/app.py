import logging
import os

from flask import Flask, current_app
from flask_admin.menu import MenuLink
from flask_migrate import Migrate
from flask_themes2 import Themes
from flask_user import UserManager

from cornerstone.admin import admin
from cornerstone.config import config_from_file
from cornerstone.db import db
from cornerstone.db.migrate import upgrade
from cornerstone.db.models import User
from cornerstone.db.setup import setup_app
from cornerstone.views.home import home
from cornerstone.views.pages import pages
from cornerstone.views.sermons import sermons
from cornerstone.views.setup import setup
from cornerstone.views.uploads import uploads

logging.basicConfig()


def _run_setup():
    # Set up database
    # current_revision = get_current_revision(current_app)
    upgrade(current_app)
    setup_app(current_app)


def create_app(config_file):
    # Set up the app
    app = Flask('cornerstone')
    config_from_file(app, config_file)
    if os.environ.get('THEME_PATHS'):
        app.config.update({'THEME_PATHS': os.environ['THEME_PATHS']})
    # Set up the extensions
    Themes(app, app_identifier='cornerstone')
    db.init_app(app)
    Migrate(app, db)
    admin.init_app(app)
    UserManager(app, db, User)
    # Register blueprints
    app.register_blueprint(home)
    app.register_blueprint(pages)
    app.register_blueprint(sermons)
    app.register_blueprint(setup)
    app.register_blueprint(uploads)
    # Register before method
    app.before_first_request(_run_setup)
    # Set up menu shortcuts
    admin.add_link(MenuLink('Back to main site', '/'))
    admin.add_link(MenuLink('Logout', '/user/sign-out'))
    return app
