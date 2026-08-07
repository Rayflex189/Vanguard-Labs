from django.apps import AppConfig

class ProposalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'proposals'

    def ready(self):
        # Load signals to register handlers
        import proposals.signals
