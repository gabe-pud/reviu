# 📘Reviu — Sistema de Flashcards 

O Reviu é uma aplicação web desenvolvida para facilitar o estudo por meio de flashcards organizados em decks. Com ele, você pode criar seus próprios decks, adicionar perguntas e respostas, revisar conteúdos pendentes e até gerar cartas automaticamente a partir de arquivos PDF. Todo o seu progresso é salvo com segurança graças ao sistema de login e cadastro.

---
### 📁 Repositorio Back-End
```bash
https://github.com/thialms/reviu-backend
```

 ## ✨ Funcionabilidades

- 📚 Criação de decks: organize seus estudos de forma prática.

- 📝 Criação e edição de cartas: adicione perguntas e respostas personalizadas.

- 📄 Geração de cartas a partir de PDFs: transforme conteúdos em flashcards rapidamente.

- 🔐 Autenticação de usuário: login e cadastro seguro.

- 🔁 Revisão de cartas pendentes: revise apenas o que ainda precisa reforçar.

- 🎨 Interface moderna: design clean e responsivo com Tailwind CSS.

--- 

# 🛠 Tecnologias Utilizadas

- 💻 Back-End (API & Lógica)

- Java com Spring Boot – API REST, lógica de negócios e injeção de dependências.

- Spring Data JPA – persistência de dados.

- Spring Security – autenticação e autorização de usuários.

# 🗄 *Banco de dados*

- PostgreSQL – armazenamento seguro e confiável.
- Ferramentas de gerenciamento: pgAdmin / DBeaver.

_______________________________________________________
# 🌐 *Front-end / Interface Web*

- Django – renderização de páginas dinâmicas e roteamento.

- Tailwind CSS – estilização para uma interface moderna.
_______________________________________________________
# 🛠 *Ferramentas de Desenvolvimento*
- Figma – prototipagem das telas.

- Postman – documentação e testes das APIs.

- IntelliJ IDEA – desenvolvimento Back-End.

- VS Code – desenvolvimento Front-End.

- Git/GitHub – controle de versão e colaboração.
_______________________________________________________
# 🔐 Variaveis de Ambiente

### 📥 1. Clone o repositório
```bash
git clone https://github.com/gabe-pud/reviu
```
### ⚙ 2. Configure as variáveis de ambiente  

crie um arquivo ".env" na pasta base do projeto e adicione estas variáveis:

- ENVIRONMENT
    - para execução local deve definido como "development", em produção deve ser alterado para qulaquer outro valor.

- SECRET_KEY

    para gerar uma secret key do djnago:

    - no terminal navegue até a pasta em que o arquivo "manage.py" se encontra
    - execute:
        ```
        python manage.py shell
        ```

    - e após o shell ser iniciado utilize esta sequencia
        ```
        from django.core.management.utils import get_random_secret_key
        print(get_random_secret_key())
        ```
    - ao rodar a ultima linha será exibido no console a chave que pode ser copiada para .env

    - para sair do shell apenas pressione **ctrl+z** e depois **enter**
---

# 🏅 Créditos

Desenvolvido por:
✨ **André Luiz Dantas**
✨ **Gabriel Garcia Santana**

Com colaboração de:
🔥☕ **Levi Ferreira**
🔥☕ **Thiago de Almeida Silva**
(Equipe de Back-end)

---
