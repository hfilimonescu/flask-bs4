from dominate import tags
from flask import current_app
from markupsafe import Markup

category = {
    'primary': 'bg-primary text-white',
    'secondary': 'bg-secondary text-white',
    'success': 'bg-success text-white',
    'danger': 'bg-danger text-white',
    'warning': 'bg-warning text-black',
    'info': 'bg-info text-white',
    'light': 'bg-light text-black',
    'dark': 'bg-dark text-white',
    'white': 'bg-white text-black',
}

button = {
    'primary': 'btn-close btn-close-white ms-auto me-2',
    'secondary': 'btn-close btn-close-white ms-auto me-2',
    'success': 'btn-close btn-close-white ms-auto me-2',
    'danger': 'btn-close btn-close-white ms-auto me-2',
    'warning': 'btn-close ms-auto me-2',
    'info': 'btn-close ms-auto me-2',
    'light': 'btn-close ms-auto me-2',
    'dark': 'btn-close btn-close-white ms-auto me-2',
    'white': 'btn-close ms-auto me-2',
}


def flash_messages(messages=None, container=False, dismiss=True, autohide=True):
    if dismiss:
        _dismiss = ['alert-dismissible', 'fade', 'show']

    if autohide:
        _dismiss.append('alert-autohide')

    if current_app.config['BOOTSTRAP_USE_TOASTS']:
        return flash_toasts(messages=messages)

    return flash_alerts(
        messages=messages,
        container=container,
        dismiss=' '.join(_dismiss)
    )


def flash_alerts(messages=None, container=False, dismiss=True, autohide=False):
    if dismiss:
        _dismiss = ['alert-dismissible', 'fade', 'show']

    if autohide:
        _dismiss.append('alert-autohide')

    if container:
        wrap = tags.div(cls='container flashed-messages')
        row = wrap.add(tags.div(cls='row'))
        col = row.add(tags.div(cls='col-md-12'))
    else:
        wrap = col = tags.div()

    for message in messages:
        try:
            cat, msg = message
        except ValueError:
            msg = message
            cat = 'message'

        if cat == 'message':
            cat = 'dark'

        with col:
            with tags.div(Markup(msg)):
                tags.attr(cls=f'alert alert-{cat} {" ".join(_dismiss)}')
                if dismiss:
                    with tags.button():
                        tags.attr(cls='btn-close')
                        tags.attr(data_bs_dismiss='alert')

    return wrap


def flash_toasts(messages=None):
    wrap = tags.div()

    for message in messages:
        try:
            cat, msg = message
        except ValueError:
            msg = message
            cat = 'message'

        if cat == 'message':
            cat = 'dark'

        with wrap:
            with tags.div():
                tags.attr(
                    cls=f'toast d-flex m-2 {category[cat]}')
                tags.attr(role='alert')
                tags.attr(
                    data_bs_delay=current_app.config.get(
                        'BOOTSTRAP_TOAST_DELAY', 5000))
                if not current_app.config['BOOTSTRAP_TOAST_AUTOHIDE']:
                    tags.attr(data_bs_autohide='false')
                with tags.div(Markup(msg)):
                    tags.attr(cls=f'toast-body')
                tags.button(cls=f'{button[cat]} pt-4',
                            data_bs_dismiss='toast')

    return wrap
