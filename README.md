# TechStock — Catálogo de componentes eletrônicos

O TechStock é uma aplicação web simples para consultar e manter um catálogo de componentes eletrônicos. O usuário entra pelo Portal e, na página Banco, pode cadastrar, pesquisar, editar e excluir componentes.

O projeto usa Python e Bottle e mantém a organização em Models, Views e Controllers. Os dados ficam em arquivos JSON dentro de `app/controllers/db/`.

**Aluno:** Abner da Silva Gomes

## Como usar no Windows

1. Baixe o projeto pelo botão **Code → Download ZIP** do GitHub e extraia a pasta, ou clone o repositório.
2. Abra a pasta `techstock-bmvc` no VS Code.
3. Dê dois cliques em `iniciar_techstock.bat`.
4. Na primeira execução, o inicializador cria o ambiente virtual e instala a dependência. Depois, inicia o servidor e abre o navegador.

Também é possível iniciar pelo terminal do VS Code:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py route.py
```

A aplicação fica disponível em **http://127.0.0.1:8080/portal**.

### Primeiro acesso

Na primeira execução, o sistema cria a conta de demonstração:

| Campo | Valor |
|---|---|
| Usuário | `admin` |
| Senha | `1234` |

A senha é armazenada como hash PBKDF2-HMAC-SHA256 com salt individual, não em texto puro. Se a instalação já tinha a senha antiga de demonstração (`techstock123`), ela é atualizada automaticamente para `1234`. Uma senha personalizada diferente é preservada.

> A senha curta é destinada à demonstração local da atividade. Não use essa configuração em um servidor público.

## Usando a página Banco

Depois do login, a página `/banco` mostra os componentes cadastrados e os indicadores de tipos e unidades em estoque.

- **Cadastrar:** preencha o formulário “Adicionar componente” e clique em “Cadastrar componente”.
- **Consultar:** use a lista e o campo de pesquisa por nome ou categoria.
- **Editar:** clique em “Editar” na linha do componente, altere os campos e salve.
- **Excluir:** clique em “Excluir” e confirme a operação.

As alterações são salvas nos arquivos JSON e a página retorna à lista atualizada. Os campos são validados: nome e categoria são obrigatórios, quantidade deve ser um inteiro igual ou maior que zero e a descrição pode ter até 300 caracteres.

## API

As operações também continuam disponíveis pela API, protegidas pela sessão de login:

| Operação | Método e rota |
|---|---|
| CREATE | `POST /componentes` |
| READ | `GET /componentes` ou página `/banco` |
| UPDATE | `PUT /componentes/<id>` |
| DELETE | `DELETE /componentes/<id>` |

A página usa rotas de formulário (`POST /banco/componentes...`) para que o CRUD possa ser feito diretamente pelo navegador. As rotas JSON anteriores foram mantidas para testes e integração.

## Organização do código

```text
techstock-bmvc/
├── route.py
├── iniciar_techstock.bat
├── requirements.txt
├── app/
│   ├── models/
│   │   ├── user_account.py
│   │   ├── componente.py
│   │   └── sessao.py
│   ├── controllers/
│   │   ├── application.py
│   │   ├── datarecord.py
│   │   └── db/
│   ├── views/html/
│   │   ├── layout.tpl
│   │   ├── portal.tpl
│   │   └── banco.tpl
│   └── static/
│       ├── css/style.css
│       └── js/main.js
└── tests/
    ├── test_models.py
    └── test_routes.py
```

| Classe | Responsabilidade |
|---|---|
| `Componente` | Representa um item e valida seus campos. |
| `User_account` | Armazena a conta e confere a senha. |
| `DataRecord` | Classe base para ler e gravar arquivos JSON. |
| `UserRecord` | Carrega e procura contas do Portal. |
| `ComponentRecord` | Realiza as operações sobre os componentes. |
| `GerenciadorSessoes` | Cria, consulta e encerra sessões. |
| `Application` | Reúne os objetos usados pelas páginas. |

## Testes

Para executar os testes automatizados no terminal do VS Code:

```powershell
py -m unittest discover -s tests -v
```

Os testes verificam os modelos, a persistência JSON, o login, o bloqueio de solicitações sem autenticação, a API e as operações pelo formulário da página Banco.

O workflow do GitHub Actions também executa a suíte de testes em Python 3.10, 3.11, 3.12 e 3.13.

## Encerrar

Na janela do inicializador, pressione `Ctrl + C` para parar o servidor. Os registros dos componentes e usuários permanecem salvos em `app/controllers/db/`.
