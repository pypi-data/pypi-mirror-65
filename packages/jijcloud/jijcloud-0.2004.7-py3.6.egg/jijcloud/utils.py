
def load_config(file_name: str):
    # TODO: validation content of file
    # ex. check split length (if space ' ' is more than 1 raise error)
    with open(file_name) as f:
        configs = {}
        for s in f.read().splitlines():
            configs[s.split(' ')[0]] = s.split(' ')[1]

        return configs
