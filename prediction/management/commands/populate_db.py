import json

from django.core.management.base import BaseCommand

from prediction.models import HealthCenter


class Command(BaseCommand):
    help = 'python manage.py populate_db static/data/unidadessaude.json'
    
    def add_arguments(self, parser):
        parser.add_argument('source_path', nargs=1, type=str)

    def _create_health_units(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
        
        health_centers = []
        
        for d in data:
            center_name, latitude, longitude = d['no_fantasia'], d['lat'], d['long']
            health_centers.append(
                HealthCenter(center_name=center_name, latitude=latitude, longitude=longitude)
            )
        
        HealthCenter.objects.bulk_create(health_centers)

        self.stdout.write("Unidades de saúde cadastradas")

    def handle(self, *args, **options):
        path = options['source_path'][0]
        self._create_health_units(path)