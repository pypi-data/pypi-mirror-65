import inspect
import re
from pathlib import Path

from unidecode import unidecode
from flask import redirect, url_for, request
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_user import current_user
from wtforms import PasswordField, TextAreaField
from wtforms.fields.html5 import IntegerField
from wtforms.widgets import TextArea

from cornerstone.db import session
from cornerstone.db.models import MenuItem, Page, Preacher, Sermon, Topic, User
from cornerstone.settings import get_all_settings, get_setting, has_setting, save_setting
from cornerstone.util import get_bool


def _create_slug(title):
    """
    Convert the title to a slug
    """
    return re.sub(r'\W+', '-', unidecode(title).lower()).strip('-')


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        class_ = kwargs.pop('class', '') or kwargs.pop('class_', '')
        class_ = 'ckeditor ' + class_
        kwargs['class'] = class_
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class AuthorizedMixin(object):
    def is_accessible(self):
        return current_user.is_active and current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('/'))
        else:
            return redirect(url_for('user.login', next=request.url))


class AuthorizedAdminIndexView(AuthorizedMixin, AdminIndexView):
    pass


class AuthorizedModelView(AuthorizedMixin, ModelView):
    extra_js = ['//cdn.ckeditor.com/4.11.4/full/ckeditor.js']
    column_exclude_list = ('password', 'can_edit', 'children')
    column_descriptions = {
        'weight': 'Use this to order items in the menu'
    }
    form_excluded_columns = ('can_edit', 'children')
    form_overrides = {
        'password': PasswordField,
        'weight': IntegerField,
        'body': CKTextAreaField,
        'description': CKTextAreaField
    }

    def on_model_change(self, form, model, is_create):
        if isinstance(model, Page):
            if not model.slug:
                model.slug = _create_slug(model.title)
            if get_setting('pages-in-menu', False) and not MenuItem.query.filter_by(slug=model.slug).first():
                session.add(
                    MenuItem(
                        title=model.title,
                        slug=model.slug,
                        url=url_for('pages.get', slug=model.slug),
                        is_enabled=True
                    )
                )
                session.commit()


class SettingsView(AuthorizedMixin, BaseView):

    def _toggle_contact_page(self, value):
        """
        Toggle the contact us page on or off
        """
        value = get_bool(value)
        print(value)
        menu_item = MenuItem.query.filter_by(slug='contact-us').first()
        if menu_item:
            menu_item.is_enabled = value
            session.add(menu_item)
            session.commit()

    def _toggle_live_stream(self, value):
        """
        Toggle the live stream page on or off
        """
        value = get_bool(value)
        menu_item = MenuItem.query.filter_by(slug='live-stream').first()
        if menu_item:
            menu_item.is_enabled = value
            session.add(menu_item)
            session.commit()

    @expose('/', methods=['GET'])
    def index(self):
        settings = get_all_settings()
        return self.render('admin/settings.html', settings=settings)

    @expose('/', methods=['POST'])
    def index_post(self):
        post_save = {
            'contact-form-enable': self._toggle_contact_page,
            'live-stream-enable': self._toggle_live_stream
        }
        for key, value in request.form.items():
            if has_setting(key):
                save_setting(key, value)
                if key in post_save:
                    post_save[key](value)
        return redirect(self.get_url('settings.index'))


def _get_template_mode():
    """
    Detect template mode. This allows us to use the bootstrap4 theme if it exists, and fall back to bootstrap3.

    NB: This is a temporary workaround until the Bootstrap 4 branch merges into Flask-Admin master
    """
    templates_path = Path(inspect.getfile(Admin)).resolve().parent / 'templates'
    admin_themes = [theme.name for theme in templates_path.iterdir()]
    if 'bootstrap4' in admin_themes:
        return 'bootstrap4'
    else:
        return 'bootstrap3'


# Set up the admin
admin = Admin(name='CornerstoneCMS', template_mode=_get_template_mode(), index_view=AuthorizedAdminIndexView())
admin.add_view(AuthorizedModelView(Page, session, name='Pages'))
admin.add_view(AuthorizedModelView(Sermon, session, name='Sermons'))
admin.add_view(AuthorizedModelView(Preacher, session, name='Preachers'))
admin.add_view(AuthorizedModelView(Topic, session, name='Topics'))
admin.add_view(AuthorizedModelView(MenuItem, session, name='Menu'))
admin.add_view(SettingsView(name='Settings', endpoint='settings'))
admin.add_view(AuthorizedModelView(User, session, name='Users'))
