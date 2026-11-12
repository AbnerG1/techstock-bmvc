#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8080}"
USUARIO="${TECHSTOCK_ADMIN_USER:-admin}"
SENHA="${TECHSTOCK_ADMIN_PASSWORD:-techstock123}"
COOKIE_FILE="$(mktemp)"
trap 'rm -f "$COOKIE_FILE"' EXIT

command -v curl >/dev/null 2>&1 || { echo "Erro: instale o cURL antes de continuar."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Erro: Python 3 é necessário para ler o ID retornado."; exit 1; }

echo "== LOGIN =="
STATUS_LOGIN=$(curl -sS -o /dev/null -w "%{http_code}" -c "$COOKIE_FILE" \
  --data-urlencode "username=$USUARIO" \
  --data-urlencode "password=$SENHA" \
  "$BASE_URL/portal")

case "$STATUS_LOGIN" in
  302|303|307) echo "Login realizado." ;;
  *) echo "Falha no login. Código HTTP: $STATUS_LOGIN"; exit 1 ;;
esac

echo
echo "== CREATE: cadastrar componente =="
RESPOSTA=$(curl -sS -w $'\n%{http_code}' -b "$COOKIE_FILE" -X POST "$BASE_URL/componentes" \
  --data-urlencode "nome=Sensor ultrassônico HC-SR04" \
  --data-urlencode "categoria=Sensor" \
  --data-urlencode "quantidade=10" \
  --data-urlencode "descricao=Sensor de distância para projetos com Arduino e ESP32.")

STATUS="${RESPOSTA##*$'\n'}"
CORPO="${RESPOSTA%$'\n'*}"
if [[ "$STATUS" != "201" ]]; then
  echo "$CORPO"
  echo "Falha ao cadastrar. Código HTTP: $STATUS"
  exit 1
fi
echo "$CORPO"

NOVO_ID=$(printf '%s' "$CORPO" | python3 -c 'import json,sys; print(json.load(sys.stdin)["componente"]["id"])')

echo
echo "== READ: conferir a página /banco =="
PAGINA_BANCO=$(curl -fsS -b "$COOKIE_FILE" "$BASE_URL/banco")
if [[ "$PAGINA_BANCO" != *"Sensor ultrassônico HC-SR04"* ]]; then
  echo "O componente cadastrado não apareceu na página /banco."
  exit 1
fi
echo "A página /banco mostra o componente cadastrado."

echo
echo "== CONSULTA ADICIONAL: conferir a rota JSON =="
STATUS_READ=$(curl -sS -o /dev/null -w "%{http_code}" -b "$COOKIE_FILE" "$BASE_URL/componentes")
if [[ "$STATUS_READ" != "200" ]]; then
  echo "Falha na consulta JSON. Código HTTP: $STATUS_READ"
  exit 1
fi
echo "Consulta JSON funcionando."

echo
echo "== UPDATE: alterar quantidade do componente #$NOVO_ID =="
STATUS_UPDATE=$(curl -sS -o /dev/null -w "%{http_code}" -b "$COOKIE_FILE" -X PUT "$BASE_URL/componentes/$NOVO_ID" \
  --data-urlencode "quantidade=15")
if [[ "$STATUS_UPDATE" != "200" ]]; then
  echo "Falha ao atualizar. Código HTTP: $STATUS_UPDATE"
  exit 1
fi
echo "Quantidade atualizada."

echo
echo "== DELETE: excluir o componente #$NOVO_ID =="
STATUS_DELETE=$(curl -sS -o /dev/null -w "%{http_code}" -b "$COOKIE_FILE" -X DELETE "$BASE_URL/componentes/$NOVO_ID")
if [[ "$STATUS_DELETE" != "200" ]]; then
  echo "Falha ao excluir. Código HTTP: $STATUS_DELETE"
  exit 1
fi
echo "Componente excluído."

echo
echo "== TESTE DE AUTENTICAÇÃO: sem cookie deve retornar HTTP 401 =="
STATUS_SEM_LOGIN=$(curl -sS -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/componentes" \
  --data-urlencode "nome=Teste" \
  --data-urlencode "categoria=Teste" \
  --data-urlencode "quantidade=1")
if [[ "$STATUS_SEM_LOGIN" != "401" ]]; then
  echo "O teste de autenticação falhou. Código HTTP recebido: $STATUS_SEM_LOGIN"
  exit 1
fi
echo "Acesso sem login bloqueado corretamente."

echo
echo "Todos os testes via cURL terminaram sem erros. Atualize /banco no navegador para conferir a lista."
