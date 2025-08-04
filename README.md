## Instalação e configuração do ambiente
o projeto depende do Poetry para seu gerenciamento e precisa ser devidamente instalado e configurado.


Para instalar o poetry execute em ordem os comandos:
```
pip install --user pipx
pipx install poetry
poetry python install 3.13
poetry env use 3.13
poetry self add poetry-plugin-shell
```

Para ativar o ambiente:
```
poetry shell
```

Com o ambiente ativado basta instalar as dependencias co o comando:
```
poetry install
```

## Subindo banco no docker
O projeto esta configurado com um banco de testes para o PostgreSQL, que pode ser baixado viar docker
```
docker run --name test_db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=test_db -p 5432:5432 -d postgres:15

```

## Executando aplicação
Para poder executar o projeto pela primeira vez é necessario executar os comandos abaixo

Para criar o banco de dados e aplicar as migrações inciais 
```
python manage.py migrate
```

Criar um usuario do tipo administrador
```
python manage.py createsuperuser
```

Popular o banco com os dados do IBGE
```
python manage.py ibge_import
```
Popular o banco com os dados de empresas
```
Adcione o arquivo CSV para a pasta imports
python manage.py companies_import
```

Executar o servidor de desenvolvimento
```
python manage.py runserver
```

## Comandos basicos
O projeto se utiliza da ferramenta task para criar scripts com os comandos fundamentais que podem ser vistos abaixo:

- **`task run`**  
  Executa o servidor de desenvolvimento.
- **`task makemigrations`**  
  Cria os arquivos de de migration do projeto.
- **`task migrate`**  
  Executa as migrations no banco de dados.
- **`task ibge`**  
  Popular ou atualiza o banco com os dados do IBGE.
- **`task companies`**  
  Popular ou atualiza o banco com os dados de empresas.