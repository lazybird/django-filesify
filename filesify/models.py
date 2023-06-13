import os

from django.db import models

try:
    from mirage.fields import EncryptedTextField

except ImportError:

    class EncryptedTextField:
        """
        This class only serves to raise an error to informs that the
        django-mirage-field package is required for using encrypted fields.
        """

        def __init__(self, *args, **kwargs):
            raise ImportError("CryptoFilesify requires django-mirage-field.")


class BaseFilesify(models.Model):
    """
    Base model for handling file creation and deletion.
    """

    file_path = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.file_path

    def create_file(self):
        """
        Generate a file with the given content.
        """
        if not self.file_path or not self.file_content:
            return
        with open(self.file_path, "w") as file:
            file.write(self.file_content)

    def save(self, *args, **kwargs):
        """
        Override the save method to generate files.
        """
        result = super().save(*args, **kwargs)
        self.create_file()
        return result

    def delete(self, *args, **kwargs):
        """
        Override the delete method to remove the generated file.
        """
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)
        return super().delete(*args, **kwargs)


class Filesify(BaseFilesify):
    """
    Abstract model providing file generation with plaintext content.
    """

    file_content = models.TextField()

    class Meta:
        abstract = True


class CryptoFilesify(BaseFilesify):
    """
    Abstract model providing file generation with encrypted content.
    """

    file_content = EncryptedTextField(
        help_text=("This field will be encrypted on save and decrypted on display.")
    )

    class Meta:
        abstract = True
