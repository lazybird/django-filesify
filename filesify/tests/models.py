from filesify.models import Filesify


class MyConfigModel(Filesify):

    class Meta:
        verbose_name = "Some config file"
        verbose_name_plural = "Some config files"
