from __future__ import unicode_literals
from os.path import join

from docker.types import Mount
from ds.command import Command
from ds.presets.docker_base import BuildContext
from ds.presets.docker_base import DefaultNaming
from ds.presets.docker_base import UserMixin
from ds.presets.docker_base.commands import Exec

try:
    from accounts import ACCOUNTS
except ImportError:
    ACCOUNTS = []
try:
    from accounts import RSS
except ImportError:
    RSS = []


class Context(UserMixin, DefaultNaming, BuildContext):
    image_name = 'mail'

    mount_paths = {
        '.temp/generated/.offlineimaprc': '/.offlineimaprc',
        '.temp/generated/': '/generated/',
        '.temp/maildirs/': '/maildirs/',
        '.temp/feeds-cache/': '/feeds-cache/',
        '.temp/feeds/': '/feeds/',
        '.temp/offlineimap': '/.offlineimap',
        'docker/scripts/': '/scripts/',
    }

    container_entry = '/scripts/daemon.sh',
    # container_entry = '/bin/bash',

    def get_commands(self):
        return super(Context, self).get_commands() + [
            Update,
            Mail,
            Rss,
            CheckMail,
            CheckRss,
        ]

    def get_docker_file(self):
        return join(self.project_root, 'docker/Dockerfile')

    def get_build_path(self):
        return join(self.project_root, 'docker')

    def get_mounts(self):
        mounts = [
            Mount(target=dest,
                  source=join(self.project_root, src),
                  type='bind',
                  read_only=False)
            for src, dest in self.mount_paths.items()
        ]
        return super(Context, self).get_mounts() + mounts

    def get_run_options(self, **options):
        options.update(dict(
            detach=True,
            auto_remove=False,
            restart_policy={
                'Name': 'always',
            },
        ))
        options.update(dict(self.calc_cpu_to_options(0.1)))
        return super(Context, self).get_run_options(**options)


class Update(Command):
    short_help = 'Sync configs with declared accounts'
    consume_all_args = True

    files = {
        'muttrc-folder-hooks': 'muttrc-folder-hooks',
        'offlineimaprc': '.offlineimaprc',
        'feeds': 'feeds',
    }

    def invoke_with_args(self, args):
        for src, dest in self.files.items():
            src = join(self.context.project_root, 'docker/templates/', src)
            dest = join(self.context.project_root, '.temp/generated/', dest)

            self.render_template(src, dest, accounts=ACCOUNTS, rss=RSS)

    def render_template(self, src, dest, **context):
        from jinja2 import Template

        print('Update {}'.format(dest))

        with open(src, 'r') as input:
            template = Template(input.read())
            with open(dest, 'w') as output:
                output.write(template.render(**context).encode('utf-8'))


class _Script(Exec):
    script = None

    def get_command(self):
        return self.script,


class CheckMail(_Script):
    script = '/scripts/check-mail.sh'


class CheckRss(_Script):
    script = '/scripts/check-rss.sh'


class _Mutt(Command):
    consume_all_args = True
    muttrc = None

    def invoke_with_args(self, args):
        self.context.executor.append([
            'mutt',
            ('-F', self.muttrc),
            args,
        ])


class Mail(_Mutt):
    muttrc = 'mutt/muttrc-mail'


class Rss(_Mutt):
    muttrc = 'mutt/muttrc-rss'
