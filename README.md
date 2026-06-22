# Bichinhos da Memória

Projeto em Flask com persistência SQLite (SQLAlchemy), Docker e endpoints extras.

Como rodar localmente:

1. Clone o repositório e entre na pasta:

   git clone https://github.com/samuelbossolaniofficial-coder/bichinhos.da.memoria.git
   cd bichinhos.da.memoria

2. Crie e ative virtualenv:

   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate

3. Instale dependências:

   pip install -r requirements.txt

4. Rode a aplicação:

   python src/app.py

A API estará em http://localhost:5000

Endpoints:
- GET / -> status
- GET /pets -> lista todos os bichinhos
- GET /pets/<id> -> obtém um bichinho
- POST /pets -> cria um bichinho (JSON: {"name":"...", "memory": ["m1","m2"]})
- DELETE /pets/<id> -> remove um bichinho
- GET /pets/<id>/memories -> lista memórias do bichinho
- POST /pets/<id>/memories -> adiciona memória (JSON: {"memory":"texto"})
- PUT /pets/<id>/memories/<mem_id> -> atualiza memória
- DELETE /pets/<id>/memories/<mem_id> -> remove memória

Rodando com Docker:

1. Build e run:
   docker build -t bichinhos-app .
   docker run -p 5000:5000 bichinhos-app

2. (Opcional) docker-compose:
   docker-compose up --build

Observações:
- O banco é um arquivo SQLite (data.db) criado automaticamente na primeira execução.
