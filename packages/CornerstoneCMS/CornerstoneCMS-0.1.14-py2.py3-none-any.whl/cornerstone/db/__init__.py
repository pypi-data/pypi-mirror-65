from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
session = db.session


def get_or_create(model, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
    return instance
