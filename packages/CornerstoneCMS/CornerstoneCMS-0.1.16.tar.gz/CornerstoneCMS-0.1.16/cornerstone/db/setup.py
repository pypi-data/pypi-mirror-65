from sqlalchemy.orm.session import close_all_sessions
from cornerstone.db import db, get_or_create
from cornerstone.db.models import MenuItem, Page, User
from cornerstone.settings import SETTINGS, add_setting, has_setting, save_setting


def setup_app(app):
    """
    Set up the application the first time
    """
    # Force SQLAlchemy to reload its session
    db.session.commit()
    db.session.close()
    db.session.remove()
    close_all_sessions()
    # Optionally create a superuser
    if app.config.get('CORNERSTONE_SUPERUSER', None) and app.config['CORNERSTONE_SUPERUSER'].get('email', None):
        superuser = app.config['CORNERSTONE_SUPERUSER']
        if not User.query.filter(User.email == superuser['email']).first():
            user = User(
                name=superuser.get('name', 'Superuser'),
                email=superuser['email'],
                password=app.user_manager.hash_password(superuser.get('password', 'Password1')),
            )
            db.session.add(user)
    # Create the home page, if it doesn't exist
    index_page = get_or_create(Page, slug='home')
    if not index_page.title and not index_page.body:
        index_page.title = 'Home'
        index_page.body = '<h1>Home</h1><p>This is the home page. Edit it and replace this content with your own.</p>'
        db.session.add(index_page)
    # Add some settings, if they don't already exist
    for setting in SETTINGS:
        if not has_setting(setting['key']):
            add_setting(setting['title'], setting['key'], setting['type'], setting['group'], setting['allowed_values'])
            save_setting(setting['key'], setting['initial_value'])
    # Create some permanent menu items
    if not MenuItem.query.filter_by(slug='home').first():
        db.session.add(MenuItem(title='Home', slug='home', url='/', can_edit=False))
    if not MenuItem.query.filter_by(slug='sermons').first():
        db.session.add(MenuItem(title='Sermons', slug='sermons', url='/sermons', can_edit=False))
    if not MenuItem.query.filter_by(slug='contact-us').first():
        db.session.add(MenuItem(title='Contact Us', slug='contact-us', url='/contact-us', can_edit=False,
                                is_enabled=False))
    if not MenuItem.query.filter_by(slug='live-stream').first():
        db.session.add(MenuItem(title='Live Stream', slug='live-stream', url='/live-stream', can_edit=False,
                                is_enabled=False))
    db.session.commit()
