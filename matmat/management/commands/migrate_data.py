import json

import os
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connections
from proso_user.models import UserProfile


class Command(BaseCommand):
    help = 'Migrate from old matmat version'
    data_dir = 'data'

    def add_arguments(self, parser):
        parser.add_argument('parts', nargs='+', type=str)

    def handle(self, *args, **options):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        if 'flush' in options['parts']:
            call_command('flush')

        if 'users' in options['parts']:
            self.migrate_users()

        if 'profiles' in options['parts']:
            self.migrate_profiles()

        if 'questions' in options['parts']:
            self.migrate_question()

        if 'answers' in options['parts']:
            self.migrate_answers()

    def migrate_users(self):
        self.dump_load('auth', exclude=['auth.Permission'] )
        self.dump_load('lazysignup')
        self.dump_load('default', exclude=['default.Code'])

        self.stdout.write(self.style.SUCCESS('Users successfully migrated'))

    def migrate_profiles(self):
        profiles = {}
        with connections['old'].cursor() as cursor:
            cursor.execute('SELECT u.user_id, u.code, cp.user_id as child'
                           '  FROM core_userprofile u '
                           '  LEFT JOIN core_userprofile_children c '
                           '    ON u.id = c.from_userprofile_id'
                           '  LEFT JOIN core_userprofile cp '
                           '    ON c.to_userprofile_id = cp.id')
            for profile in dictfetchall(cursor):
                if profile['user_id'] in profiles:
                    profiles[profile['user_id']]['children'].append(profile['child'])
                else:
                    profiles[profile['user_id']] = {
                        'code': profile['code'],
                        'children': [] if profile['child'] is None else [profile['child']]
                    }
            with open('matmat-profiles.json', 'w') as output:
                json.dump(profiles, output)
            self.stdout.write(self.style.SUCCESS('Profiles successfully exported'))

        for user in User.objects.filter(lazyuser__isnull=True):
            UserProfile.objects.get_or_create(user=user)
        self.stdout.write(self.style.SUCCESS('New profiles successfully created'))

        self.stdout.write(self.style.ERROR('Profiles import not implemented!'))  # TODO

    def migrate_question(self):
        call_command('generate_tasks')
        call_command('load_tasks', os.path.join('data', 'matmat-contexts.json'),
                     os.path.join('data', 'matmat-skills.json'), os.path.join('data', 'matmat-tasks.json'))

    def dump_load(self, app, exclude=None):
        self.stdout.write('Copy ' + app)
        if exclude is None:
            exclude = []
        file_name = os.path.join(self.data_dir, 'matmat-{}.json'.format(app))
        with open(file_name, 'w') as output:
            self.stdout.write(' - dumping')
            call_command('dumpdata', app,
                         stdout=output,
                         exclude=exclude,
                         database='old'
                         )
        self.stdout.write(' - loading')
        call_command('loaddata', file_name)

    def migrate_answers(self):
        pass


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]