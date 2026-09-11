# StoksMaster

Sistema de controle de estoque com autenticacao de usuarios, organizacao por lojas e gerenciamento de produtos.

## Funcionalidades

- Login e cadastro de lojas e usuarios.
- Area de estoque protegida em `/estoque`.
- Produtos separados por loja do usuario autenticado.
- Cadastro e edicao de produtos em modal.
- Exclusao com confirmacao.
- Categorias pre-definidas e pesquisa por nome, categoria ou ID.
- Imagens exibidas sem deformacao.
- Interface responsiva.

## Tecnologias

- Backend: Python, FastAPI, Uvicorn, SQLAlchemy, MySQL e PyMySQL.
- Seguranca: JWT com `python-jose` e senhas com Passlib/bcrypt.
- Frontend: React, Vite, Axios e CSS responsivo.

## Estrutura

```text
stoksmaster/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   └── main.py
│   ├── .env
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── index.html
│   └── package.json
└── README.md
```

## Pre-requisitos

- Python 3.13 ou superior
- Node.js e npm
- MySQL Server rodando em `localhost:3306`

O ambiente atual usa o usuario MySQL `root`, com senha `root`.

## Banco de dados

O arquivo `backend/.env` usa:

```env
DATABASE_URL=mysql+pymysql://root:root@localhost:3306/stoksMaster
SECRET_KEY=stoksmaster-secret-key-change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Na primeira inicializacao, o backend cria automaticamente o banco `stoksMaster` e as tabelas `stores`, `users` e `products`.

Para ambientes reais, altere as credenciais e nunca compartilhe a `SECRET_KEY`.

## Instalar e executar o backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API: `http://localhost:8000`

## Instalar e executar o frontend

Em outro terminal:

```powershell
cd frontend
npm install
npm run dev -- --host 127.0.0.1
```

Frontend: `http://127.0.0.1:5173`

## Fluxo da aplicacao

1. Acesse `/` para abrir o login.
2. Use **Criar uma conta** ou acesse `/cadastro` para cadastrar uma loja.
3. Depois do login, o sistema redireciona para `/estoque`.
4. Sem token valido, `/estoque` mostra a tela de login.
5. Use **+ Novo produto** para abrir o cadastro em modal.
6. Use os icones de editar e excluir na tabela.
7. O botao **Sair** remove a sessao e retorna para `/`.

## Rotas da API

### Autenticacao

| Metodo | Rota | Protecao | Descricao |
| --- | --- | --- | --- |
| POST | `/auth/register` | Publica | Cria loja e usuario |
| POST | `/auth/login` | Publica | Gera token JWT |
| POST | `/auth/login-form` | Publica | Login no formato OAuth2 |
| GET | `/auth/me` | Bearer token | Retorna usuario e loja atual |

### Produtos

Todas as rotas de produtos exigem:

```http
Authorization: Bearer SEU_TOKEN
```

| Metodo | Rota | Descricao |
| --- | --- | --- |
| GET | `/products/` | Lista produtos da loja atual |
| POST | `/products/` | Cria produto |
| PUT | `/products/{product_id}` | Atualiza produto |
| DELETE | `/products/{product_id}` | Exclui produto |

Exemplo de produto:

```json
{
	"name": "Refrigerante",
	"image": "https://exemplo.com/imagem.png",
	"category": "Bebidas",
	"price": 5.40,
	"quantity": 10
}
```

### Lojas

| Metodo | Rota | Protecao | Descricao |
| --- | --- | --- | --- |
| GET | `/stores/` | Publica | Lista lojas |
| POST | `/stores/` | Bearer token | Cria loja |

## Documentacao e verificacao

Com a API em execucao:

- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`

Para gerar o build de producao:

```powershell
npm --prefix frontend run build
```

## Observacoes

- O nome tecnico do banco e `stoksMaster`.
- O nome visual da aplicacao e `Stocks Master`.
- Cada produto pertence a uma loja e so e acessivel por usuarios daquela loja.
- O token de sessao fica no navegador com a chave `stoksmaster_token`.
PS C:\Users\lucas\OneDrive\Documentos\sla> git push -u origin main(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& C:\Users\lucas\Envs\sql_model\Scripts\Activate.ps1)
error: src refspec main does not match any
error: failed to push some refs to 'https://github.com/Lucas-Bonfim80/StoksMaster.git'
(sql_model) PS C:\Users\lucas\OneDrive\Documentos\sla> 
