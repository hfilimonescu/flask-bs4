from markupsafe import Markup

from wtforms.widgets.core import html_params

from .internals import xmlattr


def _add_description(field, **kwargs):
    rv = ''

    if field.description:
        rv += f'<small id="{ field.name }Help" class="form-text text-muted">'
        rv += field.description
        rv += '</small>'

    return rv


def _add_error_message(field_errors):
    if field_errors:
        return f'<div class="invalid-feedback">{" ".join(field_errors)}</div>'

    return ''


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
    form_content += f'enctype="{enctype if enctype else ""}" {"novalidate" if novalidate else ""} {_render_kw}>'
    form_content += f'{form}</form>'

    return form_content


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

        rv += '<div class="form-group row">'
        rv += f'<div class="{col1}">{field.label}</div>'
        rv += f'<div class="{col2}">{field(class_=field_classes)}'
        rv += _add_error_message(field.errors)
        rv += _add_description(field, **kwargs)
        rv += '</div>'
        rv += '</div>'
    else:
        rv += f'<div class="form-group">{field.label} {field(class_=field_classes)}'
        rv += _add_error_message(field.errors)
        rv += _add_description(field, **kwargs)
        rv += '</div>'
    return rv


def _wrap_boolean(field, **kwargs):
    rv = ''
    form_type = kwargs.get('form_type', 'basic')
    horizontal_columns = kwargs.get('horizontal_columns', ('lg', 0, 12))

    field_classes = 'form-check-input'

    if field.errors:
        field_classes += ' is-invalid'

    col2 = 'col-{}-{}'.format(horizontal_columns[0], horizontal_columns[2])
    off1 = 'offset-{}-{}'.format(horizontal_columns[0], horizontal_columns[1])

    rv += f'<div class="form-group { "row" if form_type == "horizontal" else "" }">'
    rv += f'<div class="{ off1 if form_type == "horizontal" else "" } { col2 if form_type == "horizontal" else "" }">'
    rv += f'<div class="form-check">'
    rv += field(class_=field_classes).unescape()
    rv += field.label(class_="form-check-label").unescape()
    rv += _add_error_message(field.errors)
    rv += _add_description(field, **kwargs)
    rv += f'</div>'
    rv += f'</div>'
    rv += '</div>'

    return rv


def _wrap_radio(field, **kwargs):
    rv = ''
    form_type = kwargs.get('form_type', 'basic')
    horizontal_columns = kwargs.get('horizontal_columns', ('lg', 0, 12))

    field_classes = 'form-check-input'
    error_class = ''

    if field.errors:
        error_class = ' is-invalid'
        field_classes += error_class

    col1 = 'col-{}-{}'.format(horizontal_columns[0], horizontal_columns[1])
    col2 = 'col-{}-{}'.format(horizontal_columns[0], horizontal_columns[2])

    if form_type == 'horizontal':
        rv += f'<div class="form-group row"> \
                <legend class="col-form-label {col1} pt-0"> \
                {field.label} \
                </legend> \
                <div class="form-check {col2}">'
        for key, value in field.choices:
            rv += f'<div class="form-check {col2} {error_class}"> \
                <input class="{field_classes}" type="radio" \
                name = "{field.name}" id = "{key}" value = "{key}" \
                {"checked" if key == field.default else ""}>\
                <label class="form-check-label" for="{key}">{value}</label> \
                </div>'
        rv += _add_error_message(field.errors)
        rv += _add_description(field, **kwargs)
        rv += '</div></div>'
    else:
        rv += f'<div class="form-group"> \
                <legend class="col-form-label pt-0">{field.label}</legend> \
                <div class="form-check">'
        for key, value in field.choices:
            rv += f'<div class="form-check {error_class}">\
                    <input class="{field_classes}" type="radio" \
                        name="{field.name}" id="{key}" value="{key}" \
                        {"checked" if key == field.default else ""}> \
                    <label class="form-check-label" for="{key}">{value}</label>\
                    </div>'
        rv += _add_error_message(field.errors)
        rv += _add_description(field, **kwargs)
        rv += '</div></div>'

    return rv


def _wrap_file(field, **kwargs):
    rv = ''
    ft = kwargs.get('form_type', 'basic')
    cols = kwargs.get('horizontal_columns', ('lg', 0, 12))

    field_classes = 'custom-file-input'

    if field.errors:
        field_classes += ' is-invalid'

    col1 = 'col-{}-{}'.format(cols[0], cols[1])
    col2 = 'col-{}-{}'.format(cols[0], cols[2])

    rv += f'<div class="form-group { "row" if ft == "horizontal" else "" }">'
    rv += f'<div class="{ col1 if ft == "horizontal" else "" }"></div>'
    rv += f'<div class="{ col2 if ft == "horizontal" else "" }">'
    rv += f'<div class="custom-file">'
    rv += field(class_=field_classes).unescape()
    rv += field.label(class_='custom-file-label').unescape()
    rv += _add_error_message(field.errors)
    rv += _add_description(field, **kwargs)
    rv += f'</div>'
    rv += f'</div>'
    rv += f'</div>'

    return rv


def _wrap_submit(field, **kwargs):
    rv = ''
    form_type = kwargs.get('form_type', 'basic')
    horizontal_columns = kwargs.get('horizontal_columns', ('lg', 0, 12))
    button_map = kwargs.get('button_map', {'submit': 'primary'})

    col1 = 'col-{}-{}'.format(horizontal_columns[0], horizontal_columns[1])
    col2 = 'col-{}-{}'.format(horizontal_columns[0], horizontal_columns[2])

    rv += f'<div class="form-group { "row" if form_type == "horizontal" else "" }">'
    rv += f'<div class="{ col1 if form_type == "horizontal" else "" }"></div>'
    rv += f'<div class="{ col2 if form_type == "horizontal" else "" }">'
    rv += field(
        class_=f'btn btn-{ button_map.get(field.name) }').unescape()
    rv += f'</div>'
    rv += _add_description(field, **kwargs)
    rv += f'</div>'

    return rv


def _wrap_csrf(field):
    return field()


def _wrap_formfield(form, **kwargs):
    form_fields = ''
    _enctype = kwargs.pop('enctype', None)

    for field in form:
        if field.type != 'CSRFTokenField':
            form_fields += render_field(field, **kwargs)

        if field.type == 'FileField':
            _enctype = _enctype or 'multipart/form-data'

    return Markup(form_fields)


def render_form(form, **kwargs):
    form_fields = ''
    _enctype = kwargs.pop('enctype', None)

    for field in form:
        form_fields += render_field(field, **kwargs)

        if field.type == 'FileField':
            _enctype = _enctype or 'multipart/form-data'

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
    elif field.type == 'FormField':
        form_field = _wrap_formfield(field.form, **kwargs)
    elif field.type == 'FieldList':
        form_field = _wrap_formfield(field.entries, **kwargs)
    else:
        form_field = _wrap_field(field, **kwargs)

    return Markup(form_field)
