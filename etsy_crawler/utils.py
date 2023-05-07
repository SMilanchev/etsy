def clear_options_items(options: str) -> list[str]:
    res = []
    for el in options.strip().split('\n'):
        res.append(el.strip())

    return res
