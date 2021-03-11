from dominate import tags
from markupsafe import Markup
from wtforms.widgets.core import html_params

from .internals import xmlattr


def _add_description(field, **kwargs):
    if field.description:
        _attributes = {
            "id": field.name + "Help",
            "class": "form-text",
        }

        return f'<div { xmlattr(_attributes) }>{ field.description }</div>'

    return ''


def _add_error_message(field_errors):
    if field_errors:
        return f'<div class="invalid-feedback">{ " ".join(field_errors) }</div>'

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

    _attributes = {
        "action": action,
        "method": method,
        "id": id,
        "class": "form " + " ".join(extra_classes),
        "role": role,
        "enctype": enctype if enctype else "",
        **render_kw
    }

    return f'<form { xmlattr(_attributes) } { "novalidate" if novalidate else "" }>{ form }</form>'


def _wrap_field(field, **kwargs):
    root = tags.div()

    _root_classes = ['mb-3']
    _field_classes = ['form-control']
    _field_descripton = Markup(_add_description(field, **kwargs))
    _field_errors = Markup(_add_error_message(field.errors))
    _form_type = kwargs.get('form_type', 'basic')
    _col1_class = ['form-label']
    _col2_class = ['']

    if field.type == 'SelectField':
        _field_classes = ['form-select']

    if field.errors:
        _field_classes.append('is-invalid')

    _field_label = field.label(class_=" ".join(_col1_class))

    if _form_type in ['basic']:
        root.add(_field_label)
        root.add(field(class_=" ".join(_field_classes)))
        root.add(_field_errors)
        root.add(_field_descripton)

    if _form_type in ['horizontal']:
        _root_classes.append('row')
        _cols = kwargs.get('horizontal_columns', ('lg', 2, 10))
        _col1_class = [f'col-{ _cols[0] }-{ _cols[1] }', 'col-form-label']
        _col2_class = [f'col-{ _cols[0] }-{ _cols[2] }']

        _field_label = field.label(class_=" ".join(_col1_class))
        _field_wrap = tags.div(_class=" ".join(_col2_class))
        _field_wrap.add(field(class_=" ".join(_field_classes)))
        _field_wrap.add(_field_errors)
        _field_wrap.add(_field_descripton)
        root.add(_field_label)
        root.add(_field_wrap)

    if _form_type in ['floating']:
        _root_classes.append('form-floating')

        root.add(field(class_=" ".join(_field_classes),
                       placeholder="placeholder"))
        root.add(_field_label)
        root.add(_field_errors)
        root.add(_field_descripton)

    root['class'] = " ".join(_root_classes)

    return root


def _wrap_boolean(field, **kwargs):
    root = tags.div()
    wrap = tags.div(_class='form-check')
    hwrap = tags.div()

    _root_classes = ['mb-3']
    _field_classes = ['form-check-input']
    _label_classes = ['form-check-label']
    _field_descripton = Markup(_add_description(field, **kwargs))
    _field_errors = Markup(_add_error_message(field.errors))
    _form_type = kwargs.get('form_type', 'basic')

    if field.errors:
        _field_classes.append('is-invalid')

    if _form_type in ['horizontal']:
        _cols = kwargs.get('horizontal_columns', ('lg', 2, 10))
        _col1_class = f'offset-{ _cols[0] }-{ _cols[1] }'
        _col2_class = f'col-{ _cols[0] }-{ _cols[2] }'

        _root_classes.append('row')

        hwrap['class'] = ' '.join([_col1_class, _col2_class])

    wrap.add(field(class_=' '.join(_field_classes)))
    wrap.add(field.label(class_=' '.join(_label_classes)))
    wrap.add(_field_errors)
    wrap.add(_field_descripton)

    hwrap.add(wrap)
    root.add(hwrap)

    root['class'] = ' '.join(_root_classes)

    return root


def _wrap_radio(field, **kwargs):
    root = tags.div()
    legend = tags.label(field.label.text)
    wrapper = tags.div()

    _root_classes = ['mb-3']
    _legend_classes = ['form-label', 'pt-0']
    _wrapper_classes = []

    _field_descripton = Markup(_add_description(field, **kwargs))
    _field_errors = Markup(_add_error_message(field.errors))

    if field.errors:
        _wrapper_classes.append('is-invalid')

    _form_type = kwargs.get('form_type', 'basic')

    if _form_type in ['horizontal']:
        _cols = kwargs.get('horizontal_columns', ('lg', 2, 10))
        _col1_class = f'col-{ _cols[0] }-{ _cols[1] }'
        _col2_class = f'col-{ _cols[0] }-{ _cols[2] }'

        _root_classes.append('row')
        _legend_classes.append(_col1_class)
        _wrapper_classes.append(_col2_class)

    for key, value in field.choices:
        item = tags.div(_class='form-check')
        _label = tags.label(
            value,
            _for=key,
            _class='form-check-label',
        )

        _field = tags._input(
            type='radio',
            name=field.name,
            id=key,
            value=key,
            _class='form-check-input',
        )

        if key == field.data:
            _field['checked'] = ''

        item.add(_field)
        item.add(_label)
        wrapper.add(item)

    wrapper.add(_field_errors)
    wrapper.add(_field_descripton)

    legend['class'] = ' '.join(_legend_classes)
    wrapper['class'] = ' '.join(_wrapper_classes)
    root['class'] = ' '.join(_root_classes)

    root.add(legend)
    root.add(wrapper)

    return root


def _wrap_file(field, **kwargs):
    _form_type = kwargs.pop('form_type', 'basic')

    if _form_type in ['floating']:
        return _wrap_field(field, form_type='basic', **kwargs)
    else:
        return _wrap_field(field, form_type=_form_type, **kwargs)


def _wrap_submit(field, **kwargs):
    rv = ''
    _form_type = kwargs.get('form_type', 'basic')
    _cols = kwargs.get('horizontal_columns', ('lg', 2, 10))
    _btn_map = kwargs.get('button_map', {'submit': 'primary'})

    _col1 = f'col-{_cols[0]}-{_cols[1]}'
    _col2 = f'col-{_cols[0]}-{_cols[2]}'

    rv += f'<div class="mb-3 { "row" if _form_type == "horizontal" else "" }">'
    rv += f'<div class="{ _col1 if _form_type == "horizontal" else "" }"></div>'
    rv += f'<div class="{ _col2 if _form_type == "horizontal" else "" }">'
    rv += field(class_=f'btn btn-{ _btn_map.get(field.name) }').unescape()
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
        # if field.type != 'CSRFTokenField':
        #     form_fields += render_field(field, **kwargs)
        form_fields += render_field(field, **kwargs)

        if field.type in ['FileField', 'MultipleFileField']:
            _enctype = _enctype or 'multipart/form-data'

    return Markup(form_fields)


def render_form(form, **kwargs):
    form_fields = ''
    _enctype = kwargs.pop('enctype', None)

    for field in form:
        form_fields += render_field(field, **kwargs)

        if field.type in ['FileField', 'MultipleFileField']:
            _enctype = _enctype or 'multipart/form-data'

    return Markup(_wrap_form(form_fields, enctype=_enctype, **kwargs))


def render_field(field, **kwargs):
    form_field = ''

    if field.type == 'BooleanField':
        form_field = _wrap_boolean(field, **kwargs)
    elif field.type == 'RadioField':
        form_field = _wrap_radio(field, **kwargs)
    elif field.type == 'SubmitField':
        form_field = _wrap_submit(field, **kwargs)
    elif field.type == 'CSRFTokenField':
        form_field = _wrap_csrf(field)
    elif field.type == 'FormField':
        form_field = _wrap_formfield(field.form, **kwargs)
    elif field.type == 'FileField':
        form_field = _wrap_file(field, **kwargs)
    elif field.type == 'FieldList':
        form_field = _wrap_formfield(field.entries, **kwargs)
    else:
        form_field = _wrap_field(field, **kwargs)

    return Markup(form_field)
