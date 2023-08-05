from datetime import datetime, timezone

from flask import Blueprint, request
from jinja2 import TemplateNotFound

from cornerstone.db.models import Page, Sermon
from cornerstone.email import send_email
from cornerstone.settings import get_setting
from cornerstone.theming import render

CONTACT_MESSAGE = """New contact form submission:

Name: {name}
E-mail: {email}
Subject: {subject}
Message:

{message}
"""

home = Blueprint('home', __name__)


def _get_datetime(isostring):
    if not isostring:
        return None
    return datetime.fromisoformat(isostring).astimezone(timezone.utc).replace(tzinfo=None)


@home.route('/', methods=['GET'])
def index():
    context = {
        'page': Page.query.filter_by(slug='home').first()
    }
    if get_setting('sermons-on-home-page', False):
        limit = get_setting('sermons-home-page-count', 10)
        context.update({
            'sermons': Sermon.query.order_by(Sermon.date.desc()).limit(limit).all()
        })
    try:
        return render('home.html', **context)
    except TemplateNotFound:
        return render('page.html', **context)


@home.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    message = None
    if request.method == 'POST' and not request.form.get('sweet-nectar'):
        body = CONTACT_MESSAGE.format(name=request.form['name'], email=request.form['email'],
                                      subject=request.form['subject'], message=request.form['message'])
        if send_email([get_setting('contact-form-email')], '[Contact Form] {}'.format(request.form['subject']), body):
            message = ('Thank you for your e-mail!', 'success')
        else:
            message = ('Unable to send your e-mail, please try again later', 'error')
    return render('contact-us.html', message=message)


@home.route('/live-stream', methods=['GET'])
def live_stream():
    context = {
        'stream_type': get_setting('live-stream-type'),
        'stream_id': get_setting('live-stream-id'),
        'stream_general': get_setting('live-stream-general'),
        'stream_before': get_setting('live-stream-before'),
        'stream_after': get_setting('live-stream-after'),
        'stream_start': _get_datetime(get_setting('live-stream-start')),
        'time_now': datetime.utcnow()
    }
    return render('live-stream.html', **context)
