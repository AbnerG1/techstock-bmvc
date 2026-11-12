% rebase('layout', title='Portal')
<section class="login-wrap">
    <div class="login-intro">
        <span class="eyebrow">PORTAL</span>
        <h1>Controle de componentes eletrônicos</h1>
        <p>Entre no sistema para consultar os componentes cadastrados.</p>
    </div>
    <div class="login-card">
        <div class="card-icon">⌁</div>
        <h2>Acessar o TechStock</h2>
        <p class="muted">Informe seu usuário e sua senha.</p>
        % if erro:
        <div class="alert" role="alert">{{erro}}</div>
        % end
        <form action="/portal" method="post" class="login-form">
            <label for="username">Usuário</label>
            <input type="text" id="username" name="username" autocomplete="username" required autofocus>
            <label for="password">Senha</label>
            <input type="password" id="password" name="password" autocomplete="current-password" required>
            <button type="submit" class="primary-button">Entrar <span>→</span></button>
        </form>
    </div>
</section>
