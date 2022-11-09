# Migrate
    Simple project to migrate MongoDB database collections to postgresSQL

---
## Requisitos
![https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white) ![https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white) ![https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

- Python 3.X +
- MongoDB 5.x +
- Postgres 
- Instalar as dependências de acordo com o arquivo "requirements.txt"

## Configuração


- Preencher um arquivo JSON com o nome "config.json", seguindo o modelo do arquivo "config_modelo.json, onde:

    - tables:
        São as collections que devem ser migradas do mongo para o postgres. O nome das tabelas no postgres será o mesmo
    - mongo:
        Informações de conexão ao banco mongo. 
        URI = string de conexão;
        database = nome do banco de dados;
        new_collections: documentos que podem ser inseridos no banco mongo via json antes de migrar para o postgres
    
    - postgres: Informações de conexão ao banco postgres


## Usando o projeto

Para rodar o projeto basta rodar o script via CLI ou usando a IDE de sua preferência.