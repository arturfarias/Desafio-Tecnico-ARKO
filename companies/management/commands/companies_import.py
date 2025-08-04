import glob, os
import pandas
import sys
import shutil
import psutil

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import connection


from companies.models import Company


class Command(BaseCommand):
    help = 'importar dados do csv de empresas e popular o banco de dados'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Importação dos dados de empresas'))

        try:
            with transaction.atomic():
                self.open_csv()
                self.import_companies()

                self.stdout.write(self.style.SUCCESS('Dados importados com sucesso!'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Falha na importação: {e}"))
            raise e
        
    def open_csv(self):
        self.stdout.write(self.style.NOTICE('Processando dados do CSV'))
        temp_dir = os.path.join(settings.BASE_DIR, 'imports', 'tmp')

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir, exist_ok=True)

        chunk_number = 1

        files = glob.glob(os.path.join(settings.BASE_DIR, 'imports', '*'))

        if not files:
            raise Exception("Nenhum arquivo CSV encontrado na pasta 'imports'.")

        for chunk in pandas.read_csv(
            files[0],
            sep=';',
            dtype=str,
            encoding='latin-1',
            header=None,
            chunksize=1000000
        ):
            
            chunk.columns = [
            'cnpj', 'name', 'legal_nature', 'qualification',
            'capital', 'size', 'federative_entity'
            ]

            chunk['capital'] = chunk['capital'].str.replace(
                ',',
                '.',
                regex=False
            ).fillna('0').astype(float)
            
            chunk['cnpj'] = chunk['cnpj'].str.zfill(14)

            chunk_file = os.path.join(temp_dir, f'chunk_{chunk_number}.csv')
            chunk.to_csv(chunk_file, index=False, header=False)
            
            print(f"Chunk {chunk_number} salvo: {chunk_file}")
            chunk_number += 1

            
    def import_companies(self):
        self.stdout.write(self.style.NOTICE('Importando empresas'))

        Company = apps.get_model('companies', 'Company')
        table_name = Company._meta.db_table

        temp_dir = os.path.join(settings.BASE_DIR, 'imports', 'tmp')
        chunk_files = sorted(glob.glob(os.path.join(temp_dir, 'chunk_*.csv')))

        if not chunk_files:
            raise Exception("Nenhum chunk encontrado para importar.")
        
        total_chunks = len(chunk_files)
        
        for i, file in enumerate(chunk_files, start=1):
            with connection.cursor() as cursor:

                cursor.execute("DROP TABLE IF EXISTS temp_companies;")
                cursor.execute(f"""
                    CREATE TEMP TABLE temp_companies
                    ON COMMIT DROP
                    AS SELECT * FROM {table_name} LIMIT 0;
                """)

                with open(file, 'r', encoding='utf-8') as f:
                    cursor.copy_expert(
                        "COPY temp_companies FROM STDIN WITH CSV DELIMITER ',' QUOTE '\"'",
                        f
                    )
                
                cursor.execute(f"""
                    INSERT INTO {table_name} (cnpj, name, legal_nature, qualification, capital, size, federative_entity)
                    SELECT cnpj, name, legal_nature, qualification, capital, size, federative_entity
                    FROM temp_companies
                    ON CONFLICT (cnpj) DO UPDATE
                    SET name = EXCLUDED.name,
                        legal_nature = EXCLUDED.legal_nature,
                        qualification = EXCLUDED.qualification,
                        capital = EXCLUDED.capital,
                        size = EXCLUDED.size,
                        federative_entity = EXCLUDED.federative_entity;
                """)

                print(f"Chunk {i}/{total_chunks} importado com sucesso")

        


