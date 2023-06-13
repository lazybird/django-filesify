Django Filesify
===============

Django Filesify helps generate a physical files from a text content stored in
database and accessible from Django admin.
The file content can be a plaintext or an encrypted field.

Requirements
------------

-  Python 3.6+
-  Django 3.1+
-  Optional : django-mirage-field
-  Optional : Pip 22+


.. _filesify-usage:

Usage
-----

Extend ``Filesify`` class in your Django model and define your
custom fields:


.. _filesify-usage-plain-text:

For plaintext content
~~~~~~~~~~~~~~~~~~~~~

::

  from filesify.models import Filesify

  class MyConfigModel(Filesify):

      class Meta:
          verbose_name = "Some config file"
          verbose_name_plural = "Some config files"

.. _filesify-usage-encrypted:

For encrypted content
~~~~~~~~~~~~~~~~~~~~~

If your file content is sensitive information, you could decide to
encrypt it. This will be transparent to you, as the the ``file_content``
field provided by ``django-filesify`` will be encrypted on model save
and decrypted before displaying it on the admin.

For encrypted content, ``django-mirage-field`` is required.

You could install ``django-mirage-field`` like this :

::

  pip install django-mirage-fields

Extend CryptoFilesify:

::

  from filesify.models import CryptoFilesify

  class MyConfigModel(CryptoFilesify):

      class Meta:
          verbose_name = "Some config file"
          verbose_name_plural = "Some config files"



.. _filesify-model:

About the abstract model
------------------------

.. _filesify-model-fields:

Model Fields
~~~~~~~~~~~~

The model class provide the following fields:

-  ``file_path``: The path of the file to generate.
-  ``file_content``: The text file content - either plain text or
   encrypted, depending on the mixin used.
-  ``comment``: A TextField for optional comments about the file.


.. _filesify-model-file-generation:

File generation
~~~~~~~~~~~~~~~

The mixin class generates a file with the content provided in the
``file_content`` field. The file generation will be trigger on the
save() method, that means it's done automatically when creating or
updating your model instances.

::

   # This create 'example.txt' containing 'Hello, World!'
   obj = MyConfigModel()
   obj.file_path = "/tmp/example.txt"
   obj.file_content = "Hello, World!"
   obj.save()

   # Equivalent to:
   obj = MyConfigModel(file_path="/tmp/example.txt", file_content="Hello, World!")

   # The file generation can be triggered manually like this:
   obj.create_file()  


.. _filesify-model-file-removeal:

File removeal
~~~~~~~~~~~~~
When an Filesify object is delete, the files on disk will be deleted as well. This is done
by overriding the model ``delete()`` method.



.. _filesify-admin:

Filesify Admin
--------------


Django Filesify provide a admin class that can be used this way :


::

  from django.contrib import admin
  from my_app.models import MyConfigModel
  from filesify.admin import FilesifyAdmin

  @admin.register(MyConfigModel)
  class MyConfigModelAdmin(FilesifyAdmin):
      pass


  # Or using the alternate way:

  class MyConfigModel(FilesifyAdmin):
      pass

  admin.site.register(MyConfigModel, MyConfigModel)





The admin class comes with a custom action to delete selected objects and their associated files on disk.


Single file instance
--------------------

Sometimes, your project only require one single file instance.
In these cases, Django Filesify can be used in conjunction with
`Django Solo <https://github.com/lazybird/django-solo>`__,
a third-party app that helps dealing with singleton database model.

To achieve this, install Django Solo and use it together with Filesify
in your models and your admin classes.


**Singleton models:**

::

  from django.db import models
  from django_solo.models import SingletonModel
  from filesify.models import Filesify

  class MyConfigModel(SingletonModel, Filesify):
      class Meta:
          verbose_name = "Some Config File"
          verbose_name_plural = "Some Config File"


**Singleton admin:**

::

  from django.contrib import admin
  from django_solo.admin import SingletonModelAdmin
  from filesify.admin import FilesifyAdmin

  from my_app.models import MyConfigModel

  @admin.register(MyConfigModel)
  class MyConfigModelAdmin(SingletonModelAdmin, FilesifyAdmin):
      pass


Filesify on post migrate signal
-------------------------------

Django Filesify provides a mixin class that can be used to create files automatically
after running database migrations.


Usage
~~~~~

::

  from django.apps import AppConfig

  from filesify.mixins import FilesifyPostMigrateMixin


  class MyAppConfig(FilesifyPostMigrateMixin, AppConfig):
      default_auto_field = "django.db.models.BigAutoField"
      name = "my_app"


This will discover all models extended from Filesify abstract model and
will create the corresponding files.

.. _filesify-mixin-limit_to_models:

Limit to models
~~~~~~~~~~~~~~~

If you want to limit the list of models to be looked at, you could
define a list of dotted path models with the
`filesify_limit_to_models` attribute.
If `filesify_limit_to_models`` is None, it calls the management command
with no arguments, considering all models.

::
  
  class MyAppConfig(FilesifyPostMigrateMixin, AppConfig):
      default_auto_field = "django.db.models.BigAutoField"
      name = "my_app"
      filesify_limit_to_models = ["my_app.MyConfigModel"]


Filesify base mixin
--------------------

If you are looking for a mode generic way to generate files from models
that are extended from the Filesify class, you could use the
`filesify.mixins.FilesifyBaseMixin` class.

::

  from my_app.filesify import SomeGenericClass

  something = SomeGenericClass()
  something.filesify_limit_to_models = ['my_app.MyConfigModel1', 'my_app.MyConfigModel2']
  something.create_files()


Notice how you can optionally limit the models that the file creation should look at.


Contribute to Django Filesify
-----------------------------

If you already have a working environnement with django running, you could install
django-filesify in "editable" mode in that receiving project.

Get the package source code somewhere outside your project folders, in this example,
will will use the parent folder.

::

  cd you/working/django/project/

  git clone https://github.com/lazybird/django-filesify.git ../django-filesify/

  or

  git clone git@github.com:lazybird/django-filesify.git ../django-filesify/


Now the code inside ``../django-filesify/`` is where you'll make changes.

You can install the package in then "editable" mode in you working project.
Here we assume you are in you project's virtual environnement.

::

  pip uninstall django-filesify  # just in case you have it already...
  pip install --editable ../django-filesify/



Run tests :

::

  python ../django-filesify/filesify/tests/runtests.py


  pytest ../django-filesify/filesify/tests/tests.py --ds=filesify.tests.settings