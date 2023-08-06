from typing import List


def load_config(config_path, configs: List[str] = None):
    from ehelply_bootstrapper.utils.state import State
    from pymlconf import Root

    if State.config is None:
        State.config = Root()

    State.config.load_file(config_path + '/bootstrap.yaml')
    State.config.load_file(config_path + '/aws.yaml')
    State.config.load_file(config_path + '/fastapi.yaml')
    State.config.load_file(config_path + '/mongo.yaml')
    State.config.load_file(config_path + '/rabbitmq.yaml')
    State.config.load_file(config_path + '/redis.yaml')
    State.config.load_file(config_path + '/sentry.yaml')
    State.config.load_file(config_path + '/sql.yaml')
    State.config.load_file(config_path + '/app.yaml')

    if configs:
        for config in configs:
            State.config.load_file(config_path + '/' + config)
