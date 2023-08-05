from os import path

from django.core.management.commands import startapp

import django_command_overrides

class Command(startapp.Command):

    def handle(self, **options):
        # if there is no template specified, use ours defined in conf
        template = options["template"]
        if not template:
            template = path.join(django_command_overrides.__path__[0], 'conf', 'app_template')
            options['template'] = template
        super().handle(**options)

