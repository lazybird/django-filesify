from django.core import management
from django.db.models.signals import post_migrate


class FilesifyBaseMixin:
    """
    Provides a way to generate files from models that are extended from Filesify.
    """

    filesify_limit_to_models = None  # List of models to look at. None means all models.

    def create_files(self, **kwargs):
        """
        Looks at the `filesify_limit_to_models` attribute that defines the models filesify
        should consider and run a the command that create files.
        """
        if self.filesify_limit_to_models is None:
            management.call_command("create_files")
            return None
        if not isinstance(self.filesify_limit_to_models, (list, tuple)):
            raise ValueError(
                "filesify_limit_to_models must be a list or tuple of dotted path models"
            )
        management.call_command("create_files", *self.filesify_limit_to_models)


class FilesifyPostMigrateMixin(FilesifyBaseMixin):
    """
    Provides a way to generate files on database post migrate signal.
    This is expected to be used on a AppConfig class.
    """

    def handle_post_migrate(self):
        post_migrate.connect(self.create_files, sender=self)

    def ready(self):
        super().ready()
        self.handle_post_migrate()
