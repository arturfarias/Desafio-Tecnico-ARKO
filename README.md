## Instalação e configuração do ambiente via poetry
O projeto depende do Poetry para seu gerenciamento e precisa ser devidamente instalado e configurado.

Para instalar o poetry execute em ordem os comandos:
```
sudo apt install pipx

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

## Instalação e configuração do ambiente via pip
Caso não queria utilizar o poetry segue a lista de dependencias a serem baixadas via pip
```
python3 -m venv .venv
source .venv/bin/activate

pip install django
pip install psycopg2-binary
pip install requests
pip install pandas
```


## Subindo banco no docker
O projeto esta configurado com um banco de testes para o PostgreSQL, que pode ser baixado viar docker
```
docker run --name test_db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=test_db -p 5432:5432 -d postgres:15
```
Caso deseje usar outras configurações do banco os dados cadastraos são:
```
'NAME': 'test_db',
'USER': 'user',
'PASSWORD': 'password',
'HOST': 'localhost',
'PORT': '5432',
```
Tambem pode ser configurado em config/settings.py na linha 78
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_db',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Template
Para o css extraia dentro da pasta assets o arquivo zip denomidado template, dentro desta pasta deve ficar duas pastas, umas demoninada css e outra vendors

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

Criando um usuario para logar no sistema
```
python manage.py createsuperuser
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

## Imagens do projeto
<div style="display: flex; gap: 10px; flex-wrap: wrap;">
  <img src="https://github.com/arturfarias/Desafio-Tecnico-ARKO/blob/main/img/img1.png" width="150" alt="Imagem 1" />
  <img src="https://github.com/arturfarias/Desafio-Tecnico-ARKO/blob/main/img/img2.png" width="150" alt="Imagem 2" />
  <img src="https://github.com/arturfarias/Desafio-Tecnico-ARKO/blob/main/img/img3.png" width="150" alt="Imagem 3" />
  <img src="https://github.com/arturfarias/Desafio-Tecnico-ARKO/blob/main/img/img4.png" width="150" alt="Imagem 4" />
  <img src="https://github.com/arturfarias/Desafio-Tecnico-ARKO/blob/main/img/img5.png" width="150" alt="Imagem 5" />
</div>
