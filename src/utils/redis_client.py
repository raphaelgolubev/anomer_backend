import redis.asyncio as redis
from src.config import settings


class RedisClient:
    """Клиент для работы с Redis"""
    
    def __init__(self):
        redis_kwargs = {
            "host": settings.redis.host,
            "port": settings.redis.port,
            "db": settings.redis.db,
            "decode_responses": True
        }
        
        # Добавляем username если указан
        if settings.redis.username:
            redis_kwargs["username"] = settings.redis.username
            
        # Добавляем password если указан
        if settings.redis.password:
            redis_kwargs["password"] = settings.redis.password
            
        self.redis = redis.Redis(**redis_kwargs)
    
    async def set_verification_code(self, email: str, code: str) -> bool:
        """
        Сохраняет код верификации для email с TTL
        
        Args:
            email: Email пользователя
            code: 6-значный код верификации
            
        Returns:
            bool: True если код успешно сохранен
        """
        try:
            key = f"verification_code:{email}"
            await self.redis.setex(
                key, 
                settings.redis.verification_code_ttl, 
                code
            )
            return True
        except Exception as e:
            print(f"Redis error: {e}")
            return False
    
    async def get_verification_code(self, email: str) -> str | None:
        """
        Получает код верификации для email
        
        Args:
            email: Email пользователя
            
        Returns:
            str | None: Код верификации или None если не найден/истек
        """
        try:
            key = f"verification_code:{email}"
            code = await self.redis.get(key)
            return code
        except Exception as e:
            print(f"Redis error: {e}")
            return None
    
    async def delete_verification_code(self, email: str) -> bool:
        """
        Удаляет код верификации для email
        
        Args:
            email: Email пользователя
            
        Returns:
            bool: True если код успешно удален
        """
        try:
            key = f"verification_code:{email}"
            result = await self.redis.delete(key)
            return result > 0
        except Exception as e:
            print(f"Redis error: {e}")
            return False
    
    async def close(self):
        """Закрывает соединение с Redis"""
        await self.redis.close()


# Глобальный экземпляр Redis клиента
redis_client = RedisClient() 