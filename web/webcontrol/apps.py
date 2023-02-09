from django.apps import AppConfig

class WebcontrolConfig(AppConfig):
    name = 'webcontrol'
    def ready(self) -> None:
        open("backup.txt", "w").close()

        return super().ready()