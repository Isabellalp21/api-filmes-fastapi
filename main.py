from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta

import models, schemas, crud
from database import SessionLocal, engine

# 🔒 Configurações JWT
SECRET_KEY = "segredo_super_secreto"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 🔐 Usuário fictício (para fins de teste)
fake_user = {
    "username": "admin",
    "password": "123456"
}

# 🔧 Criação do banco de dados
models.Base.metadata.create_all(bind=engine)

# ✅ Instância da aplicação com segurança
app = FastAPI(
    title="API de Filmes com FastAPI",
    description="Esta API permite gerenciar filmes com autenticação via JWT",
    version="1.0.0"
)

# 🔧 Customização do Swagger para mostrar o botão "Authorize"
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/login",
                    "scopes": {}
                }
            }
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if "security" not in openapi_schema["paths"][path][method]:
                openapi_schema["paths"][path][method]["security"] = [{"OAuth2PasswordBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# 🔁 Dependência para obter o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔑 Geração de token JWT
def criar_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ✅ Verificação do token
def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

# 🔐 Rota de login
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != fake_user["username"] or form_data.password != fake_user["password"]:
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos")
    
    token = criar_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

# 📦 ROTAS PROTEGIDAS COM TOKEN JWT

@app.post("/filmes/", response_model=schemas.Filme)
def criar_filme(
    filme: schemas.FilmeCreate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verificar_token)
):
    return crud.create_filme(db=db, filme=filme)

@app.get("/filmes/", response_model=list[schemas.Filme])
def listar_filmes(
    db: Session = Depends(get_db),
    token_data: dict = Depends(verificar_token)
):
    return crud.get_filmes(db)

@app.get("/filmes/{filme_id}", response_model=schemas.Filme)
def buscar_filme(
    filme_id: int,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verificar_token)
):
    filme = crud.get_filme(db, filme_id)
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return filme

@app.put("/filmes/{filme_id}", response_model=schemas.Filme)
def atualizar_filme(
    filme_id: int,
    filme: schemas.FilmeCreate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verificar_token)
):
    return crud.update_filme(db, filme_id, filme)

@app.delete("/filmes/{filme_id}")
def deletar_filme(
    filme_id: int,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verificar_token)
):
    filme = crud.delete_filme(db, filme_id)
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return {"message": "Filme deletado"}
