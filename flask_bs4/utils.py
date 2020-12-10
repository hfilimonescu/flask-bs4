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
    'light': 'bg-light text-dark',
    'dark': 'bg-dark text-white',
    'white': 'bg-white text-dark',
}


def flash_messages(messages=None, container=False, dismiss=True, autohide=True):
    if dismiss:
        _dismiss = ['alert-dismissible', 'fade', 'show']

    if autohide:
        _dismiss.append('alert-autohide')

    if current_app.config['BOOTSTRAP_USE_TOASTS']:
        return flash_toasts(
            messages=messages,
            stacked=container,
            autohide=autohide,
        )
    else:
        return flash_alerts(
            messages=messages,
            container=container,
            dismiss=' '.join(_dismiss)
        )

    return ''


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

    for cat, msg in messages:
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


def flash_toasts(messages=None, stacked=False, autohide=False):
    if stacked:
        wrap = tags.div(
            cls='toast-container')
        row = wrap.add(tags.div(cls='row'))
        col = row.add(tags.div(cls='col-md-12'))
    else:
        wrap = col = tags.div()

    for cat, msg in messages:
        if cat == 'message':
            cat = 'dark'

        with col:
            with tags.div():
                tags.attr(cls=f'toast m-2 {category[cat]}')
                tags.attr(role='alert')
                with tags.div(cls=f'toast-header {category[cat]}'):
                    tags.strong('Toast Message', cls='me-auto')
                    tags.button(cls='btn-close', data_bs_dismiss='toast')
                with tags.div(Markup(msg)):
                    tags.attr(cls=f'toast-body')

    return wrap
