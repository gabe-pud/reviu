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

- ENVIRONMENT
    - para execução local deve definido como "development", em produção deve ser alterado para qulaquer outro valor.

- SECRET_KEY

    para gerar uma secret key do djnago:

    - no terminal navegue até a pasta em que o arquivo "manage.py" se encontra
    - execute:
        
        python manage.py shell
        

    - e após o shell ser iniciado utilize esta sequencia
        
        from django.core.management.utils import get_random_secret_key
        print(get_random_secret_key())
        
    - ao rodar a ultima linha será exibido no console a chave que pode ser copiada para .env

    - para sair do shell apenas pressione *ctrl+z* e depois *enter*


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



