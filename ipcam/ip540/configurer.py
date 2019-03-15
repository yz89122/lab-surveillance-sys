from .controller import Controller
from .fetcher import StreamingFetcher

def config_controller(*args, **kwargs):
    return Controller(
        control_address=kwargs['control_address'],
        admin_username=kwargs['admin_username'],
        admin_password=kwargs['admin_password'],
    )

def config_fetcher(*arg, **kwargs):
    return StreamingFetcher(
        streaming_address=kwargs['streaming_address'],
    )
