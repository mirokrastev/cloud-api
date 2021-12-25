convert_map = {
    'kb': lambda arg: arg / 1024 ** 1,
    'mb': lambda arg: arg / 1024 ** 2,
    'gb': lambda arg: arg / 1024 ** 3,
}


def convert(*args, convert_type: str) -> dict:
    # todo implement
    ...
