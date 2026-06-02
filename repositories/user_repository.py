from bson import ObjectId
from repositories.database import user_collection
from repositories.schemas import UserDB, UserCreate
from services.auth_service import get_password_hash

class UserRepository:
    @staticmethod
    async def create_user(user: UserCreate):
        hashed_password = get_password_hash(user.password)
        user_dict = {
            "username": user.username,
            "hashed_password": hashed_password,
            "role": user.role
        }
        new_user = await user_collection.insert_one(user_dict)
        created_user = await user_collection.find_one({"_id": new_user.inserted_id})
        return UserDB(**created_user)

    @staticmethod
    async def get_user_by_username(username: str):
        return await user_collection.find_one({"username": username})

    @staticmethod
    async def get_all_users():
        users = []
        cursor = user_collection.find()
        async for document in cursor:
            users.append(UserDB(**document))
        return users

    @staticmethod
    async def update_user(id: str, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        update_data = {
            "username": user.username,
            "hashed_password": hashed_password,
            "role": user.role
        }
        await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )
        updated_user = await user_collection.find_one({"_id": ObjectId(id)})
        if updated_user:
            return UserDB(**updated_user)
        return None

    @staticmethod
    async def delete_user(id: str):
        result = await user_collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0