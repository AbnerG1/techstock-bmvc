% rebase('layout', title='Banco', username=username)
<section class="page-heading">
    <div>
        <span class="eyebrow">BANCO</span>
        <h1>Componentes cadastrados</h1>
        <p>Consulte e mantenha os itens do catálogo atualizados.</p>
    </div>
    <div class="heading-mark">⌘</div>
</section>

% if mensagem:
<div class="flash-message {{'flash-error' if tipo_mensagem == 'erro' else 'flash-success'}}" role="status">{{mensagem}}</div>
% end

<section class="stats-grid" aria-label="Resumo do catálogo">
    <article class="stat-card">
        <span class="stat-label">Tipos cadastrados</span>
        <strong>{{len(componentes)}}</strong>
    </article>
    <article class="stat-card">
        <span class="stat-label">Unidades no estoque</span>
        <strong>{{quantidade_total}}</strong>
    </article>
    <article class="stat-card">
        <span class="stat-label">Usuário conectado</span>
        <strong class="connected-user">{{username}}</strong>
    </article>
</section>

<section class="catalog-card form-card" id="novo-componente">
    <div class="section-heading">
        <div>
            <span class="eyebrow">NOVO REGISTRO</span>
            <h2>Adicionar componente</h2>
            <p class="muted">Preencha os dados para incluir um item no catálogo.</p>
        </div>
    </div>
    <form action="/banco/componentes" method="post" class="component-form">
        <div class="form-field">
            <label for="novo-nome">Nome</label>
            <input id="novo-nome" name="nome" maxlength="100" placeholder="Ex.: Sensor HC-SR04" required>
        </div>
        <div class="form-field">
            <label for="novo-categoria">Categoria</label>
            <input id="novo-categoria" name="categoria" maxlength="60" placeholder="Ex.: Sensor" required>
        </div>
        <div class="form-field quantity-field">
            <label for="novo-quantidade">Quantidade</label>
            <input id="novo-quantidade" name="quantidade" type="number" min="0" step="1" value="1" required>
        </div>
        <div class="form-field description-field">
            <label for="novo-descricao">Descrição</label>
            <input id="novo-descricao" name="descricao" maxlength="300" placeholder="Informações adicionais (opcional)">
        </div>
        <div class="form-actions">
            <button type="submit" class="primary-button">Cadastrar componente <span>＋</span></button>
        </div>
    </form>
</section>

<section class="catalog-card">
    <div class="catalog-toolbar">
        <div>
            <h2>Lista de componentes</h2>
            <p class="muted">Pesquise, edite ou remova registros existentes.</p>
        </div>
        <input type="search" id="filtro" class="search-input" placeholder="Buscar por nome ou categoria..." aria-label="Buscar componente">
    </div>
    % if componentes:
    <div class="table-scroll">
        <table id="tabela">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Componente</th>
                    <th>Categoria</th>
                    <th>Quantidade</th>
                    <th>Descrição</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
                % for componente in componentes:
                <tr>
                    <td class="id-cell">#{{componente.id}}</td>
                    <td class="component-name">{{componente.nome}}</td>
                    <td><span class="category-pill">{{componente.categoria}}</span></td>
                    <td><strong>{{componente.quantidade}}</strong></td>
                    <td class="description-cell">{{componente.descricao or '—'}}</td>
                    <td class="actions-cell">
                        <details class="edit-details">
                            <summary class="small-button edit-button">Editar</summary>
                            <form action="/banco/componentes/{{componente.id}}/atualizar" method="post" class="edit-form">
                                <strong>Editar #{{componente.id}}</strong>
                                <label for="nome-{{componente.id}}">Nome</label>
                                <input id="nome-{{componente.id}}" name="nome" value="{{componente.nome}}" maxlength="100" required>
                                <label for="categoria-{{componente.id}}">Categoria</label>
                                <input id="categoria-{{componente.id}}" name="categoria" value="{{componente.categoria}}" maxlength="60" required>
                                <label for="quantidade-{{componente.id}}">Quantidade</label>
                                <input id="quantidade-{{componente.id}}" name="quantidade" type="number" min="0" step="1" value="{{componente.quantidade}}" required>
                                <label for="descricao-{{componente.id}}">Descrição</label>
                                <input id="descricao-{{componente.id}}" name="descricao" value="{{componente.descricao}}" maxlength="300">
                                <button type="submit" class="small-button save-button">Salvar alterações</button>
                            </form>
                        </details>
                        <form action="/banco/componentes/{{componente.id}}/excluir" method="post" class="delete-form" onsubmit="return confirm('Deseja realmente excluir este componente?');">
                            <button type="submit" class="small-button delete-button">Excluir</button>
                        </form>
                    </td>
                </tr>
                % end
            </tbody>
        </table>
    </div>
    <p id="empty-filter" class="empty-state hidden">Não encontrei nenhum componente com esse nome ou categoria.</p>
    % else:
    <p class="empty-state">Ainda não há componentes cadastrados. Use o formulário acima para adicionar o primeiro.</p>
    % end
</section>
