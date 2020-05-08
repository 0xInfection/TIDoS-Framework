from __future__ import absolute_import

import re
from collections import defaultdict

from ._form_controls import HTMLForm, Label
from ._request import Request
from .polyglot import urljoin, is_string, as_unicode


class SkipControl(ValueError):
    pass


def normalize_line_endings(text):
    return re.sub(as_unicode(r"(?:(?<!\r)\n)|(?:\r(?!\n))"), u"\r\n", text)


def label_text(elem):
    ans = []
    if elem.text:
        ans.append(elem.text)
    for child in elem:
        if child.tail:
            ans.append(child.tail)
    return ''.join(ans)


def parse_control(elem, parent_of, default_type='text'):
    attrs = dict(elem.attrib)
    label_elem = parent_of(elem, 'label')
    if label_elem is not None:
        lt = label_text(label_elem)
        if lt:
            attrs["__label"] = lt
    ctype = attrs.get('type') or default_type
    return ctype, attrs.get('name'), attrs


def parse_input(elem, parent_of, *a):
    return parse_control(elem, parent_of)


def parse_button(elem, parent_of, *a):
    ctype, name, attrs = parse_control(elem, parent_of, default_type='submit')
    ctype += 'button'
    return ctype, name, attrs


def parse_option(elem, parent_of, attrs_map):
    ctype, name, attrs = parse_control(elem, parent_of)
    og = parent_of(elem, 'optgroup')
    contents = (elem.text or '').strip()
    attrs['contents'] = contents
    attrs['value'] = attrs.get('value', contents)
    attrs['label'] = attrs.get('label', contents)
    if og is not None and og.get('disabled') is not None:
        attrs['disabled'] = 'disabled'
    sel = parent_of(elem, 'select')
    if sel is None:
        raise SkipControl()
    attrs['__select'] = sel = attrs_map[sel]['__select']
    return 'select', sel.get('name'), attrs


def parse_textarea(elem, parent_of, *a):
    ctype, name, attrs = parse_control(elem, parent_of)
    ctype = 'textarea'
    attrs['value'] = normalize_line_endings(elem.text or u'')
    return ctype, name, attrs


def parse_select(elem, parent_of, *a):
    ctype, name, attrs = parse_control(elem, parent_of)
    ctype = 'select'
    return ctype, name, {'__select': attrs}


def parse_forms(root, base_url, request_class=None, select_default=False, encoding=None):
    if request_class is None:
        request_class = Request
    global_form = HTMLForm(base_url, encoding=encoding)
    forms, labels = [], []
    form_elems = []
    form_id_map = {}
    all_elems = tuple(
        e for e in root.iter('*') if is_string(e.tag))
    parent_map = {c: p for p in all_elems for c in p}
    id_to_labels = defaultdict(list)
    for e in all_elems:
        q = e.tag.lower()
        if q == 'form':
            form_elems.append(e)
            fid = e.get('id')
            if fid:
                form_id_map[fid] = e
        elif q == 'label':
            for_id = e.get('for')
            if for_id is not None:
                label = Label(label_text(e), for_id)
                labels.append(label)
                id_to_labels[for_id].append(label)
        elif q == 'base':
            base_url = e.get('href') or base_url

    def parent_of(elem, parent_name):
        q = elem
        while True:
            q = parent_map.get(q)
            if q is None:
                return
            if q.tag.lower() == parent_name:
                return q

    forms_map = {}
    for form_elem in form_elems:
        name = form_elem.get('name') or None
        action = form_elem.get('action') or None
        method = form_elem.get('method') or 'GET'
        enctype = form_elem.get(
            'enctype') or "application/x-www-form-urlencoded"
        if action:
            action = urljoin(base_url, action)
        else:
            action = base_url
        form = HTMLForm(action, method, enctype, name, form_elem.attrib,
                        request_class, forms, labels, id_to_labels, encoding=encoding)
        forms_map[form_elem] = form
        forms.append(form)

    attrs_map = {}
    control_names = {
        'option': parse_option,
        'button': parse_button,
        'input': parse_input,
        'textarea': parse_textarea,
        'select': parse_select,
    }

    for i, elem in enumerate(all_elems):
        q = elem.tag.lower()
        cfunc = control_names.get(q)
        if cfunc is not None:
            fid = elem.get('form')
            if fid and fid in form_id_map:
                form_elem = form_id_map[fid]
            else:
                form_elem = parent_of(elem, 'form')
            form = forms_map.get(form_elem, global_form)
            try:
                control_type, control_name, attrs = cfunc(elem, parent_of,
                                                          attrs_map)
            except SkipControl:
                continue
            attrs_map[elem] = attrs
            form.new_control(
                control_type,
                control_name,
                attrs,
                index=i * 10,
                select_default=select_default)

    for form in forms:
        form.fixup()
    global_form.fixup()

    return forms, global_form
