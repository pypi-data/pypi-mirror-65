from flask_themes2 import get_theme, render_theme_template

from cornerstone.db.models import MenuItem
from cornerstone.settings import get_setting


def render(template, **context):
    try:
        theme = get_theme(get_setting('theme', 'bootstrap4'))
    except KeyError:
        theme = get_theme('bootstrap4')
    context['menu'] = MenuItem.query\
        .filter_by(is_enabled=True)\
        .filter_by(parent_id=None)\
        .order_by(MenuItem.weight.asc()).all()
    return render_theme_template(theme, template, **context)
