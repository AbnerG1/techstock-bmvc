<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#101b35">
    <title>{{title}} | TechStock</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <header class="topbar">
        <a class="brand" href="/portal" aria-label="TechStock início">
            <span class="brand-mark">TS</span>
            <span><strong>TechStock</strong><small>Controle de componentes</small></span>
        </a>
        % if defined('username') and username:
        <nav class="nav-user">
            <span class="user-name">{{username}}</span>
            <a class="logout-link" href="/logout">Sair</a>
        </nav>
        % end
    </header>
    <main class="main-content">
        {{!base}}
    </main>
    <footer class="footer">
        Projeto BMVC · Python e Bottle
    </footer>
    <script src="/static/js/main.js"></script>
</body>
</html>
