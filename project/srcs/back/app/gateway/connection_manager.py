from app.core.config import Config
from flask import jsonify

class ConnectionManager:

    @staticmethod
    def connect_user(user_id: int, sid: str):
        redis = Config.redis_instence
        redis.hset(
            f"ws:connections", 
            f"sid:{sid}", 
            user_id
        )
        redis.sadd(
            f"ws:user:{user_id}:sockets", 
            sid
        )
        
        redis.set(
            f"ws:user:{user_id}:online", 
            "1"
        )
        
        redis.publish(
            "ws:presence", 
            jsonify({
                "user_id": user_id,
                "status": "online"
            })
        )
    
    @staticmethod
    def disconnect_user(sid: str):
        redis = Config.redis_instence
        user_id = redis.hget("ws:connections", f"sid:{sid}")
        if not user_id:
            return
            
        user_id = int(user_id)
        
        redis.hdel("ws:connections", f"sid:{sid}")
        redis.srem(f"ws:user:{user_id}:sockets", sid)
        
        if redis.scard(f"ws:user:{user_id}:sockets") == 0:
            redis.delete(f"ws:user:{user_id}:online")
            
            redis.publish(
                "ws:presence",
                jsonify({
                    "user_id": user_id,
                    "status": "offline"
                })
            )

    @staticmethod
    def is_user_online(user_id: int) -> bool:
        redis = Config.redis_instence
        return bool(
            redis.exists(f"ws:user:{user_id}:online")
        )