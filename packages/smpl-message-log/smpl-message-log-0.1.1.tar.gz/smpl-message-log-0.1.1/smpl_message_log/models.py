
import markdown

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation

__all__ = [
    'MessageLog',
    'MessageLogs'
]


class MessageLogManager(models.Manager):

    def _add_message(self, level, message):
        return MessageLog.objects.create(
            level=level,
            message=message,
            content_type=self.content_type,
            object_id=self.pk_val
        )

    def info(self, message):
        return self._add_message(self.model.INFO, message)

    def debug(self, message):
        return self._add_message(self.model.DEBUG, message)

    def warning(self, message):
        return self._add_message(self.model.WARNING, message)

    def error(self, message):
        return self._add_message(self.model.ERROR, message)

    def critical(self, message):
        return self._add_message(self.model.CRITICAL, message)

    def success(self, message):
        return self._add_message(self.model.SUCCESS, message)


class MessageLog(models.Model):

    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    SUCCESS = 'SUCCESS'
    CRITICAL = 'CRITICAL'

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, db_index=True)
    object_id = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    level = models.CharField(max_length=100)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    content_object = GenericForeignKey()
    objects = MessageLogManager()

    class Meta:
        default_permissions = ()
        ordering = ('-created',)

    def __str__(self):
        return self.message

    def as_html(self):
        return markdown.markdown(self.message)


class MessageLogs(GenericRelation):

    def __init__(self, **kwargs):
        super().__init__(MessageLog, **kwargs)
