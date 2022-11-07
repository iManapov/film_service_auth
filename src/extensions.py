from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from src.db.db_redis import rate_limit_redis_pool
from src.core.config import settings
from src.utils.user import get_key_func, get_user_uuid


ma = Marshmallow()
jwt = JWTManager()
migrate = Migrate()
limiter = Limiter(
    key_func=get_key_func,
    default_limits=settings.rate_limits,
    storage_uri="redis://",
    storage_options={"connection_pool": rate_limit_redis_pool},
)
