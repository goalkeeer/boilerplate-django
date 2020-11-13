from sys import argv

from django.conf import global_settings as default_settings, settings
from django.db.backends.signals import connection_created
from django.db.migrations.executor import MigrationExecutor
from django.dispatch import receiver
from django.core.management.commands.migrate import Command as MigrateCommand


CUSTOM_USER_MIGRATION = ('user_profile', '0001_initial')


def get_migration_callback():
    """ Reusing original migration callback """
    migrate = MigrateCommand()
    parser = migrate.create_parser(argv[0], argv[1])
    options = parser.parse_args(argv[2:])
    migrate.verbosity = options.verbosity
    return migrate.migration_progress_callback


def on_pre_migrate(connection, **kwargs):
    """ Ensures that custom user migration executed before main migration
    process.

    The main problem with existing application custom user implementation is
    failing migration consistency check.
    But in fact migration is ok, the problem is that migration plan
    expects user migration applied before others.
    So only thing we need to do, is to force custom user migration.
    Here is approach when we detect such situation during migration process
    and manually applying custom user migration before checks executed.

    1. This method detects:
        1.1. if it executed within migrate command
        1.2. if other miggrations already applied
        1.3. custom_user migrations not applied
    2. Manually applies custom_user migration.

    """

    if len(argv) < 2 or argv[1] != 'migrate':
        return

    executor = MigrationExecutor(connection, get_migration_callback())
    executor.loader.load_disk()

    is_fresh = not executor.loader.applied_migrations
    is_applied = CUSTOM_USER_MIGRATION in executor.loader.applied_migrations
    if is_fresh or is_applied:
        return

    migration = executor.loader.disk_migrations[CUSTOM_USER_MIGRATION]
    state = executor._create_project_state(with_applied_migrations=True)  # noqa protected-access
    executor.apply_migration(state, migration)


# We hooked in to the migration process so we have to control need of this
# migration manually, otherwise this migration will be applied even if custom
# user is not set.
if settings.AUTH_USER_MODEL != default_settings.AUTH_USER_MODEL:
    on_pre_migrate = receiver(connection_created)(on_pre_migrate)  # noqa: invalid-name
