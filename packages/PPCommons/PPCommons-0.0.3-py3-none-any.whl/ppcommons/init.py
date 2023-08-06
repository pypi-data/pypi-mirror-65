import os
from io import StringIO
from dotenv import dotenv_values
from redis import StrictRedis
from redis_cache import RedisCache


def init_app(app=None):
    if not app:
        raise Exception('Invalid INIT APP received')
    # configuring configs
    app = configure_config(app, getattr(app, '__pp_init_properties', {}).get("config_eval", {}))
    # configuring redis cache
    app = configure_redis_cache(app)
    # configuring logging
    app = configure_logging(app)
    # configure templating
    app = configure_templating(app)
    return app


def configure_config(app, eval):
    dotenv_path = os.path.join(app.root_path, 'chalicelib', 'config.env')
    if not eval:
        eval = {}
    app_config = getattr(app, 'config', {})

    with open(dotenv_path, 'r') as file:
        config_data_string = file.read()
        if len(config_data_string.strip()) > 0:
            file_like = StringIO(config_data_string)
            file_like.seek(0)
            parsed_configs = dotenv_values(stream=file_like)
            print(parsed_configs)
            # for eval_key, eval_value in eval.items():
            #     if not parsed_configs.get(eval_key):
            #         parsed_configs[eval_key] = parsed_configs[eval_key]
            if parsed_configs:
                app_config = {**app_config, **parsed_configs}  # merging two config dicts

    setattr(app, 'config', app_config)
    return app


def configure_redis_cache(app):
    enable_cache = app.config.get('ENABLE_CACHE', False)
    if not enable_cache:
        return app
    redis_client = StrictRedis(host=app.config.get('CACHE_HOST', None), decode_responses=True)
    redis_cache = RedisCache(redis_client=redis_client)
    setattr(app, '__redis_cache', redis_cache)
    return app


def configure_logging(app):
    return app


def configure_templating(app):
    return app
