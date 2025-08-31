from typing import List, Optional
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from pymongo.errors import PyMongoError

from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import InsertionError, NotFoundException


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        
        # Anotação: Resolvendo o Desafio 1.
        # Adicionei esse bloco try/except para capturar qualquer erro que o
        # MongoDB possa retornar durante a inserção de um novo produto.
        # Se der erro, ele levanta a minha exceção customizada `InsertionError`.
        try:
            await self.collection.insert_one(product_model.model_dump())
        except PyMongoError as e:
            raise InsertionError(message=str(e))

        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductOut(**result)

    # Anotação: Resolvendo o Desafio 3.
    # Mudei a função `query` para aceitar `price_min` e `price_max` como argumentos.
    # Com isso, consigo criar um filtro dinâmico pro MongoDB, usando `$gt` (maior que)
    # e `$lt` (menor que), para buscar produtos numa faixa de preço.
    async def query(self, price_min: Optional[float] = None, price_max: Optional[float] = None) -> List[ProductOut]:
        filter_query = {}
        price_filter = {}

        if price_min is not None:
            price_filter["$gt"] = price_min

        if price_max is not None:
            price_filter["$lt"] = price_max

        if price_filter:
            filter_query["price"] = price_filter

        return [ProductOut(**item) async for item in self.collection.find(filter_query)]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        # Anotação: Resolvendo o Desafio 2. Fiz duas coisas aqui:
        # 1. Mudei para `body.model_dump(exclude_unset=True)`. Isso força
        #    a inclusão do campo `updated_at` (que tem um valor padrão de fábrica
        #    lá no schema) na hora de salvar a alteração no banco.
        update_data = body.model_dump(exclude_unset=True)

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": update_data},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        # 2. Adicionei esta verificação. Se o `find_one_and_update` não
        #    encontrar o produto pra atualizar, o `result` vai ser None.
        #    Nesse caso, eu levanto a exceção `NotFoundException`, como foi pedido.
        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        result = await self.collection.delete_one({"id": id})

        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()
