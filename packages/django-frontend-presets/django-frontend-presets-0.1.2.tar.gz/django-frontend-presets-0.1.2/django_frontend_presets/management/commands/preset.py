from django.core.management import BaseCommand, CommandError

from django_frontend_presets import presets
from django_frontend_presets.utils import get_project_root


class Command(BaseCommand):
    available_presets = ('reset', 'bootstrap', 'vue', 'react',)

    help = "Swap the front-end scaffolding for the project"
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('type', type=str, help="The preset type ({presets})".format(
            presets=", ".join(self.available_presets)
        ))

    def handle(self, *args, **options):
        if not get_project_root():
            raise CommandError("No ROOT_DIR or BASE_DIR specified in settings.")

        type = options['type']

        if type not in self.available_presets:
            return self.stdout.write(
                self.style.WARNING("Invalid preset. Please choose between ({presets})".format(
                    presets=", ".join(self.available_presets)
                ))
            )

        if not presets.Init.check_installation():
            if type == "reset":
                return self._init()
            self._init()

        getattr(self, type)()

        return self.stdout.write(
            self.style.WARNING('Please run "npm install && npm run dev" to compile your fresh scaffolding.')
        )

    def _init(self):
        confirm = input(
            'Are you sure you want to delete default frontend files and directories? (y/n): '
        )
        if confirm.lower() != 'y':
            return self.stdout.write('Canceled.')

        presets.Init().install()
        return self.stdout.write(self.style.SUCCESS('Frontend scaffolding setup successfully.'))

    def reset(self):
        presets.Reset().install()
        return self.stdout.write(self.style.SUCCESS('Frontend scaffolding reset successfully.'))

    def bootstrap(self):
        presets.Bootstrap().install()
        return self.stdout.write(self.style.SUCCESS('Bootstrap scaffolding installed successfully.'))

    def vue(self):
        presets.Vue().install()
        return self.stdout.write(self.style.SUCCESS('Vuejs scaffolding installed successfully.'))

    def react(self):
        presets.React().install()
        return self.stdout.write(self.style.SUCCESS('React scaffolding installed successfully.'))
