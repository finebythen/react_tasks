from django.core.management.base import BaseCommand
from ...models import MainTask, SubTask


class Command(BaseCommand):
    help = 'Clear the models Main- and Subtask from database.'

    def handle(self, *args, **options):
        count_main = MainTask.objects.count()
        count_sub = SubTask.objects.count()

        MainTask.objects.all().delete()
        SubTask.objects.all().delete()

        print('*' * 25)
        print('Der Befehl "clear_db" wurde erfolgreich ausgeführt.')
        print(f'Es wurden {count_main} MainTask-Einträge gelöscht.')
        print(f'Es wurden {count_sub} SubTask-Einträge gelöscht.')
        print('*' * 25)
