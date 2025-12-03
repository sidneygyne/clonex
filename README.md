# 📱 Clonex - Rede Social Django

Clonex é uma aplicação web desenvolvida com **Python/Django** que implementa uma rede social simples, atendendo aos requisitos de autenticação, perfil, seguidores, feed e interações.

---

## 🚀 Funcionalidades

### 🔐 Autenticação
- Registro de novos usuários com validação de senha.
- Login e logout seguros.
- Modal de confirmação após criação de conta.

### 👤 Perfil
- Alteração opcional de foto de perfil, nome e senha.
- Nenhuma alteração é obrigatória.

### 🤝 Seguir e Feed
- Possibilidade de seguir outros usuários.
- Listagem de seguidores e seguidos.
- Feed exibe apenas postagens das pessoas seguidas.

### ❤️ Interações
- Curtidas em postagens.
- Comentários com atualização dinâmica via AJAX.

---

## 🛠️ Tecnologias

- **Back-end:** Django (Python)
- **Banco de dados:** SQLite (padrão, pode ser substituído por PostgreSQL)
- **Front-end:** Templates Django + Bootstrap 5
- **Deploy:** PythonAnywhere

---

## 📦 Instalação e uso

### 1. Clone o repositório
```bash
git clone https://github.com/sidneygyne/clonex.git
cd clonex

### 2. Crie e ative o ambiente virtual
bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

### 3. Instale as dependências
bash
pip install -r requirements.txt

### 4. Execute migrações
bash
python manage.py migrate

### 5. Crie um superusuário
bash
python manage.py createsuperuser

### 6. Rode o servidor
bash
python manage.py runserver
Acesse em: http://localhost:8000