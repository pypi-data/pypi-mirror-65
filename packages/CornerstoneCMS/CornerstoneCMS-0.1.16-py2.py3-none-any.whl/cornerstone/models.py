from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin

db = SQLAlchemy()
session = db.session


def get_or_create(session, model, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
    return instance


sermons_topics = db.Table(
    'sermons_topics',
    db.Column('sermon_id', db.Integer, db.ForeignKey('sermons.id'), primary_key=True),
    db.Column('topic_id', db.Integer, db.ForeignKey('topics.id'), primary_key=True)
)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    def __repr__(self):
        return self.name


class Sermon(db.Model):
    __tablename__ = 'sermons'
    id = db.Column(db.Integer, primary_key=True)
    preacher_id = db.Column(db.Integer, db.ForeignKey('preachers.id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    scripture = db.Column(db.String(255), nullable=False)
    simplecast_id = db.Column(db.String(50))
    date = db.Column(db.Date, nullable=False)

    preacher = db.relationship('Preacher', lazy='subquery', backref=db.backref('sermons', lazy=True))
    topics = db.relationship('Topic', secondary=sermons_topics, lazy='subquery',
                             backref=db.backref('sermons', lazy=True))

    def __repr__(self):
        return self.title


class Preacher(db.Model):
    __tablename__ = 'preachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return self.name


class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return self.title


class Page(db.Model):
    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text)
    weight = db.Column(db.Integer, default=0)

    def __repr__(self):
        return self.title


class Setting(db.Model):
    __tablename__ = 'settings'
    key = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    group = db.Column(db.String(255), default='core')
    value = db.Column(db.Text)
    type = db.Column(db.String(20), nullable=False)
    allowed_values = db.Column(db.Text, default='None')


class MenuLink(db.Model):
    __tablename__ = 'menulinks'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    weight = db.Column(db.Integer, default=0)
    is_enabled = db.Column(db.Boolean, default=True)
    can_edit = db.Column(db.Boolean, default=True)


def setup_db(app):
    """
    Set up the database
    """
    # Need this to prevent a circular import
    from cornerstone.settings import add_setting, has_setting, save_setting

    # Create the tables
    db.create_all()
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
    index_page = get_or_create(db.session, Page, slug='home')
    if not index_page.title and not index_page.body:
        index_page.title = 'Home'
        index_page.body = '<h1>Home</h1><p>This is the home page. Edit it and replace this content with your own.</p>'
        db.session.add(index_page)
    # Add some settings, if they don't already exist
    if not has_setting('sermons-on-home-page'):
        add_setting('Show sermons on the home page', 'sermons-on-home-page', 'bool', 'home page')
        save_setting('sermons-on-home-page', False)
        add_setting('Number of sermons to show on the home page', 'sermons-home-page-count', 'int', 'home page')
        save_setting('sermons-home-page-count', 10)
    if not has_setting('pages-in-menu'):
        add_setting('Include pages in menu automatically', 'pages-in-menu', 'bool', 'menu')
        save_setting('pages-in-menu', True)
    if not has_setting('theme'):
        add_setting('Theme', 'theme', 'str', 'theme')
        save_setting('theme', 'bootstrap4')
    # Create some permanent menu links
    if not MenuLink.query.filter_by(slug='home').first():
        db.session.add(MenuLink(title='Home', slug='home', url='/', can_edit=False))
    if not MenuLink.query.filter_by(slug='sermons').first():
        db.session.add(MenuLink(title='Sermons', slug='sermons', url='/sermons', can_edit=False))
    db.session.commit()
