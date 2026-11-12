# TechStock — Catálogo de componentes eletrônicos

Este projeto foi feito para a atividade de BMVC. A ideia foi montar um sistema simples para organizar alguns componentes eletrônicos, com uma tela de login e uma página para consultar o que está cadastrado.

O sistema usa Python e Bottle e está separado em Model, View e Controller (MVC). Não é a proposta de ser um sistema completo de almoxarifado; ele serve para colocar em prática a estrutura pedida na atividade e mostrar as operações do CRUD.

**Aluno:** Abner da Silva Gomes

## Como o sistema está dividido

Há dois recursos principais:

- **Portal:** é a tela de login. A conferência do usuário e da senha é feita pelo modelo `User_account`.
- **Banco:** é a página que aparece depois do login. Nela fica a lista dos componentes cadastrados. É também onde acontece a operação **READ**, como foi pedido.

O modelo `Componente` guarda cinco informações: ID, nome, categoria, quantidade e descrição.

As outras operações são feitas pelo terminal Linux com cURL:

| Operação | Como é feita |
|---|---|
| CREATE | `POST /componentes` |
| READ | página `/banco`, no navegador |
| UPDATE | `PUT /componentes/<id>` |
| DELETE | `DELETE /componentes/<id>` |

## Organização das classes

A estrutura das pastas segue a divisão MVC. Dentro dela, as classes têm funções diferentes:

| Classe | Função |
|---|---|
| `Componente` | Guarda os dados de cada item e valida os campos. |
| `User_account` | Guarda os dados da conta e confere a senha. |
| `DataRecord` | Classe abstrata que serve de base para ler e gravar os arquivos JSON. |
| `UserRecord` | Cuida das contas cadastradas e consulta o usuário usado no login. |
| `ComponentRecord` | Cuida da lista de componentes e das operações do CRUD. |
| `GerenciadorSessoes` | Cria, consulta e encerra as sessões de login. |
| `Application` | Reúne os objetos usados pelo sistema e prepara as páginas. |

Também aparecem alguns conceitos de orientação a objetos que foram trabalhados na disciplina:

- **Herança:** `UserRecord` e `ComponentRecord` herdam de `DataRecord`.
- **Polimorfismo:** cada uma dessas classes implementa seu próprio método `converter()`, transformando os dados do JSON no objeto correspondente.
- **Encapsulamento:** as validações e operações de cada tipo de dado ficam organizadas dentro de suas próprias classes.
- **Composição:** a classe `Application` utiliza os records e o gerenciador de sessões para montar o funcionamento do sistema.
- **Métodos estáticos e de classe:** os modelos usam `@staticmethod` nas validações e `@classmethod` na criação e recuperação dos objetos.
- **Serialização:** os métodos `to_dict()` e `from_dict()` permitem salvar e recuperar os objetos usando arquivos JSON.

## Arquivos do projeto

A organização ficou assim:

```text
TechStock-BMVC/
├── .gitignore
├── route.py
├── requirements.txt
├── curl_exemplos.sh
├── README.md
├── app/
│   ├── models/
│   │   ├── user_account.py
│   │   ├── componente.py
│   │   └── sessao.py
│   ├── controllers/
│   │   ├── application.py
│   │   ├── datarecord.py
│   │   └── db/
│   │       ├── .gitkeep
│   │       ├── user_accounts.json  # aparece na primeira execução
│   │       └── componentes.json    # aparece na primeira execução
│   ├── views/html/
│   │   ├── layout.tpl
│   │   ├── portal.tpl
│   │   └── banco.tpl
│   └── static/
│       ├── css/style.css
│       └── js/main.js
├── tests/
│   ├── test_models.py
│   └── test_routes.py
└── .github/
    └── workflows/
        └── tests.yml
```

## O que é preciso para rodar

- Linux (Ubuntu, Debian ou outro ambiente Linux).
- Python 3.10 ou superior.
- pip e cURL.

Para conferir se Python e cURL estão disponíveis:

```bash
python3 --version
curl --version
```

## Instalação

Abra o terminal dentro da pasta do projeto e rode os comandos:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 route.py
```

Com o servidor ligado, acesse esta página no navegador:

**http://127.0.0.1:8080/portal**

### Primeiro acesso

Na primeira execução, o sistema cria uma conta para demonstração:

| Campo | Valor |
|---|---|
| Usuário | `admin` |
| Senha | `techstock123` |

Essa senha é apenas para testar o projeto. Ela não é salva diretamente no arquivo: o sistema gera um hash com PBKDF2-HMAC-SHA256 e um salt individual.

Também é possível escolher os dados dessa primeira conta antes de iniciar o sistema:

```bash
export TECHSTOCK_ADMIN_USER="seu_usuario"
export TECHSTOCK_ADMIN_PASSWORD="sua_senha"
python3 route.py
```

Essas variáveis só são usadas quando o arquivo de usuários ainda não existe. Se ele já tiver sido criado, os dados atuais são mantidos.

## Testando as operações com cURL

Deixe o servidor rodando no primeiro terminal. Abra outro terminal na pasta do projeto. É nesse segundo terminal que os comandos abaixo serão executados.

### 1. Fazer login

O primeiro passo é entrar no sistema e guardar o cookie da sessão em um arquivo. Depois, esse cookie será enviado nas outras operações.

```bash
curl -i -c cookies.txt \
  --data-urlencode "username=admin" \
  --data-urlencode "password=techstock123" \
  http://127.0.0.1:8080/portal
```

Com os dados corretos, o sistema redireciona para `/banco`.

### 2. CREATE — cadastrar um componente

Este exemplo cadastra um sensor ultrassônico:

```bash
curl -i -b cookies.txt -X POST http://127.0.0.1:8080/componentes \
  --data-urlencode "nome=Sensor ultrassônico HC-SR04" \
  --data-urlencode "categoria=Sensor" \
  --data-urlencode "quantidade=10" \
  --data-urlencode "descricao=Sensor de distância para Arduino e ESP32."
```

A resposta mostra os dados cadastrados e o ID que foi gerado. Guarde esse ID, pois ele será usado nos exemplos de UPDATE e DELETE.

Quando o sistema é executado pela primeira vez, ele já vem com três componentes de exemplo. Por isso, nesse primeiro cadastro o ID será 4. Nos próximos cadastros, o número continua aumentando.

### 3. READ — consultar os componentes

A leitura pedida na atividade é feita dentro do próprio sistema. Depois de cadastrar, abra esta página no navegador:

**http://127.0.0.1:8080/banco**

A lista mostra os componentes salvos, inclusive o que acabou de ser cadastrado.

Também deixei uma rota extra para consultar os registros em formato JSON pelo terminal. Ela não substitui a leitura da página `/banco`:

```bash
curl -i -b cookies.txt http://127.0.0.1:8080/componentes
```

### 4. UPDATE — alterar um componente

No exemplo abaixo, a quantidade do componente de ID 4 passa para 15. Caso o ID retornado no seu cadastro seja outro, troque o número na URL.

```bash
curl -i -b cookies.txt -X PUT http://127.0.0.1:8080/componentes/4 \
  --data-urlencode "quantidade=15" \
  --data-urlencode "descricao=Sensor ultrassônico atualizado."
```

### 5. DELETE — excluir um componente

Para excluir o mesmo registro:

```bash
curl -i -b cookies.txt -X DELETE http://127.0.0.1:8080/componentes/4
```

Depois, atualize a página `/banco` para conferir que ele não aparece mais.

### Rodar a sequência de testes de uma vez

Também deixei um script com os comandos principais. Com o servidor ligado, execute:

```bash
bash curl_exemplos.sh
```

Ele faz login, cadastra um componente, confere se ele aparece na página `/banco`, consulta a rota JSON, altera a quantidade e depois exclui o registro. No final, também faz uma requisição sem cookie para conferir se a API bloqueia quem não está autenticado. Essa última requisição deve retornar HTTP 401.

## Validações

O sistema confere os dados antes de salvar. Nome e categoria são obrigatórios, a quantidade precisa ser um número inteiro igual ou maior que zero e a descrição tem um limite de caracteres.

Algumas respostas que podem aparecer durante os testes:

| Situação | Código HTTP |
|---|---:|
| Requisição sem login | 401 |
| Campo inválido ou obrigatório vazio | 400 |
| ID não encontrado em UPDATE ou DELETE | 404 |
| Componente cadastrado | 201 |
| Componente atualizado ou excluído | 200 |

Os componentes e as contas ficam guardados em arquivos JSON dentro de `app/controllers/db/`. Assim, os registros continuam salvos mesmo depois de desligar o servidor. As sessões de login ficam em memória, expiram após uma hora e precisam ser criadas novamente quando o servidor é reiniciado.

## Testes dos modelos

Para executar os testes automatizados:

```bash
python3 -m unittest discover -s tests -v
```

Os testes estão divididos em dois arquivos. `test_models.py` verifica os modelos, as sessões, a classe abstrata e a persistência dos dados. `test_routes.py` verifica o login, o bloqueio de acesso sem autenticação e o CRUD pelas rotas HTTP, incluindo a consulta na página `/banco`.

Também configurei uma verificação automática no GitHub Actions. A cada atualização enviada ao repositório ou abertura de pull request, o GitHub instala as dependências e executa os testes dos modelos e das rotas.

## Encerrar o sistema

No terminal em que o servidor está rodando, pressione `Ctrl + C`. Para sair do ambiente virtual, use:

```bash
deactivate
```

## Explicação do projeto para a atividade

Neste trabalho, montei o TechStock, um sistema simples para cadastrar e consultar componentes eletrônicos. Separei o projeto em dois recursos: no portal, o usuário faz login usando o modelo `User_account`; depois, na página banco, consegue visualizar os componentes cadastrados. A leitura (READ) é feita nessa página, enquanto o cadastro, a alteração e a exclusão são testados pelo terminal Linux com cURL.

Para organizar o código, usei a divisão MVC: os modelos cuidam dos dados, as views mostram as páginas e o controller conecta essas partes. Os registros ficam salvos em arquivos JSON, e o sistema verifica algumas informações antes de gravar os dados. A proposta foi atender ao que foi pedido na atividade sem precisar configurar um banco de dados externo.

## Referência

Usei como referência de organização dos recursos `portal` e `banco` e da estrutura com Bottle o exemplo público [ianemirv/sigtap-bmvc](https://github.com/ianemirv/sigtap-bmvc), disponibilizado no GitHub. O TechStock tem seu próprio tema, modelos, campos, validações e páginas.
