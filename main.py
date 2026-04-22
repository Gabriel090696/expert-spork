from datetime import date
from enum import Enum
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Controle Financeiro API", version="1.0.0")


class TipoTransacao(str, Enum):
    receita = "receita"
    despesa = "despesa"


class TransacaoCriacao(BaseModel):
    descricao: str = Field(..., min_length=3, max_length=120)
    valor: float = Field(..., gt=0)
    tipo: TipoTransacao
    data: date
    categoria: str = Field(..., min_length=2, max_length=50)


class Transacao(TransacaoCriacao):
    id: int


class Resumo(BaseModel):
    total_receitas: float
    total_despesas: float
    saldo: float


transacoes: List[Transacao] = []
proximo_id = 1


@app.get("/")
async def root() -> Dict[str, str]:
    return {
        "mensagem": "API de controle financeiro online! Acesse /docs para testar os endpoints."
    }


@app.post("/transacoes", response_model=Transacao, status_code=201)
async def criar_transacao(payload: TransacaoCriacao) -> Transacao:
    global proximo_id

    nova = Transacao(id=proximo_id, **payload.model_dump())
    transacoes.append(nova)
    proximo_id += 1

    return nova


@app.get("/transacoes", response_model=List[Transacao])
async def listar_transacoes() -> List[Transacao]:
    return transacoes


@app.get("/transacoes/{transacao_id}", response_model=Transacao)
async def buscar_transacao(transacao_id: int) -> Transacao:
    for transacao in transacoes:
        if transacao.id == transacao_id:
            return transacao

    raise HTTPException(status_code=404, detail="Transação não encontrada")


@app.delete("/transacoes/{transacao_id}", status_code=204)
async def remover_transacao(transacao_id: int) -> None:
    for i, transacao in enumerate(transacoes):
        if transacao.id == transacao_id:
            transacoes.pop(i)
            return

    raise HTTPException(status_code=404, detail="Transação não encontrada")


@app.get("/resumo", response_model=Resumo)
async def obter_resumo() -> Resumo:
    total_receitas = sum(t.valor for t in transacoes if t.tipo == TipoTransacao.receita)
    total_despesas = sum(t.valor for t in transacoes if t.tipo == TipoTransacao.despesa)

    return Resumo(
        total_receitas=round(total_receitas, 2),
        total_despesas=round(total_despesas, 2),
        saldo=round(total_receitas - total_despesas, 2),
    )
