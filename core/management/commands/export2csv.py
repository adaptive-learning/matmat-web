from contextlib import closing
import csv
import zipfile
from django.db import connection
import os
from django.core.management import BaseCommand, CommandError
import re
from matmat import settings
from questions.models import Answer, Question, Simulator
from model.models import Skill


class Command(BaseCommand):
    args = 'table name'
    help = "Delete all lazy user without data"

    BATCH_SIZE = 5 * 10**5
    MODELS_TO_EXPORT = [Question, Answer, Simulator, Skill]

    def __init__(self):
        super(Command, self).__init__()
        self.tables_to_export = []
        for model in self.MODELS_TO_EXPORT:
            self.tables_to_export.append(model._meta.db_table)

    def handle(self, *args, **options):

        if len(args) > 0 and len(args) != 1:
            raise CommandError('''
                The command requires exactly one arguments:
                - table name
                or no argument.
            ''')

        if len(args) > 0:
            table_name = args[0]
            self.handle_one_table(table_name)
        else:
            self.handle_all_tables()

    def handle_all_tables(self):
        for table_name in self.tables_to_export:
            self.handle_one_table(table_name)

        filename_zip = settings.MEDIA_ROOT + '/' + "matmat_export.zip"

        if os.path.exists(filename_zip):
            os.remove(filename_zip)

        zf = zipfile.ZipFile(filename_zip, 'w', zipfile.ZIP_DEFLATED)
        for table_name in self.tables_to_export:
            filename_csv = settings.MEDIA_ROOT + '/' + table_name + '.csv'
            zf.write(filename_csv, os.path.basename(filename_csv))
            os.remove(filename_csv)
        zf.close()

    def handle_one_table(self, table_name):
        if table_name not in self.tables_to_export:
            raise CommandError('table "%s" is not supported' % table_name)

        count = 0
        with closing(connection.cursor()) as cursor:
            cursor.execute('SELECT COUNT(*) FROM ' + table_name)
            count, = cursor.fetchone()
        print 'processing %s' % table_name, ',', count, 'items'

        sql = 'SELECT * FROM ' + table_name
        filename_csv = settings.MEDIA_ROOT + '/' + table_name + '.csv'
        for offset in xrange(0, count, self.BATCH_SIZE):
            with closing(connection.cursor()) as cursor:
                cursor.execute(sql + ' LIMIT ' + str(self.BATCH_SIZE) + ' OFFSET ' + str(offset))
                self.dump_cursor(
                    cursor,
                    filename_csv,
                    append=(offset > 0))

    def dump_cursor(self, cursor, filename, append=False):
        headers = [re.sub(r'_id$', '', col[0]) for col in cursor.description]
        with open(filename, 'a' if append else 'w') as csvfile:
            writer = csv.writer(csvfile)
            if not append:
                writer.writerow(headers)
            for row in cursor:
                row = [val.encode('utf-8') if isinstance(val, unicode) else val for val in row]
                writer.writerow(row)



