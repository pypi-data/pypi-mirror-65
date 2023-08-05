
from django.apps import AppConfig


class MessageLogConfig(AppConfig):

    name = 'smpl_message_log'
    verbose_name = 'Лог сообщений'

    def ready(self):
        pass
