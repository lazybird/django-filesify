from django.apps import apps
from django.core.management.base import BaseCommand

from filesify.models import BaseFilesify


class Command(BaseCommand):
    help = "Create files for all models that inherit from Filesify."

    def add_arguments(self, parser):
        parser.add_argument(
            "models",
            nargs="*",
            type=str,
            help="Optional list of specific models to create files for. "
            "Provide models as dot strings in 'myapp.MyModel' format. "
            "If not provided, files will be created for all models "
            "inheriting from Filesify.",
        )

    def is_filesify_subclass(self, obj):
        """
        Checks if the given object is a valid subclass of Filesify, excluding Filesify itself.
        """
        return issubclass(obj, BaseFilesify) and obj is not BaseFilesify

    def get_all_filesify_models(self):
        """
        Get all models that extends from Filesify abstract model.
        """
        return [
            model for model in apps.get_models() if self.is_filesify_subclass(model)
        ]

    def get_models_from_args(self, models_arg):
        """
        Get Filesyfy models class for the given dot path strings.
        """
        models = []
        for model_path in models_arg:
            app_label, model_name = model_path.split(".")
            model = apps.get_model(app_label, model_name)
            if not self.is_filesify_subclass(model):
                raise TypeError(f"Model {model_path} is not a subclass of Filesify")
            models.append(model)
        return models

    def handle(self, *args, **options):
        models_arg = options["models"]
        if models_arg:
            filesify_models = self.get_models_from_args(models_arg)
        else:
            filesify_models = self.get_all_filesify_models()
        for model in filesify_models:
            self.stdout.write(
                f"Creating files for model: {model._meta.app_label}.{model.__name__}"
            )
            for item in model.objects.all():
                self.stdout.write(f"    -- Creating file: {item}")
                item.create_file()
