# Bichinhos da Memória

Projeto mínimo em Flask para gerenciar "bichinhos" e suas memórias.

Como rodar localmente:

1. Clone o repositório e entre na pasta:

   git clone https://github.com/samuelbossolaniofficial-coder/bichinhos.da.memoria.git
   cd bichinhos.da.memoria

2. Crie um virtualenv e ative:

   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate

3. Instale dependências:

   pip install -r requirements.txt

4. Rode a aplicação:

   python src/app.py

A API estará em http://localhost:5000

Endpoints principais:
- GET / -> status da API
- GET /pets -> lista todos os bichinhos
- GET /pets/<id> -> obtém um bichinho
- POST /pets -> cria um bichinho (JSON: {"name":"..."})
- POST /pets/<id>/memories -> adiciona uma memória (JSON: {"memory":"texto"})
