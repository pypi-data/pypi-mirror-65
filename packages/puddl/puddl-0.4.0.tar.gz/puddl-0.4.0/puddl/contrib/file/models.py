import logging
from pathlib import Path

from django.db import models
from django.contrib.postgres.fields import JSONField
import filetype

from puddl.fields import PathField
from puddl.models import Datum, Device

log = logging.getLogger(__name__)


class FileManager(models.Manager):

    def upsert(self, device: Device, path: Path):
        path = Path(path)
        try:
            instance = self.get(device=device, path=path)
            log.debug(f'found {instance}')
        except self.model.DoesNotExist:
            instance = self.model()
            instance.device = device
            instance.path = path
            log.debug(f'created {instance}')
        instance.filetype = instance.guess_filetype()
        instance.stat = instance.get_stat()
        instance.save()
        return instance


class File(Datum):
    objects = FileManager()

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    path = PathField()

    filetype = JSONField(null=True)
    stat = JSONField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['device', 'path'],
                name='unique_device_path',
            )
        ]

    @property
    def ssh_path(self):
        return f'{self.device.name}:{self.path}'

    def __str__(self):
        return self.ssh_path

    def guess_filetype(self):
        x = filetype.guess(str(self.path))
        if x is not None:
            return {
                "extension": x.extension,
                "mime": x.mime
            }

    def get_stat(self):
        s = self.path.stat()
        attrs = [a for a in dir(s) if a.startswith('st_')]
        return {a: getattr(s, a) for a in attrs}
