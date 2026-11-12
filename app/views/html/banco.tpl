% rebase('layout', title='Banco', username=username)
<section class="page-heading">
    <div>
        <span class="eyebrow">BANCO</span>
        <h1>Componentes cadastrados</h1>
        <p>Consulte os itens que estão salvos no sistema.</p>
    </div>
    <div class="heading-mark">⌘</div>
</section>
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
<section class="catalog-card">
    <div class="catalog-toolbar">
        <div>
            <h2>Lista de componentes</h2>
            <p class="muted">A consulta (READ) fica nesta página.</p>
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
                </tr>
                % end
            </tbody>
        </table>
    </div>
    <p id="empty-filter" class="empty-state hidden">Não encontrei nenhum componente com esse nome ou categoria.</p>
    % else:
    <p class="empty-state">Ainda não há componentes cadastrados. Use o comando CREATE com cURL para adicionar o primeiro.</p>
    % end
    <div class="catalog-note">
        <span class="note-icon">i</span>
        <span>Para cadastrar, alterar ou excluir um item, use o cURL no terminal Linux. Depois, atualize esta página para conferir a mudança.</span>
    </div>
</section>
