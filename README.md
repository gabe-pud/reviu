📘 Reviu — Sistema de Flashcards

O Reviu é uma aplicação web desenvolvida para facilitar o estudo por meio de flashcards organizados em decks.
Você cria seus decks, adiciona perguntas e respostas, revisa conteúdos pendentes e ainda pode gerar cartas automaticamente a partir de arquivos PDF.
O sistema também conta com login e cadastro para salvar todo o seu progresso.

✨ Funcionalidades

📚 Criação de decks
📝 Criação e edição de cartas
📄 Geração de cartas a partir de PDFs
🔐 Autenticação de usuário (login e cadastro)
🔁 Revisão de cartas pendentes
🎨 Interface moderna utilizando TailwindCSS

🔧 Tecnologias Utilizadas
Python (Django)
HTML + TailwindCSS
Django Templates
SQLite


🔐 Variáveis de Ambiente
Crie um arquivo .env na pasta base do projeto e adicione estas variáveis:

ENVIRONMENT

Para execução local:

ENVIRONMENT=development


Em produção deve ser qualquer outro valor:

ENVIRONMENT=production

SECRET_KEY

Para gerar uma secret key do Django:

No terminal, navegue até a pasta onde o arquivo manage.py se encontra

Execute:

python manage.py shell


Após o shell iniciar, execute:

from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())


Copie a chave exibida e cole no .env:

SECRET_KEY=sua_chave_gerada


Para sair do shell pressione Ctrl + Z e depois Enter

▶️ Como Rodar o Projeto
1. Instale as dependências
pip install -r requirements.txt

2. Aplique as migrações
python manage.py migrate

3. Rode o servidor
python manage.py runserver

4. Acesse no navegador:
http://127.0.0.1:8000/


└── README.md
