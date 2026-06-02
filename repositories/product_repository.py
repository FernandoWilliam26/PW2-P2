from bson import ObjectId
from repositories.database import product_collection
from repositories.schemas import ProductDB, ProductBase

class ProductRepository:
    
    @staticmethod
    async def get_all_products():
        products = []
        cursor = product_collection.find()
        async for document in cursor:
            products.append(ProductDB(**document))
        return products

    @staticmethod
    async def create_product(product: ProductBase):
        product_dict = product.model_dump()
        new_product = await product_collection.insert_one(product_dict)
        created_product = await product_collection.find_one({"_id": new_product.inserted_id})
        return ProductDB(**created_product)

    @staticmethod
    async def update_product(id: str, product: ProductBase):
        await product_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": product.model_dump()}
        )
        updated_product = await product_collection.find_one({"_id": ObjectId(id)})
        if updated_product:
            return ProductDB(**updated_product)
        return None

    @staticmethod
    async def delete_product(id: str):
        result = await product_collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0