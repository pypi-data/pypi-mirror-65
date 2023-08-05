from flask import Blueprint
from jinja2 import TemplateNotFound

from cornerstone.db.models import Page
from cornerstone.theming import render


pages = Blueprint('pages', __name__)


@pages.route('/<path:slug>', methods=['GET'])
def get(slug):
    template_name = '{}.html'.format(slug)
    page = Page.query.filter_by(slug=slug).first()
    try:
        return render(template_name, page=page)
    except TemplateNotFound:
        return render('page.html', page=page)
