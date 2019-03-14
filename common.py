from redis_op import RedisOperator
import config

redis = RedisOperator(host=config.REDIS_HOST, port=config.REDIS_PORT)
