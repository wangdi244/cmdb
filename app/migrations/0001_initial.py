# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 09:30
from __future__ import unicode_literals

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('manage_role', models.CharField(choices=[(b'super', '\u8d85\u7ea7\u7ba1\u7406\u5458'), (b'manage', '\u7ba1\u7406\u5458')], default=b'super', max_length=30, verbose_name='\u89d2\u8272')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u7ba1\u7406',
                'verbose_name_plural': '\u7528\u6237\u7ba1\u7406',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='cmd_run',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(verbose_name='IP\u5730\u5740')),
                ('command', models.CharField(max_length=30, verbose_name='\u547d\u4ee4')),
                ('track_mark', models.IntegerField()),
            ],
            options={
                'verbose_name': '\u547d\u4ee4\u7ba1\u7406',
                'verbose_name_plural': '\u547d\u4ee4\u7ba1\u7406',
            },
        ),
        migrations.CreateModel(
            name='ContainsList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contain_id', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u5bb9\u5668ID')),
                ('contain_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP\u5730\u5740')),
                ('contain_netmask', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u5bb9\u5668\u63a9\u7801')),
                ('contain_port', models.CharField(blank=True, max_length=10, null=True, verbose_name='\u5bb9\u5668\u76d1\u542c\u7aef\u53e3')),
                ('contain_http', models.CharField(blank=True, max_length=10, null=True, verbose_name='\u670d\u52a1url')),
                ('create_datetime', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u5bb9\u5668\u521b\u5efa\u65f6\u95f4')),
                ('contain_cpu_core', models.CharField(blank=True, max_length=10, null=True, verbose_name='cpu\u7ed1\u5b9a\u6838\u53f7')),
                ('contain_host', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u7269\u7406\u673a\u4e3b\u673a\u540d')),
                ('contain_memory', models.CharField(blank=True, max_length=10, null=True, verbose_name='\u5185\u5b58\u5206\u914d')),
                ('contain_hostname', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u5bb9\u5668\u4e3b\u673a\u540d')),
                ('release_application', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u5e94\u7528\u540d\u79f0')),
                ('service_pack', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u5e94\u7528\u5305\u540d')),
                ('service_depend', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u5e94\u7528\u4f9d\u8d56')),
                ('service_env', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u670d\u52a1\u73af\u5883')),
                ('project_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u9879\u76ee\u540d\u79f0')),
                ('proposer', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u9879\u76ee\u5f00\u53d1\u8005')),
                ('principal', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u9879\u76ee\u8d1f\u8d23\u4eba')),
                ('project_section', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u9879\u76ee\u6240\u5c5e\u90e8\u95e8')),
                ('state', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u5bb9\u5668\u72b6\u6001')),
                ('flag', models.CharField(blank=True, max_length=5, null=True, verbose_name='\u5bb9\u5668\u6807\u8bb0\u4f4d')),
                ('x_flag', models.CharField(blank=True, max_length=30, null=True, verbose_name='\u5bb9\u5668\u5904\u7406\u60c5\u51b5')),
            ],
            options={
                'verbose_name': '\u5bb9\u5668\u5217\u8868',
                'verbose_name_plural': '\u5bb9\u5668\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u7ec4\u4fe1\u606f',
                'verbose_name_plural': '\u4e3b\u673a\u7ec4\u4fe1\u606f\u7ba1\u7406',
            },
        ),
        migrations.CreateModel(
            name='HostList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(unique=True, verbose_name='\u7269\u7406\u673aIP\u5730\u5740')),
                ('manage_ip', models.GenericIPAddressField(unique=True, verbose_name='\u7ba1\u7406IP\u5730\u5740')),
                ('hostname', models.CharField(max_length=30, verbose_name='\u4e3b\u673a\u540d')),
                ('application', models.CharField(max_length=20, verbose_name='\u5e94\u7528')),
                ('bianhao', models.CharField(max_length=30, verbose_name='\u7f16\u53f7')),
                ('idc_name', models.CharField(blank=True, max_length=40, null=True, verbose_name='\u6240\u5c5e\u673a\u623f')),
                ('group', models.ManyToManyField(blank=True, to='app.Group', verbose_name='\u7ec4\u540d')),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u5217\u8868',
                'verbose_name_plural': '\u4e3b\u673a\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='Idc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idc_name', models.CharField(max_length=40, verbose_name='\u673a\u623f\u540d\u79f0')),
                ('idc_address', models.CharField(max_length=80, verbose_name='\u673a\u623f\u5730\u5740')),
                ('remark', models.CharField(max_length=40, verbose_name='\u5907\u6ce8')),
            ],
            options={
                'verbose_name': '\u673a\u623f\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='salt_return',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fun', models.CharField(max_length=50)),
                ('jid', models.CharField(max_length=255)),
                ('result', models.TextField()),
                ('host', models.CharField(max_length=255)),
                ('success', models.CharField(max_length=10)),
                ('full_ret', models.TextField()),
            ],
            options={
                'verbose_name': '\u547d\u4ee4\u8fd4\u56de\u7ed3\u679c',
                'verbose_name_plural': '\u547d\u4ee4\u8fd4\u56de\u7ed3\u679c',
            },
        ),
        migrations.CreateModel(
            name='ServerAsset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer', models.CharField(max_length=20, verbose_name='\u5382\u5546')),
                ('productname', models.CharField(max_length=30, verbose_name='\u4ea7\u54c1\u578b\u53f7')),
                ('service_tag', models.CharField(max_length=80, unique=True, verbose_name='\u5e8f\u5217\u53f7')),
                ('cpu_model', models.CharField(max_length=50, verbose_name='CPU\u578b\u53f7')),
                ('cpu_nums', models.PositiveSmallIntegerField(verbose_name='CPU\u7ebf\u7a0b\u6570')),
                ('cpu_groups', models.PositiveSmallIntegerField(verbose_name='CPU\u7269\u7406\u6838\u6570')),
                ('mem', models.CharField(max_length=100, verbose_name=b'\xe5\x86\x85\xe5\xad\x98\xe5\xa4\xa7\xe5\xb0\x8f')),
                ('disk', models.CharField(max_length=300, verbose_name=b'\xe7\xa1\xac\xe7\x9b\x98\xe5\xa4\xa7\xe5\xb0\x8f')),
                ('hostname', models.CharField(max_length=30, verbose_name='\u4e3b\u673a\u540d')),
                ('ip', models.CharField(max_length=20, verbose_name='IP\u5730\u5740')),
                ('os', models.CharField(max_length=20, verbose_name='\u64cd\u4f5c\u7cfb\u7edf')),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u8d44\u4ea7\u4fe1\u606f',
                'verbose_name_plural': '\u4e3b\u673a\u8d44\u4ea7\u4fe1\u606f\u7ba1\u7406',
            },
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headImg', models.FileField(upload_to=b'./upload/')),
            ],
            options={
                'verbose_name': '\u6587\u4ef6\u4e0a\u4f20',
                'verbose_name_plural': '\u6587\u4ef6\u4e0a\u4f20',
            },
        ),
        migrations.AddField(
            model_name='newuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='newuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]