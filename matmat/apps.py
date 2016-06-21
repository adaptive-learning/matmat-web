from django.apps import AppConfig as OAppConfig
from proso.django.enrichment import register_object_type_enricher


class AppConfig(OAppConfig):

    name = 'matmat'

    def ready(self):
        from matmat.prediction import enrich_mean_time
        register_object_type_enricher(['question'], enrich_mean_time)
