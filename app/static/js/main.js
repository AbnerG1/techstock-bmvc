document.addEventListener('DOMContentLoaded', function () {
    const filtro = document.getElementById('filtro');
    const tabela = document.getElementById('tabela');
    const avisoVazio = document.getElementById('empty-filter');

    if (!filtro || !tabela) return;

    filtro.addEventListener('input', function () {
        const termo = filtro.value.trim().toLocaleLowerCase('pt-BR');
        let visiveis = 0;

        tabela.querySelectorAll('tbody tr').forEach(function (linha) {
            const corresponde = linha.textContent.toLocaleLowerCase('pt-BR').includes(termo);
            linha.hidden = !corresponde;
            if (corresponde) visiveis += 1;
        });

        if (avisoVazio) avisoVazio.classList.toggle('hidden', visiveis !== 0);
    });
});
