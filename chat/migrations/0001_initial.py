# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True, blank=True)),
                ('app', models.CharField(max_length=12)),
                ('shoppening', models.CharField(max_length=12)),
                ('code', models.CharField(max_length=120)),
                ('used', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Facebook',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True, blank=True)),
                ('app', models.CharField(max_length=12)),
                ('facebook_id', models.BigIntegerField(db_index=True)),
                ('token', models.CharField(default=None, max_length=1024, null=True, blank=True)),
                ('email', models.EmailField(default=None, max_length=75, null=True, blank=True)),
                ('username', models.TextField(default=None, null=True, blank=True)),
                ('name', models.TextField(default=None, null=True, blank=True)),
                ('gender', models.IntegerField(default=0, choices=[(0, b'-'), (1, b'Male'), (2, b'Female')])),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True, blank=True)),
                ('app', models.CharField(max_length=12)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('follow', models.ForeignKey(related_name='member_follow_set', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FollowApp',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True, blank=True)),
                ('app', models.CharField(max_length=12)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FollowRaw',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True, blank=True)),
                ('app', models.CharField(max_length=12)),
                ('facebook_id', models.BigIntegerField(db_index=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True, blank=True)),
                ('from_user', models.CharField(max_length=12)),
                ('to_user', models.CharField(max_length=12)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True, blank=True)),
                ('from_user', models.CharField(max_length=12)),
                ('to_user', models.CharField(max_length=12)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('rejected', models.DateTimeField(null=True, blank=True)),
                ('viewed', models.DateTimeField(null=True, blank=True)),
                ('type', models.IntegerField(default=1, choices=[(0, b'-'), (1, b'Sent request'), (2, b'Reject'), (3, b'Cancle'), (4, b'Accept')])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True, blank=True)),
                ('data', models.TextField(default=b'null')),
                ('user', models.ForeignKey(related_name='member_user_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True, blank=True)),
                ('app', models.CharField(max_length=12)),
                ('display', models.CharField(max_length=60, blank=True)),
                ('gender', models.IntegerField(default=0, choices=[(0, b'-'), (1, b'Male'), (2, b'Female')])),
                ('birthday', models.DateField(default=None, null=True, blank=True)),
                ('data', models.TextField(default=b'null')),
                ('code', models.CharField(db_index=True, max_length=32, blank=True)),
                ('login_apppro', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProfileData',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True, blank=True)),
                ('app', models.CharField(max_length=12)),
                ('name', models.CharField(max_length=12)),
                ('code', models.CharField(max_length=12)),
                ('type', models.IntegerField(choices=[(0, b'String')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResetPassword',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True, blank=True)),
                ('password', models.CharField(max_length=12)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('timestamp_reset', models.DateTimeField(default=None, null=True)),
                ('is_reset', models.BooleanField(default=False)),
                ('profile', models.ForeignKey(to='chat.Profile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='T1Card',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True, blank=True)),
                ('app', models.CharField(max_length=12)),
                ('idcard', models.CharField(max_length=15, blank=True)),
                ('t1card', models.CharField(max_length=15)),
                ('email', models.EmailField(default=None, max_length=75, null=True, blank=True)),
                ('mobileid', models.CharField(max_length=60, blank=True)),
                ('first_name_th', models.CharField(max_length=60, null=True, blank=True)),
                ('first_name_en', models.CharField(max_length=60, null=True, blank=True)),
                ('last_name_th', models.CharField(max_length=60, null=True, blank=True)),
                ('last_name_en', models.CharField(max_length=60, null=True, blank=True)),
                ('point_balance', models.BigIntegerField(blank=True)),
                ('point_expiring', models.BigIntegerField(blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Twitter',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True, blank=True)),
                ('twitter_id', models.BigIntegerField(unique=True, db_index=True)),
                ('name', models.TextField(blank=True)),
                ('screen_name', models.TextField(blank=True)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserUUID',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True, blank=True)),
                ('app', models.CharField(max_length=12)),
                ('uuid', models.CharField(max_length=120)),
                ('data', models.TextField(blank=True)),
                ('timestamp_create', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True, db_index=True)),
                ('code', models.ForeignKey(blank=True, to='chat.Code', null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='friendrequest',
            unique_together=set([('from_user', 'to_user')]),
        ),
        migrations.AlterUniqueTogether(
            name='friend',
            unique_together=set([('from_user', 'to_user')]),
        ),
        migrations.AddField(
            model_name='facebook',
            name='profile',
            field=models.ForeignKey(to='chat.Profile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facebook',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
