# Generated by Django 3.1.3 on 2020-11-12 16:13

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import pik.core.models.uided
import simple_history.models
import user_profile.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='updated')),
                ('uid', models.UUIDField(default=pik.core.models.uided._new_uid, editable=False, primary_key=True, serialize=False)),
                ('version', models.IntegerField(editable=False)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, editable=False, null=True, verbose_name='deleted')),
                ('username', models.CharField(error_messages={'unique': 'Пользователь с таким логином уже существует.'}, help_text='Обязательное. 150 символов или меньше. Разрешается использовать буквы, цифры и @/./+/-/_.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('middle_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Отчество')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
                'ordering': ['-updated'],
            },
            managers=[
                ('objects', user_profile.managers.SoftObjectsUserManager()),
                ('all_objects', user_profile.managers.AllObjectsUserManager()),
                ('deleted_objects', user_profile.managers.SoftDeletedObjectsUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
            ],
            options={
                'verbose_name': 'group',
                'verbose_name_plural': 'groups',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created', models.DateTimeField(blank=True, db_index=True, editable=False, verbose_name='created')),
                ('updated', models.DateTimeField(blank=True, db_index=True, editable=False, verbose_name='updated')),
                ('uid', models.UUIDField(db_index=True, default=pik.core.models.uided._new_uid, editable=False)),
                ('version', models.IntegerField(editable=False)),
                ('deleted', models.DateTimeField(blank=True, db_index=True, editable=False, null=True, verbose_name='deleted')),
                ('username', models.CharField(db_index=True, error_messages={'unique': 'Пользователь с таким логином уже существует.'}, help_text='Обязательное. 150 символов или меньше. Разрешается использовать буквы, цифры и @/./+/-/_.', max_length=150, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('middle_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Отчество')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical пользователь',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]