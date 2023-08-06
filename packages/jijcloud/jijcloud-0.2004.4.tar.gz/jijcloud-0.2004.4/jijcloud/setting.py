import toml


def load_config(file_name: str, config='default') -> dict:
    """load config file (TOML file)

    Args:
        file_name (str): path to config file.
        config (str, optional): loading enviroment name. Defaults to 'default'.

    Raises:
        TypeError: if 'config' enviroment is not defined in config file.

    Returns:
        dict: {'token': 'xxxx', 'url': 'xxxx'} 
    """
    with open(file_name) as f:
        toml_setting_file = toml.load(f)
    if config not in toml_setting_file:
        raise TypeError(
            "'{}' is not define in config file ({}).".format(config, file_name))
    return toml_setting_file
