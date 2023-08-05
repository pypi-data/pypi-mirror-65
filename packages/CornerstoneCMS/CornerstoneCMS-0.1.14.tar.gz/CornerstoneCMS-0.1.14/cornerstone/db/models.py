from flask_user import UserMixin

from cornerstone.db import db


sermons_topics = db.Table(
    'sermons_topics',
    db.Column('sermon_id', db.Integer, db.ForeignKey('sermons.id'), primary_key=True),
    db.Column('topic_id', db.Integer, db.ForeignKey('topics.id'), primary_key=True)
)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    def __repr__(self):
        return self.name


class Sermon(db.Model):
    __tablename__ = 'sermons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return self.name


class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return self.title


class Page(db.Model):
    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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


class MenuItem(db.Model):
    __tablename__ = 'menuitems'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('menuitems.id'), nullable=True)
    slug = db.Column(db.String(255), nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    weight = db.Column(db.Integer, default=0)
    is_enabled = db.Column(db.Boolean, default=True)
    can_edit = db.Column(db.Boolean, default=True)

    children = db.relationship('MenuItem', backref=db.backref('parent', remote_side=[id]))

    def __repr__(self):
        return self.title

    def has_children(self):
        """Return True if there are any children for this menu item, else False"""
        return self.query.filter_by(parent_id=self.id).count() != 0
