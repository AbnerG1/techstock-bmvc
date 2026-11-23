from pathlib import Path
from threading import Timer
from urllib.parse import urlencode
import os
import webbrowser

from bottle import Bottle, redirect, request, response, run, static_file

from app.controllers.application import Application
from app.models.sessao import TEMPO_EXPIRACAO_SESSAO

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "app" / "static"

app = Bottle()
application = Application()


def current_user():
    token = request.get_cookie("session_id")
    return application.usuario_logado(token)


def require_api_login():
    if not current_user():
        response.status = 401
        return {"erro": "Acesso não autorizado. Faça login primeiro e envie cookies.txt."}
    return None


def voltar_ao_banco(mensagem, tipo="sucesso"):
    query = urlencode({"mensagem": mensagem, "tipo": tipo})
    redirect(f"/banco?{query}")


@app.route("/")
def index():
    return redirect("/portal")


@app.route("/static/<filepath:path>")
def serve_static(filepath):
    return static_file(filepath, root=str(STATIC_DIR))


@app.get("/portal")
def portal():
    if current_user():
        return redirect("/banco")
    return application.render_portal()


@app.post("/portal")
def login():
    username = request.forms.getunicode("username") or ""
    password = request.forms.getunicode("password") or ""
    token = application.autenticar(username, password)

    if not token:
        response.status = 401
        return application.render_portal(erro="Usuário ou senha incorretos.")

    response.set_cookie(
        "session_id",
        token,
        path="/",
        max_age=TEMPO_EXPIRACAO_SESSAO,
        httponly=True,
        samesite="Lax",
    )
    return redirect("/banco")


@app.get("/logout")
def logout():
    application.logout(request.get_cookie("session_id"))
    response.delete_cookie("session_id", path="/")
    return redirect("/portal")


@app.get("/banco")
def banco():
    username = current_user()
    if not username:
        return redirect("/portal")
    tipo = request.query.getunicode("tipo") or "sucesso"
    if tipo not in ("sucesso", "erro"):
        tipo = "sucesso"
    return application.render_banco(
        username,
        mensagem=request.query.getunicode("mensagem"),
        tipo_mensagem=tipo,
    )


# Formulários da página Banco. A API JSON continua disponível para testes e integração.
@app.post("/banco/componentes")
def criar_componente_pela_pagina():
    if not current_user():
        return redirect("/portal")
    try:
        application.componentes.criar(
            nome=request.forms.getunicode("nome"),
            categoria=request.forms.getunicode("categoria"),
            quantidade=request.forms.getunicode("quantidade"),
            descricao=request.forms.getunicode("descricao") or "",
        )
    except ValueError as exc:
        voltar_ao_banco(str(exc), "erro")
    voltar_ao_banco("Componente cadastrado com sucesso.")


@app.post("/banco/componentes/<componente_id:int>/atualizar")
def atualizar_componente_pela_pagina(componente_id):
    if not current_user():
        return redirect("/portal")
    try:
        componente = application.componentes.atualizar(
            componente_id,
            nome=request.forms.getunicode("nome"),
            categoria=request.forms.getunicode("categoria"),
            quantidade=request.forms.getunicode("quantidade"),
            descricao=request.forms.getunicode("descricao"),
        )
    except ValueError as exc:
        voltar_ao_banco(str(exc), "erro")
    if componente is None:
        voltar_ao_banco(f"Componente #{componente_id} não encontrado.", "erro")
    voltar_ao_banco(f"Componente #{componente_id} atualizado com sucesso.")


@app.post("/banco/componentes/<componente_id:int>/excluir")
def remover_componente_pela_pagina(componente_id):
    if not current_user():
        return redirect("/portal")
    componente = application.componentes.remover(componente_id)
    if componente is None:
        voltar_ao_banco(f"Componente #{componente_id} não encontrado.", "erro")
    voltar_ao_banco(f"Componente #{componente_id} excluído com sucesso.")


@app.get("/componentes")
def listar_componentes():
    erro = require_api_login()
    if erro:
        return erro

    return {
        "componentes": [
            componente.to_dict()
            for componente in application.componentes.listar()
        ]
    }


@app.post("/componentes")
def criar_componente():
    erro = require_api_login()
    if erro:
        return erro

    try:
        componente = application.componentes.criar(
            nome=request.forms.getunicode("nome"),
            categoria=request.forms.getunicode("categoria"),
            quantidade=request.forms.getunicode("quantidade"),
            descricao=request.forms.getunicode("descricao") or "",
        )
    except ValueError as exc:
        response.status = 400
        return {"erro": str(exc)}

    response.status = 201
    return {
        "mensagem": "Componente cadastrado com sucesso.",
        "componente": componente.to_dict(),
    }


@app.put("/componentes/<componente_id:int>")
def atualizar_componente(componente_id):
    erro = require_api_login()
    if erro:
        return erro

    try:
        componente = application.componentes.atualizar(
            componente_id,
            nome=request.forms.getunicode("nome"),
            categoria=request.forms.getunicode("categoria"),
            quantidade=request.forms.getunicode("quantidade"),
            descricao=request.forms.getunicode("descricao"),
        )
    except ValueError as exc:
        response.status = 400
        return {"erro": str(exc)}

    if componente is None:
        response.status = 404
        return {"erro": f"Componente de ID {componente_id} não encontrado."}

    return {
        "mensagem": "Componente atualizado com sucesso.",
        "componente": componente.to_dict(),
    }


@app.delete("/componentes/<componente_id:int>")
def remover_componente(componente_id):
    erro = require_api_login()
    if erro:
        return erro

    componente = application.componentes.remover(componente_id)
    if componente is None:
        response.status = 404
        return {"erro": f"Componente de ID {componente_id} não encontrado."}

    return {
        "mensagem": "Componente removido com sucesso.",
        "componente": componente.to_dict(),
    }


if __name__ == "__main__":
    if os.getenv("TECHSTOCK_ABRIR_NAVEGADOR", "1") == "1" and not os.getenv("CI"):
        Timer(1.2, lambda: webbrowser.open_new_tab("http://127.0.0.1:8080/portal")).start()
    run(app, host="127.0.0.1", port=8080, debug=False, reloader=False)
