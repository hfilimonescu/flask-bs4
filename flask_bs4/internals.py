def xmlattr(d, autospace=True):
    rv = " ".join(
        f'{key}="{value}"'
        for key, value in d.items()
        if value is not None
    )
    if autospace and rv:
        rv = ' ' + rv
    return rv
