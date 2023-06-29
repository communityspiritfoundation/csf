# Generated by Django 4.2.2 on 2023-06-28 04:54

from django.db import migrations, models
import django.utils.timezone
import users.models


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
                ('is_superuser', models.BooleanField(default=False, help_text='User has permissions, unassigned.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates if user can login admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates if user should be treated as active.'
                                                  'Unselect instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('team_signup', models.BooleanField(default=True)),
                ('has_consent', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups user belongs to.', related_name='user'
                                                  '_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_'
                                                            'set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', users.models.UserManager()),
            ],
        ),
    ]
