from dominate import tags
from markupsafe import Markup


def flash_messages(messages=None, container=False, dismiss='alert-dismissible fade show'):
    if container:
        wrap = tags.div(cls='container flashed-messages')
        row = wrap.add(tags.div(cls='row'))
        col = row.add(tags.div(cls='col-md-12'))
    else:
        wrap = col = tags.div()

    for cat, msg in messages:
        if cat == 'message':
            cat = 'dark'

        with col:
            with tags.div(Markup(msg)):
                tags.attr(cls=f'alert alert-{cat} {dismiss}')
                if dismiss:
                    with tags.button():
                        tags.attr(cls='btn-close')
                        tags.attr(data_bs_dismiss='alert')

    return wrap
