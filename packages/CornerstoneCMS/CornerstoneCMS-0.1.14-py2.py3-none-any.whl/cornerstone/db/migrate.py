from pathlib import Path

from alembic.script import ScriptDirectory
from alembic.runtime.environment import EnvironmentContext

MIGRATIONS_DIR = str(Path(__file__).parent.parent / 'migrations')


def get_config_and_script(app):
    """Create a ScriptDirectory instance"""
    config = app.extensions['migrate'].migrate.get_config(MIGRATIONS_DIR)
    return config, ScriptDirectory.from_config(config)


def get_current_revision(app):
    """Get the current head revision"""
    config, script = get_config_and_script(app)
    current_revision = []

    def _get_current(rev, context):
        current_revision.extend([r.revision for r in script.get_all_current(rev)])
        return []

    with EnvironmentContext(config, script, fn=_get_current):
        script.run_env()
    return current_revision


def upgrade(app):
    """Upgrade the database"""
    config, script = get_config_and_script(app)

    def _upgrade(rev, context):
        return script._upgrade_revs('head', rev)

    with EnvironmentContext(config, script, fn=_upgrade, as_sql=False, starting_rev=None, destination_rev='head',
                            tag=None):
        script.run_env()
