def load_ip540():
    from .ip540.configurer import config_controller, config_fetcher

    return config_controller, config_fetcher

mapper = {
    'ip540': load_ip540
}

def load(model):
    return mapper[model]()
