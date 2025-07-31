import requests

from django.core.management.base import BaseCommand
from django.db import transaction

from regions.models import (
    Region,
    Mesoregion,
    Microregion,
    IntermediateRegion,
    ImmediateRegion,
    State,
    Municipality,
    District
)

class Command(BaseCommand):
    help = 'importar dados do IBGE e popular o banco de dados'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Importação dos dados do IBGE'))

        try:
            with transaction.atomic():
                self.api_request()

                self.import_states()
                self.import_municipalities()
                self.import_districts()
            
                self.stdout.write(self.style.SUCCESS('Dados importados com sucesso!'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Falha na importação: {e}"))
            raise e
        
    def api_request(self):
        self.state_data = self.get_IBGE_data('estados')
        self.municipality_data = self.get_IBGE_data('municipios')
        self.district_data = self.get_IBGE_data('distritos')
    
    def get_IBGE_data(self, url):
        response = requests.get(f'https://servicodados.ibge.gov.br/api/v1/localidades/{url}')
        
        if response.status_code != 200:
            raise Exception(f"Falha ao acessar {url}. Status: {response.status_code}")
        return response.json()
    
    def import_states(self):
        self.stdout.write(self.style.NOTICE('Salvando dados de Estados.....'))

        for state in self.state_data:

            region = state.get('regiao')

            Region.objects.update_or_create(
                id=region['id'],
                defaults={
                    'name': region['nome'],
                    'acronym': region['sigla']
                }
            )

            State.objects.update_or_create(
                id=state['id'],
                defaults={
                    'name': state['nome'],
                    'acronym': state['sigla'],
                    'region_id': region['id']
                }
            )

    def import_municipalities(self):
        self.stdout.write(self.style.NOTICE('Salvando dados de Municipios.....'))

        for municipality in self.municipality_data:
            microregion = municipality.get('microrregiao')
            mesoregion = microregion.get('mesorregiao') if microregion else None
            immediate_region_data = municipality.get('regiao-imediata')
            intermediate_region_data = municipality.get(
                'regiao-imediata', {}
                ).get('regiao-intermediaria')

            if mesoregion:
                Mesoregion.objects.update_or_create(
                    id=mesoregion['id'],
                    defaults={
                        'name': mesoregion['nome'],
                        'state_id': mesoregion['UF']['id']
                    }
                )

            if microregion:
                Microregion.objects.update_or_create(
                    id=microregion['id'],
                    defaults={
                        'name': microregion['nome'],
                        'mesoregion_id': mesoregion['id'] if mesoregion else None
                    }
                )

            if intermediate_region_data:
                IntermediateRegion.objects.update_or_create(
                    id=intermediate_region_data['id'],
                    defaults={
                        'name': intermediate_region_data['nome'],
                        'state_id': intermediate_region_data['UF']['id']
                    }
                )

            if immediate_region_data:
                ImmediateRegion.objects.update_or_create(
                    id=immediate_region_data['id'],
                    defaults={
                        'name': immediate_region_data['nome'],
                        'intermediate_region_id': intermediate_region_data['id'] if intermediate_region_data else None
                    }
                )

            Municipality.objects.update_or_create(
                id=municipality['id'],
                defaults={
                    'name': municipality['nome'],
                    'microregion_id': microregion['id'] if microregion else None,
                    'immediate_region_id': immediate_region_data['id'] if immediate_region_data else None
                }
            )
  

    def import_districts(self):
        self.stdout.write(self.style.NOTICE('Salvando dados de Distritos.....'))

        for district in self.district_data:
            District.objects.update_or_create(
                id=district['id'],
                defaults={
                    'name': district['nome'],
                    'municipality_id': district['municipio']['id']
                }
            )

