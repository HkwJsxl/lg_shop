from django.db import models


class Areas(models.Model):
    name = models.CharField(max_length=32, verbose_name="区划名称")
    pid = models.ForeignKey("self", related_name="subs", on_delete=models.SET_NULL,
                            null=True, blank=True, verbose_name="父级id")

    class Meta:
        db_table = "lg_areas"
        verbose_name = "三级区域"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
