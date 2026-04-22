# expert-spork

API de **controle financeiro** construída com FastAPI.

## Funcionalidades

- Cadastro de transações (receita/despesa)
- Listagem e consulta por ID
- Remoção de transação
- Resumo financeiro com total de receitas, despesas e saldo

## Como executar

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

Acesse:

- API: `http://127.0.0.1:8000`
- Documentação interativa: `http://127.0.0.1:8000/docs`

## Endpoints

- `POST /transacoes`
- `GET /transacoes`
- `GET /transacoes/{transacao_id}`
- `DELETE /transacoes/{transacao_id}`
- `GET /resumo`

## Exemplo de payload (POST /transacoes)

```json
{
  "descricao": "Salário",
  "valor": 5000,
  "tipo": "receita",
  "data": "2026-04-22",
  "categoria": "Trabalho"
}
```
