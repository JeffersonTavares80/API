from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
import sqlite3
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Configuração do banco de dados SQLite
DATABASE = 'dados.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Modelos Pydantic para cada tabela
class ODS(BaseModel):
    ID_ODS: Optional[int] = None
    NOME_ODS: str

class Dominio(BaseModel):
    ID_DOMINIO: Optional[int] = None
    NOME_DOMINIO: str
    RESPONSAVEL_DOMINIO: str

class Servico(BaseModel):
    ID_SERVICO: Optional[int] = None
    TITULO_SERVICO: str

class Programa(BaseModel):
    ID_PROGRAMA: str
    ID_DOMINIO: int
    TITULO_PROGRAMA: str

class ProgramaODS(BaseModel):
    ID_PROGRAMA: str
    ID_ODS: int

class Inscricao(BaseModel):
    ID_INSCRICAO: str
    ID_PROGRAMA: str
    ID_PESSOA: str
    DATA_INSCRICAO: str

class ParticipantePrograma(BaseModel):
    ID_PROGRAMA: str
    ID_INSCRICAO: str

class AgendamentoServico(BaseModel):
    ID_AGENDAMENTO: Optional[int] = None
    ID_PESSOA: str
    ID_SERVICO: int
    DATETIME_AGENDAMENTO: str

# ONU_ODS
@app.get("/ods/", response_model=List[ODS])
async def read_all_ods():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ONU_ODS")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/ods/", response_model=ODS)
async def create_ods(ods: ODS):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ONU_ODS (NOME_ODS) VALUES (?)", (ods.NOME_ODS,))
    conn.commit()
    ods.ID_ODS = cursor.lastrowid
    conn.close()
    return ods

@app.delete("/ods/{id_ods}")
async def delete_ods(id_ods: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ONU_ODS WHERE ID_ODS = ?", (id_ods,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="ODS não encontrado")
    return {"detail": "ODS deletado"}

# DOMINIOS
@app.get("/dominios/", response_model=List[Dominio])
async def read_all_dominios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DOMINIOS")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/dominios/", response_model=Dominio)
async def create_dominio(dominio: Dominio):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO DOMINIOS (NOME_DOMINIO, RESPONSAVEL_DOMINIO) VALUES (?, ?)",
                   (dominio.NOME_DOMINIO, dominio.RESPONSAVEL_DOMINIO))
    conn.commit()
    dominio.ID_DOMINIO = cursor.lastrowid
    conn.close()
    return dominio

@app.delete("/dominios/{id_dominio}")
async def delete_dominio(id_dominio: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM DOMINIOS WHERE ID_DOMINIO = ?", (id_dominio,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Domínio não encontrado")
    return {"detail": "Domínio deletado"}

# SERVICOS
@app.get("/servicos/", response_model=List[Servico])
async def read_all_servicos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SERVICOS")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/servicos/", response_model=Servico)
async def create_servico(servico: Servico):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO SERVICOS (TITULO_SERVICO) VALUES (?)", (servico.TITULO_SERVICO,))
    conn.commit()
    servico.ID_SERVICO = cursor.lastrowid
    conn.close()
    return servico

@app.delete("/servicos/{id_servico}")
async def delete_servico(id_servico: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM SERVICOS WHERE ID_SERVICO = ?", (id_servico,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return {"detail": "Serviço deletado"}

# PROGRAMAS
@app.get("/programas/", response_model=List[Programa])
async def read_all_programas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PROGRAMAS")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/programas/", response_model=Programa)
async def create_programa(programa: Programa):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO PROGRAMAS (ID_PROGRAMA, ID_DOMINIO, TITULO_PROGRAMA) VALUES (?, ?, ?)",
                   (programa.ID_PROGRAMA, programa.ID_DOMINIO, programa.TITULO_PROGRAMA))
    conn.commit()
    conn.close()
    return programa

@app.delete("/programas/{id_programa}")
async def delete_programa(id_programa: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM PROGRAMAS WHERE ID_PROGRAMA = ?", (id_programa,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Programa não encontrado")
    return {"detail": "Programa deletado"}

# PROGRAMAS/ODS

class ProgramaODS(BaseModel):
    ID_PROGRAMA: str
    ID_ODS: int

@app.get("/programa_ods/", response_model=List[ProgramaODS])
async def read_all_programa_ods():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PROGRAMA_ODS")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/programa_ods/", response_model=ProgramaODS)
async def create_programa_ods(programa_ods: ProgramaODS):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO PROGRAMA_ODS (ID_PROGRAMA, ID_ODS) VALUES (?, ?)",
        (programa_ods.ID_PROGRAMA, programa_ods.ID_ODS)
    )
    conn.commit()
    conn.close()
    return programa_ods

@app.delete("/programa_ods/{id_programa}/{id_ods}")
async def delete_programa_ods(id_programa: str, id_ods: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM PROGRAMA_ODS WHERE ID_PROGRAMA = ? AND ID_ODS = ?", (id_programa, id_ods))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Relação Programa-ODS não encontrada")
    return {"detail": "Relação Programa-ODS deletada"}

# INSCRIÇÕES

class Inscricao(BaseModel):
    ID_INSCRICAO: str
    ID_PROGRAMA: str
    ID_PESSOA: str
    DATA_INSCRICAO: str

@app.get("/inscricoes/", response_model=List[Inscricao])
async def read_all_inscricoes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM INSCRICOES")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/inscricoes/", response_model=Inscricao)
async def create_inscricao(inscricao: Inscricao):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO INSCRICOES (ID_INSCRICAO, ID_PROGRAMA, ID_PESSOA, DATA_INSCRICAO) VALUES (?, ?, ?, ?)",
        (inscricao.ID_INSCRICAO, inscricao.ID_PROGRAMA, inscricao.ID_PESSOA, inscricao.DATA_INSCRICAO)
    )
    conn.commit()
    conn.close()
    return inscricao

@app.delete("/inscricoes/{id_inscricao}")
async def delete_inscricao(id_inscricao: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM INSCRICOES WHERE ID_INSCRICAO = ?", (id_inscricao,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Inscrição não encontrada")
    return {"detail": "Inscrição deletada"}

#PARTICIPANTE PROGRAMA

class ParticipantePrograma(BaseModel):
    ID_PROGRAMA: str
    ID_INSCRICAO: str

@app.get("/participantes_programa/", response_model=List[ParticipantePrograma])
async def read_all_participantes_programa():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PARTICIPANTE_PROGRAMA")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/participantes_programa/", response_model=ParticipantePrograma)
async def create_participante_programa(participante_programa: ParticipantePrograma):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO PARTICIPANTE_PROGRAMA (ID_PROGRAMA, ID_INSCRICAO) VALUES (?, ?)",
        (participante_programa.ID_PROGRAMA, participante_programa.ID_INSCRICAO)
    )
    conn.commit()
    conn.close()
    return participante_programa

@app.delete("/participantes_programa/{id_programa}/{id_inscricao}")
async def delete_participante_programa(id_programa: str, id_inscricao: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM PARTICIPANTE_PROGRAMA WHERE ID_PROGRAMA = ? AND ID_INSCRICAO = ?", (id_programa, id_inscricao))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Participante não encontrado")
    return {"detail": "Participante deletado"}

#AGENDAMENTO DE SERVIÇOS

class AgendamentoServico(BaseModel):
    ID_AGENDAMENTO: Optional[int] = None
    ID_PESSOA: str
    ID_SERVICO: int
    DATETIME_AGENDAMENTO: str

@app.get("/agendamentos_servico/", response_model=List[AgendamentoServico])
async def read_all_agendamentos_servico():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM AGENDAMENTO_SERVICO")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/agendamentos_servico/", response_model=AgendamentoServico)
async def create_agendamento_servico(agendamento_servico: AgendamentoServico):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO AGENDAMENTO_SERVICO (ID_PESSOA, ID_SERVICO, DATETIME_AGENDAMENTO) VALUES (?, ?, ?)",
        (agendamento_servico.ID_PESSOA, agendamento_servico.ID_SERVICO, agendamento_servico.DATETIME_AGENDAMENTO)
    )
    conn.commit()
    agendamento_servico.ID_AGENDAMENTO = cursor.lastrowid
    conn.close()
    return agendamento_servico

@app.delete("/agendamentos_servico/{id_agendamento}")
async def delete_agendamento_servico(id_agendamento: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM AGENDAMENTO_SERVICO WHERE ID_AGENDAMENTO = ?", (id_agendamento,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return {"detail": "Agendamento deletado"}
