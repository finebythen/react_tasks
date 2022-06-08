from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from ...models import MainTask, SubTask


USER = get_user_model()


class Command(BaseCommand):
    help = 'Insert x sample entries of Main- and SubTask to database.'

    def handle(self, *args, **options):
        count_main = MainTask.objects.count()
        count_sub = SubTask.objects.count()

        if count_main > 0 or count_sub > 0:
            print('*' * 25)
            print('Der Befehl "insert_db" konnte nicht ausgeführt werden.')
            print(f'Es befinden sich noch {count_main + count_sub} Einträge in der Datenbank.')
            print('Führen Sie zuerst den Befehl "python manage.py clear_db" aus.')
            print('*' * 25)
        else:
            l_main = []
            admin_user = USER.objects.get(email='admin@email.com')
            for i in range(0, 10):
                l_main.append(
                    MainTask(
                        id=i,
                        title=f'Task #00{i}',
                        slug=f'task-00{i}',
                        created_by=admin_user
                    )
                )

            MainTask.objects.bulk_create(l_main)

            l_sub = []
            for item in MainTask.objects.all():
                for i in range(0, 10):
                    l_sub.append(
                        SubTask(
                            maintask=item,
                            title=f'Subtitle #00{i}',
                            slug=f'{slugify(item.title)}-subtitle-00{i}',
                            created_by=admin_user
                        )
                    )
            
            SubTask.objects.bulk_create(l_sub)

            print('*' * 25)
            print('Der Befehl "insert_db" wurde erfolgreich ausgeführt.')
            print('Es wurden 10 MainTask-Einträge in die Datenbank geschrieben.')
            print('Es wurden 100 SubTask-Einträge in die Datenbank geschrieben.')
            print('*' * 25)