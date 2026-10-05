# SIGAE – Sistema Inteligente de Gestão de Ativos e Empréstimos

## Rodando
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# MySQL: CREATE DATABASE sigae CHARACTER SET utf8mb4;  (exporte as variáveis de .env.example)
python manage.py makemigrations core   # já incluída; rode se alterar models
python manage.py migrate
python manage.py seed
python manage.py runserver
```
Usuários do seed (senha `sigae@2026`): `admin.sigae`, `instrutor.a`, `instrutor.b`, `aluno01`…`aluno15`.
Para testar sem MySQL: `DB_ENGINE=sqlite python manage.py migrate`.
