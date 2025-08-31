from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from store.core.exceptions import InsertionError
from store.core.config import settings
from store.routers import api_router


class App(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            version="0.0.1",
            title=settings.PROJECT_NAME,
            root_path=settings.ROOT_PATH
        )


app = App()

# Anotação: Adicionei este handler para resolver a parte do desafio sobre
# o tratamento de exceções. Quando a `InsertionError` é lançada lá no usecase,
# este código a captura e retorna um erro JSON positivo com status 422,
# em vez de deixar a aplicação quebrar.
@app.exception_handler(InsertionError)
def insertion_error_handler(request: Request, exc: InsertionError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.message},
    )

app.include_router(api_router)
