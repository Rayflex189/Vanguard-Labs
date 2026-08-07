from django.apps import AppConfig

class ProjectsManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects_management'

    def ready(self):
        # Import signals to register them
        import projects_management.signals
