# Sistema de Login com Autenticação de Dois Fatores (2FA) em Django

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 📜 Descrição

Este projeto é uma aplicação web desenvolvida em Django que implementa um sistema de autenticação de usuários robusto, incluindo cadastro, login/logout e a funcionalidade de **Autenticação de Dois Fatores (2FA)**. A 2FA é implementada usando senhas de uso único baseadas em tempo (TOTP), e os usuários podem ativá-la escaneando um QR Code com um aplicativo autenticador (como Google Authenticator, Authy, etc.).

## ✨ Funcionalidades

- **Cadastro de Usuários:** Permite que novos usuários criem uma conta.
- **Autenticação Segura:** Sistema de login e logout padrão do Django.
- **Autenticação de Dois Fatores (2FA):**
  - Geração de QR Code para fácil configuração em aplicativos autenticadores.
  - Ativação e desativação da 2FA pelo usuário em seu perfil.
  - Verificação do código TOTP durante o processo de login.
- **Gerenciamento de Configurações:** Uso de variáveis de ambiente para proteger informações sensíveis como a `SECRET_KEY`.

## 🛠️ Tecnologias Utilizadas

O projeto foi construído com as seguintes tecnologias e bibliotecas:

- **Backend:**

  - Python 3.13+
  - Django: Framework web principal.
  - django-otp: Framework para adicionar autenticação de dois fatores.
  - pyotp: Biblioteca para gerar e validar senhas de uso único.
  - qrcode: Biblioteca para gerar QR Codes.
  - Pillow: Biblioteca para manipulação de imagens (dependência do `qrcode`).
  - python-decouple: Para gerenciar as configurações do projeto de forma separada do código.

- **Gerenciador de Pacotes:**
  - uv: Um instalador e resolvedor de pacotes Python extremamente rápido.

## 🚀 Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos

- Python 3.13 ou superior.
- Git para clonar o repositório.
- (Opcional, mas recomendado) uv instalado. Se não, você pode usar `pip`.

### Passos

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/seu-usuario/login_django.git
    cd login_django
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    # Usando uv
    uv venv
    source .venv/bin/activate  # No Windows: .venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    O arquivo `uv.lock` garante que as mesmas versões de pacotes sejam instaladas.

    ```bash
    uv sync
    ```

4.  **Configure as variáveis de ambiente:**
    Crie um arquivo `.env` na raiz do projeto ou configure as variáveis de ambiente do sistema.

    **Configuração Básica:**

    ```ini
    # .env
    SECRET_KEY='sua-chave-secreta-super-segura-aqui'
    ```

    **Configuração de Email (Opcional - para produção):**
    Para enviar emails reais (como recuperação de senha), configure as seguintes variáveis:

    ```ini
    # .env
    EMAIL_HOST_USER=seu@email.com
    EMAIL_HOST_PASSWORD=sua_senha_app  # Para Gmail, use "Senha de App"
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    ```

    **Nota:** Se as credenciais de email não estiverem configuradas, o sistema usará o backend de console (emails aparecerão no terminal). Isso é útil para desenvolvimento.

5.  **Aplique as migrações do banco de dados:**

    ```bash
    python manage.py migrate
    ```

6.  **Crie um superusuário (opcional):**
    Isso é útil para acessar o painel de administração do Django.

    ```bash
    python manage.py createsuperuser
    ```

7.  **Inicie o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

Acesse a aplicação em seu navegador em `http://127.0.0.1:8000`.

---
