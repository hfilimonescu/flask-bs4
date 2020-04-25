from markupsafe import Markup

from wtforms.widgets.core import html_params

from .internals import xmlattr


def _add_description(field, **kwargs):
    rv = ''
    if field.description:
        rv += f'<small id="{ field.name }Help" class="form-text text-muted">'
        rv += field.description
        rv += f'</small>'

    return Markup(rv)


def _add_error_message(field_errors):
    rv = ''
    if field_errors:
        rv += f'<div class="invalid-feedback">{" ".join(field_errors)}</div>'

    return Markup(rv)


def _wrap_form(form,
               action='',
               button_map=None,
               enctype=None,
               extra_classes=[],
               form_type=None,
               horizontal_columns=None,
               id=None,
               method='post',
               novalidate=False,
               role='form',
               render_kw={}):
    _classes = " ".join(extra_classes)

    _render_kw = xmlattr(render_kw)

    form_content = f'<form action="{action}" method="{method}" id="{id}" class="form {_classes}" role="{role}"'
    form_content += f'enctype="{enctype[0] if enctype else ""}" {"novalidate" if novalidate else ""} {_render_kw}>\n'
    form_content += f'{form}\n</form>'

    return Markup(form_content)


def _wrap_field(field, **kwargs):
    rv = ''
    form_type = kwargs.get('form_type', 'basic')
    cols = kwargs.get('horizontal_columns', ('lg', 0, 12))

    field_classes = 'form-control'

    if field.errors:
        field_classes += ' is-invalid'

    if form_type == 'horizontal':
        col1 = 'col-{}-{}'.format(cols[0], cols[1])
        col2 = 'col-{}-{}'.format(cols[0], cols[2])
        off1 = 'offset-{}-{}'.format(cols[0], cols[1])

        rv += Markup('<div class="form-group row">\n')
        rv += Markup(f'\t<div class="{col1}">{field.label}</div>\n')
        rv += Markup(f'\t<div class="{col2}">{field(class_=field_classes)}')
        rv += _add_error_message(field.errors)
        rv += _add_description(field, **kwargs)
        rv += Markup('</div>\n</div>\n')
    else:
        rv += Markup(
            f'<div class="form-group">{field.label} {field(class_=field_classes)}')
        rv += _add_error_message(field.errors)
        rv += _add_description(field, **kwargs)
        rv += Markup('</div>\n')
    return rv


def _wrap_boolean(field, **kwargs):
    content = ''
    form_type = kwargs.get('form_type', 'basic')
    horizontal_columns = kwargs.get('horizontal_columns', ('lg', 0, 12))

    field_classes = 'form-check-input'

    if field.errors:
        field_classes += ' is-invalid'

    col1 = 'col-{}-{}'.format(horizontal_columns[0], horizontal_columns[1])
    col2 = 'col-{}-{}'.format(horizontal_columns[0], horizontal_columns[2])
    off1 = 'offset-{}-{}'.format(horizontal_columns[0], horizontal_columns[1])

    content += Markup(
        f'<div class="form-group { "row" if form_type == "horizontal" else "" }">\n')
    content += Markup(
        f'\t<div class="{ off1 if form_type == "horizontal" else "" } { col2 if form_type == "horizontal" else "" }">')
    content += Markup(f'<div class="form-check">')
    content += field(class_=field_classes)
    content += field.label(class_="form-check-label")
    content += _add_error_message(field.errors)
    content += _add_description(field, **kwargs)
    content += Markup('</div></div></div>')

    return content


def _wrap_radio(field, **kwargs):
    content = ''
    form_type = kwargs.get('form_type', 'basic')
    horizontal_columns = kwargs.get('horizontal_columns', ('lg', 0, 12))

    field_classes = 'form-check-input'
    error_class = ''

    if field.errors:
        error_class = ' is-invalid'
        field_classes += error_class

    col1 = 'col-{}-{}'.format(horizontal_columns[0], horizontal_columns[1])
    col2 = 'col-{}-{}'.format(horizontal_columns[0], horizontal_columns[2])
    off1 = 'offset-{}-{}'.format(horizontal_columns[0], horizontal_columns[1])

    if form_type == 'horizontal':
        content += Markup('<div class="form-group row">\n')
        content += Markup(
            f'\t<legend class="col-form-label {col1} pt-0">{field.label}</legend>\n')
        content += Markup(f'\t<div class="form-check {col2}">')
        for key, value in field.choices:
            content += Markup(
                f'<div class="form-check {col2} {error_class}">\n')
            content += Markup(
                f'<input class="{field_classes}" type="radio" name="{field.name}" id="{key}" value="{key}" {"checked" if key == field.default else ""}>\n')
            content += Markup(
                f'<label class="form-check-label" for="{key}">{value}</label>')
            content += Markup(f'</div>\n')
        content += _add_error_message(field.errors)
        content += _add_description(field, **kwargs)
        content += Markup('</div></div>')
    else:
        content += Markup('<div class="form-group">\n')
        content += Markup(
            f'\t<legend class="col-form-label pt-0">{field.label}</legend>\n')
        content += Markup(f'\t<div class="form-check">')
        for key, value in field.choices:
            content += Markup(f'<div class="form-check {error_class}">\n')
            content += Markup(
                f'<input class="{field_classes}" type="radio" name="{field.name}" id="{key}" value="{key}" {"checked" if key == field.default else ""}>\n')
            content += Markup(
                f'<label class="form-check-label" for="{key}">{value}</label>')
            content += Markup(f'</div>\n')
        content += _add_error_message(field.errors)
        content += _add_description(field, **kwargs)
        content += Markup('</div></div>')

    return content


def _wrap_file(field, **kwargs):
    content = ''
    ft = kwargs.get('form_type', 'basic')
    cols = kwargs.get('horizontal_columns', ('lg', 0, 12))

    field_classes = 'custom-file-input'

    if field.errors:
        field_classes += ' is-invalid'

    col1 = 'col-{}-{}'.format(cols[0], cols[1])
    col2 = 'col-{}-{}'.format(cols[0], cols[2])
    off1 = 'offset-{}-{}'.format(cols[0], cols[1])

    content += Markup(
        f'<div class="form-group { "row" if ft == "horizontal" else "" }">\n')
    content += Markup(
        f'\t<div class="{ col1 if ft == "horizontal" else "" }"></div>\n')
    content += Markup(
        f'\t<div class="{ col2 if ft == "horizontal" else "" }">\n')
    content += Markup(f'\t<div class="custom-file">\n')
    content += field(class_=field_classes)
    content += field.label(class_='custom-file-label')
    content += _add_error_message(field.errors)
    content += _add_description(field, **kwargs)
    content += Markup(f'\n\t</div>\n')
    content += Markup(f'\n\t</div>\n')
    content += Markup(f'</div>\n')

    return content


def _wrap_submit(field, **kwargs):
    content = ''
    form_type = kwargs.get('form_type', 'basic')
    horizontal_columns = kwargs.get('horizontal_columns', ('lg', 0, 12))
    button_map = kwargs.get('button_map', {'submit': 'primary'})

    col1 = 'col-{}-{}'.format(horizontal_columns[0], horizontal_columns[1])
    col2 = 'col-{}-{}'.format(horizontal_columns[0], horizontal_columns[2])
    off1 = 'offset-{}-{}'.format(horizontal_columns[0], horizontal_columns[1])

    content += Markup(
        f'<div class="form-group { "row" if form_type == "horizontal" else "" }">\n')
    content += Markup(
        f'\t<div class="{ col1 if form_type == "horizontal" else "" }"></div>\n')
    content += Markup(
        f'\t<div class="{ col2 if form_type == "horizontal" else "" }">\n')
    content += field(class_=f'btn btn-{ button_map.get(field.name) }')
    content += Markup(f'\n\t</div>\n')
    content += _add_description(field, **kwargs)
    content += Markup(f'</div>\n')

    return content


def _wrap_csrf(field):
    return field()


def render_form(form, **kwargs):
    form_fields = ''
    _enctype = kwargs.get('enctype', [])

    for field in form:
        form_fields += render_field(field, **kwargs)

    return Markup(_wrap_form(form_fields, enctype=_enctype, **kwargs))


def render_field(field, **kwargs):
    form_field = ''

    if field.type == 'BooleanField':
        form_field = _wrap_boolean(field, **kwargs)
    elif field.type == 'RadioField':
        form_field = _wrap_radio(field, **kwargs)
    elif field.type == 'FileField':
        form_field = _wrap_file(field, **kwargs)
    elif field.type == 'SubmitField':
        form_field = _wrap_submit(field, **kwargs)
    elif field.type == 'CSRFTokenField':
        form_field = _wrap_csrf(field)
    else:
        form_field = _wrap_field(field, **kwargs)

    return Markup(form_field)
