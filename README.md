📘 Reviu — Sistema de Flashcards

O Reviu é uma aplicação web desenvolvida para facilitar o estudo por meio de flashcards organizados em decks. Com ele, você pode criar seus próprios decks, adicionar perguntas e respostas, revisar conteúdos pendentes e até gerar cartas automaticamente a partir de arquivos PDF. Todo o seu progresso é salvo com segurança graças ao sistema de login e cadastro.

✨ Funcionalidades

📚 Criação de decks: organize seus estudos de forma prática.

📝 Criação e edição de cartas: adicione perguntas e respostas personalizadas.

📄 Geração de cartas a partir de PDFs: transforme conteúdos em flashcards rapidamente.

🔐 Autenticação de usuário: login e cadastro seguro.

🔁 Revisão de cartas pendentes: revise apenas o que ainda precisa reforçar.

🎨 Interface moderna: design clean e responsivo com Tailwind CSS.

🛠 Tecnologias Utilizadas
💻 Back-End (API & Lógica)

Java com Spring Boot – API REST, lógica de negócios e injeção de dependências.
Spring Data JPA – persistência de dados.
Spring Security – autenticação e autorização de usuários.

🗄 Banco de Dados

PostgreSQL – armazenamento seguro e confiável.
Ferramentas de gerenciamento: pgAdmin / DBeaver.


🌐 Front-End / Interface Web

Django – renderização de páginas dinâmicas e roteamento.
Tailwind CSS – estilização utility-first para uma interface moderna.
PyPDF2 – extração e processamento de PDFs para gerar cartas automaticamente.

🛠 Ferramentas de Desenvolvimento
Figma – prototipagem das telas.
Postman – documentação e testes das APIs.
IntelliJ IDEA – desenvolvimento Back-End.
VS Code – desenvolvimento Front-End.
Git/GitHub – controle de versão e colaboração.

🔐 Variáveis de Ambiente

Para rodar o projeto, crie um arquivo chamado .env na pasta principal e configure as variáveis essenciais:

*ENVIRONMENT*
- para execução local deve definido como "development", em produção deve ser alterado para qulaquer outro valor.

Isso permite que o sistema identifique onde está rodando. 🚀

*SECRET_KEY*

Chave de segurança do Django.

Para gerar, execute no terminal (na pasta do manage.py):

python manage.py shell

No shell do Django, digite:

from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())


Copie a chave gerada para o arquivo .env. 
