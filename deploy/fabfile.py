# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime

import fabric.api as fab

from speedydeploy.deployment import _, Deployment
from speedydeploy.base import Ubuntu104
from speedydeploy.database import SqliteDatabase
from speedydeploy.vcs import GIT
from speedydeploy.project import Project, Memcache, CronTab
from speedydeploy.project.django import Django14
from speedydeploy.server import FcgiWrapper, Nginx, UwsgiBackend
from speedydeploy.providers.linode import Linode


class ArtsofteDeployment(Deployment):

    def node1(self):
        fab.env.hosts = ["node1.suvit.ru"]
        fab.env.project_name = "artsofte-exercise"
        fab.env.user = 'artsofte'
        fab.env.instance_name = fab.env.user

        fab.env.provider = Linode()

        fab.env.remote_dir = _("%(home_dir)s/%(project_name)s")

        fab.env.db = SqliteDatabase()

        fab.env.project = Project()
        fab.env.project.django = Django14(_('%(remote_dir)s/%(project_name)s/artexer'),
                                          settings_local=_('settings/settings_node1.py'),
                                          python_path=_('%(remote_dir)s/env/bin/python'))
        fab.env.project.django.USE_STATICFILES = True
        fab.env.project.django.USE_SOUTH = False

        fab.env.server = Nginx(domain='site2.suvit.ru')
        fab.env.backend = fab.env.server.backend = UwsgiBackend()
        fab.env.worker_count = 1

        fab.env.vcs = GIT()
        fab.env.git_path = \
            'https://github.com/suvit/artsofte-exercise'

    def update_code(self):
        project = fab.env.project

        if project.use_django:
            project.django.reload()

        if project.use_celery:
            self.celery_configure()
        if project.use_sphinxsearch:
            self.sphinxsearch_configure()
        if project.use_memcache:
            self.memcache_configure()

        if project.use_server:
            self.server_configure()
            #self.server_restart()
            self.server_reload()

    def update(self):
        self.vcs_deploy()
        self.update_code()


instance = ArtsofteDeployment()
