#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# Copyright 2002-2005 John J. Lee <jjl@pobox.com>
# Copyright 2005 Gary Poster
# Copyright 2005 Zope Corporation
# Copyright 1998-2000 Gisle Aas.

import os
import string
import unittest
import warnings
from cStringIO import StringIO
from functools import partial

import mechanize
import mechanize._form as _form
import mechanize._form_controls as _form_controls
import mechanize._testcase as _testcase
from mechanize import (AmbiguityError, ControlNotFoundError, ItemCountError,
                       ItemNotFoundError)
from mechanize._html import content_parser
from mechanize._util import get1

# XXX
# HTMLForm.set/get_value_by_label()
# Base control tests on ParseFile, so can use same tests for different form
#  implementations.
# HTMLForm.enctype
# XHTML


def hide_deprecations():
    warnings.filterwarnings('ignore', category=DeprecationWarning)


def reset_deprecations():
    warnings.filterwarnings('default', category=DeprecationWarning)


def raise_deprecations():
    try:
        registry = _form.__warningregistry__
    except AttributeError:
        pass
    else:
        registry.clear()
    warnings.filterwarnings('error', category=DeprecationWarning)


class DummyForm:
    def __init__(self):
        self._forms = []
        self._labels = []
        self._id_to_labels = {}
        self.backwards_compat = False
        self.controls = []

    def find_control(self, name, type):
        raise mechanize.ControlNotFoundError


def parse_file_ex(file,
                  base_uri,
                  select_default=False,
                  request_class=mechanize.Request,
                  encoding=None,
                  backwards_compat=False,
                  add_global=True):
    raw = file.read()
    root = content_parser(raw, transport_encoding=encoding)
    forms, global_form = _form.parse_forms(
        root,
        base_uri,
        select_default=select_default,
        request_class=request_class)
    if not add_global:
        return list(forms)
    return [global_form] + list(forms)


parse_file = partial(parse_file_ex, add_global=False)


def first_form(text, base_uri="http://example.com/"):
    return parse_file_ex(StringIO(text), base_uri)[0]


class UnescapeTests(unittest.TestCase):  # {{{
    def test_unescape_parsing(self):
        file = StringIO("""<form action="&amp;amp;&mdash;&#x2014;&#8212;">
<textarea name="name&amp;amp;&mdash;&#x2014;&#8212;">val&amp;amp;&mdash;\
&#x2014;&#8212;</textarea>
</form>
""")
        forms = parse_file(
            file,
            "http://localhost/",
            backwards_compat=False,
            encoding="utf-8")
        form = forms[0]
        test_string = "&amp;" + (u"\u2014" * 3)
        self.assertEqual(form.action, "http://localhost/" + test_string)
        control = form.find_control(type="textarea", nr=0)
        self.assertEqual(control.value, "val" + test_string)
        self.assertEqual(control.name, "name" + test_string)

    def test_unescape_parsing_select(self):
        f = StringIO("""\
<form>
<select name="a">
    <option>1&amp;amp;&mdash;&#x2014;&#8212;</option>
    <option value="2&amp;amp;&mdash;&#x2014;&#8212;">2&amp;amp;&mdash;&#x2014;\
&#8212;</option>
</select>
</form>
""")
        forms = parse_file_ex(f, "http://localhost/", encoding="utf-8")
        form = forms[1]
        test_string = "&amp;" + (u"\u2014" * 3)
        control = form.find_control(nr=0)
        for ii in range(len(control.items)):
            item = control.items[ii]
            self.assertEqual(item.name, str(ii + 1) + test_string)
            # XXX label

    def test_unescape_parsing_data(self):
        file = StringIO("""\
<form>
    <label for="foo">Blah &#x201d; &rdquo; blah</label>
    <input type="text" id="foo" name="foo">
</form>
""")
        # don't crash if we can't encode -- rather, leave entity ref intact
        forms = parse_file(
            file,
            "http://localhost/",
            backwards_compat=False,
            encoding="latin-1")
        label = forms[0].find_control(nr=0).get_labels()[0]
        self.assertEqual(label.text, u"Blah \u201d \u201d blah")


class LWPFormTests(unittest.TestCase):
    """The original tests from libwww-perl 5.64."""

    def testEmptyParse(self):
        forms = parse_file(
            StringIO(""), "http://localhost", backwards_compat=False)
        self.assert_(len(forms) == 0)

    def _forms(self):
        file = StringIO("""<form action="abc">

        <input name="firstname" value="Gisle">

        </form>

        """)
        return parse_file(file, "http://localhost/", backwards_compat=False)

    def testParse(self):
        forms = self._forms()
        self.assert_(len(forms) == 1)
        self.assert_(forms[0]["firstname"] == "Gisle")

    def testFillForm(self):
        forms = self._forms()
        form = forms[0]
        form["firstname"] = "Gisle Aas"
        req = form.click()

        def request_method(req):
            if req.has_data():
                return "POST"
            else:
                return "GET"

        self.assert_(request_method(req) == "GET")
        self.assert_(
            req.get_full_url() == "http://localhost/abc?firstname=Gisle+Aas")


def get_header(req, name):
    try:
        return req.get_header(name)
    except AttributeError:
        return req.headers[name]


def header_items(req):
    try:
        return req.header_items()
    except AttributeError:
        return req.headers.items()


class MockResponse:
    def __init__(self, f, url):
        self._file = f
        self._url = url

    def geturl(self):
        return self._url

    def __getattr__(self, name):
        return getattr(self._file, name)


# }}}


class ParseTests(unittest.TestCase):  # {{{
    def test_unknown_control(self):
        f = StringIO("""<form action="abc">
<input type="bogus">
<input>
</form>
""")
        base_uri = "http://localhost/"
        forms = parse_file(f, base_uri, backwards_compat=False)
        form = forms[0]
        for ctl in form.controls:
            self.assert_(isinstance(ctl, _form_controls.TextControl))

    def test_form_attribute(self):
        f = StringIO(
            '''<form id="f"><input name="a"><input name="c" form="o"></form>
            <input name="b" form="f"></input>
            <form id="o"><input name="d"></form>''')
        forms = parse_file(f, 'http://example.com')
        self.assertEqual(len(forms), 2)
        f = forms[0]
        self.assertEqual(len(f.controls), 2)
        self.assertEqual([c.name for c in f.controls], 'a b'.split())
        f = forms[1]
        self.assertEqual(len(f.controls), 2)
        self.assertEqual([c.name for c in f.controls], 'c d'.split())

    def test_ParseFileEx(self):
        # empty "outer form" (where the "outer form" is the form consisting of
        # all controls outside of any form)
        f = StringIO("""<form action="abc">
<input type="text"></input>
</form>
""")
        base_uri = "http://localhost/"
        forms = parse_file_ex(f, base_uri)
        outer = forms[0]
        self.assertEqual(len(forms), 2)
        self.assertEqual(outer.controls, [])
        self.assertEqual(outer.name, None)
        self.assertEqual(outer.action, base_uri)
        self.assertEqual(outer.method, "GET")
        self.assertEqual(outer.enctype, "application/x-www-form-urlencoded")
        self.assertEqual(outer.attrs, {})

        # non-empty outer form
        f = StringIO("""
<input type="text" name="a"></input>
<form action="abc">
  <input type="text" name="b"></input>
</form>
<input type="text" name="c"></input>
<form action="abc">
  <input type="text" name="d"></input>
</form>
<input type="text" name="e"></input>
""")
        base_uri = "http://localhost/"
        forms = parse_file_ex(f, base_uri)
        outer = forms[0]
        self.assertEqual(len(forms), 3)
        self.assertEqual([c.name for c in outer.controls], ["a", "c", "e"])
        self.assertEqual(outer.name, None)
        self.assertEqual(outer.action, base_uri)
        self.assertEqual(outer.method, "GET")
        self.assertEqual(outer.enctype, "application/x-www-form-urlencoded")
        self.assertEqual(outer.attrs, {})

    def test_base_uri(self):
        # BASE element takes priority over document URI
        file = StringIO("""<base HREF="http://example.com">
<form action="abc">
<input type="submit"></input>
</form>
""")
        forms = parse_file(file, "http://localhost/", backwards_compat=False)
        form = forms[0]
        self.assertEqual(form.action, "http://example.com/abc")

        file = StringIO("""<form action="abc">
<input type="submit"></input>
</form>
""")
        forms = parse_file(file, "http://localhost/", backwards_compat=False)
        form = forms[0]
        self.assert_(form.action == "http://localhost/abc")

    def testTextarea(self):
        file = StringIO("""<form action="abc&amp;amp;&mdash;d">

<input name="firstname" value="Gisle">
<textarea>blah, blah,
Rhubarb.

</textarea>

<textarea></textarea>

<textarea name="&quot;ta&quot;" id="foo&amp;amp;bar">Hello testers &amp;amp; \
users!</textarea>

</form>

""")
        forms = parse_file(
            file,
            "http://localhost/",
            backwards_compat=False,
            encoding="utf-8")
        self.assert_(len(forms) == 1)
        form = forms[0]
        self.assert_(form.name is None)
        self.assertEqual(form.action,
                         "http://localhost/abc&amp;" + u"\u2014" + "d")
        control = form.find_control(type="textarea", nr=0)
        self.assert_(control.name is None)
        self.assert_(control.value == "blah, blah,\r\nRhubarb.\r\n\r\n")

        empty_control = form.find_control(type="textarea", nr=1)
        self.assert_(str(empty_control) == "<TextareaControl(<None>=)>")
        self.assert_(empty_control.value == "")

        entity_ctl = form.find_control(type="textarea", nr=2)
        self.assertEqual(entity_ctl.name, '"ta"')
        self.assertEqual(entity_ctl.attrs["id"], "foo&amp;bar")
        self.assertEqual(entity_ctl.value, "Hello testers &amp; users!")

    def testSelect(self):
        file = StringIO("""<form action="abc">

<select name="foo">
 <option>Hello testers &amp; &blah; users!</option>
 <option></option><option></option>
</select>

</form>

""")
        forms = parse_file(file, "http://localhost/", backwards_compat=False)
        self.assert_(len(forms) == 1)
        form = forms[0]

        entity_ctl = form.find_control(type="select")
        self.assert_(entity_ctl.name == "foo")
        self.assertEqual(entity_ctl.value[0], "Hello testers & &blah; users!")

        hide_deprecations()
        opt = entity_ctl.get_item_attrs("Hello testers & &blah; users!")
        reset_deprecations()
        self.assertEqual(opt["value"], "Hello testers & &blah; users!")
        self.assertEqual(opt["label"], "Hello testers & &blah; users!")
        self.assertEqual(opt["contents"], "Hello testers & &blah; users!")

    def testButton(self):
        file = StringIO("""<form action="abc" name="myform">

<input type="text" value="cow" name="moo">

<button name="b">blah, blah,
Rhubarb.</button>

<button type="reset" name="b2"></button>
<button type="button" name="b3"></button>

</form>

""")
        forms = parse_file(file, "http://localhost/", backwards_compat=False)
        form = forms[0]
        self.assert_(form.name == "myform")
        control = form.find_control(name="b")
        self.assertEqual(control.type, "submitbutton")
        self.assert_(control.value == "")
        self.assert_(form.find_control("b2").type == "resetbutton")
        self.assert_(form.find_control("b3").type == "buttonbutton")
        pairs = form.click_pairs()
        self.assert_(pairs == [("moo", "cow"), ("b", "")])

    def testEmptySelect(self):
        file = StringIO("""<form action="abc">
<select name="foo"></select>

<select name="bar" multiple></select>

</form>
""")
        forms = parse_file(file, "http://localhost/", backwards_compat=False)
        form = forms[0]
        control0 = form.find_control(type="select", nr=0)
        control1 = form.find_control(type="select", nr=1)
        self.assert_(str(control0) == "<SelectControl(foo=[])>")
        self.assert_(str(control1) == "<SelectControl(bar=[])>")
        form.set_value([], "foo")
        self.assertRaises(ItemNotFoundError, form.set_value, ["oops"], "foo")
        self.assert_(form.click_pairs() == [])

# XXX figure out what to do in these sorts of cases
#     def badSelect(self):
#         # what objects should these generate, if any?
#         # what should happen on submission of these?
#         # what about similar checkboxes and radios?
# """<form action="abc" name="myform">

# <select multiple>
#  <option>1</option>
#  <option>2</option>
#  <option>3</option>
# </select>

# <select multiple>
#  <option>1</option>
#  <option>2</option>
#  <option>3</option>
# </select>

# </form>
# """

# """<form action="abc" name="myform">

# <select multiple>
#  <option>1</option>
#  <option>2</option>
#  <option>3</option>
#  <option>1</option>
#  <option>2</option>
#  <option>3</option>
# </select>

# </form>
# """
# <select name="foo">
#  <option>1</option>
#  <option>2</option>
#  <option>3</option>
# </select>

# <select name="foo" multiple>
#  <option>4</option>
#  <option>5</option>
#  <option>6</option>
# </select>
# """

# """<form action="abc" name="myform">

# <select>
#  <option>1</option>
#  <option>2</option>
#  <option>3</option>
# </select>

# <select>
#  <option>1</option>
#  <option>2</option>
#  <option>3</option>
# </select>

# </form>
# """

#     def testBadCheckbox(self):
#         # see comments above
#         # split checkbox -- is it one control, or two?

# """
# <html>

# <input type=checkbox name=foo value=bar>
# <input type=checkbox name=foo value=bar>

# <select>
#  <option>1</option>
#  <option>2</option>
# </select>

# <input type=checkbox name=foo value=baz>
# <input type=checkbox name=foo value=bar>

# </html>
# """

    def testUnnamedControl(self):
        file = StringIO("""
<form action="./weird.html">

<input type="checkbox" value="foo"></input>

</form>
""")
        forms = parse_file(file, "http://localhost/", backwards_compat=False)
        form = forms[0]
        self.assert_(form.controls[0].name is None)

    def testNamelessListItems(self):
        # XXX SELECT
        # these controls have no item names
        file = StringIO("""<form action="./weird.html">

<input type="checkbox" name="foo"></input>

<input type="radio" name="bar"></input>

<!--
<select name="baz">
  <option></option>
</select>

<select name="baz" multiple>
  <option></option>
</select>
-->

<input type="submit" name="submit">
</form>
""")
        forms = parse_file(file, "http://localhost/", backwards_compat=False)
        form = forms[0]
        hide_deprecations()
        self.assert_(form.possible_items("foo") == ["on"])
        self.assert_(form.possible_items("bar") == ["on"])
        reset_deprecations()
        # self.assert_(form.possible_items("baz") == [])
        self.assert_(form["foo"] == [])
        self.assert_(form["bar"] == [])
        # self.assert_(form["baz"] == [])
        form["foo"] = ["on"]
        form["bar"] = ["on"]
        pairs = form.click_pairs()
        self.assert_(pairs == [("foo", "on"), ("bar", "on"), ("submit", "")])

    def testSingleSelectFixup(self):
        # HTML 4.01 section 17.6.1: single selection SELECT controls shouldn't
        # have > 1 item selected, but if they do, not more than one should end
        # up selected.
        # In fact, testing really obscure stuff here, which follows Firefox
        # 1.0.7 -- IE doesn't even support disabled OPTIONs.
        file = StringIO("""<form action="./bad.html">

<select name="spam">
  <option selected>1</option>
  <option selected>2</option>
</select>

<select name="cow">
  <option selected>1</option>
  <option disabled selected>2</option>
</select>

<select name="moo">
  <option selected disabled>1</option>
  <option>2</option>
</select>

<select name="nnn">
  <option disabled>1</option>
  <option>2</option>
  <option>3</option>
</select>

</form>
""")
        forms = parse_file(file, "http://localhost/", backwards_compat=False)
        form = forms[0]
        # deselect all but last item if more than one were selected...
        spam = form.find_control("spam")
        self.assertEqual([ii.name for ii in spam.items if ii.selected], ["2"])
        # ...even if it's disabled
        cow = form.find_control("cow")
        self.assertEqual([ii.name for ii in cow.items if ii.selected], ["2"])
        # exactly one selected item is OK even if it's disabled
        moo = form.find_control("moo")
        self.assertEqual([ii.name for ii in moo.items if ii.selected], ["1"])
        # if nothing was selected choose the first non-disabled item
        moo = form.find_control("nnn")
        self.assertEqual([ii.name for ii in moo.items if ii.selected], ["2"])

    def testSelectDefault(self):
        file = StringIO("""<form action="abc" name="myform">

<select name="a" multiple>
 <option>1</option>
 <option>2</option>
 <option>3</option>
</select>

<select name="b">
 <option>1</option>
 <option>2</option>
 <option>3</option>
</select>

</form>

""")
        forms = parse_file(file, "http://localhost/", backwards_compat=False)
        form = forms[0]
        control = form.find_control("a")
        self.assert_(control.value == [])
        single_control = form.find_control("b")
        self.assert_(single_control.value == ["1"])

        file.seek(0)
        forms = parse_file(
            file,
            "http://localhost/",
            select_default=1,
            backwards_compat=False)
        form = forms[0]
        # select_default only affects *multiple* selection select controls
        control = form.find_control(type="select", nr=0)
        self.assert_(control.value == ["1"])
        single_control = form.find_control(type="select", nr=1)
        self.assert_(single_control.value == ["1"])

    def test_close_base_tag(self):
        # Benji York: a single newline immediately after a start tag is
        # stripped by browsers, but not one immediately before an end tag.
        # TEXTAREA content is converted to the DOS newline convention.
        forms = parse_file(
            StringIO("<form><textarea>\n\nblah\n</textarea></form>"),
            "http://example.com/",
            backwards_compat=False, )
        ctl = forms[0].find_control(type="textarea")
        self.assertEqual(ctl.value, "\r\nblah\r\n")

    def test_embedded_newlines(self):
        # newlines that happen to be at the start of strings passed to the
        # parser's .handle_data() method must not be trimmed unless they also
        # follow immediately after a start tag
        forms = parse_file(
            StringIO(
                "<form><textarea>\n\nspam&amp;\neggs\n</textarea></form>"),
            "http://example.com/",
            backwards_compat=False, )
        ctl = forms[0].find_control(type="textarea")
        self.assertEqual(ctl.value, "\r\nspam&\r\neggs\r\n")

    def test_double_select(self):
        # More than one SELECT control of the same name in a form never
        # represent a single control (unlike RADIO and CHECKBOX elements), so
        # don't merge them.
        forms = parse_file(
            StringIO("""\
<form>
    <select name="a">
        <option>b</option>
        <option>c</option>
    </select>
    <select name="a">
        <option>d</option>
        <option>e</option>
    </select>
</form>
"""),
            "http://example.com/",
            backwards_compat=False, )
        form = forms[0]
        self.assertEquals(len(form.controls), 2)
        ctl = form.find_control(name="a", nr=0)
        self.assertEqual([item.name for item in ctl.items], ["b", "c"])
        ctl = form.find_control(name="a", nr=1)
        self.assertEqual([item.name for item in ctl.items], ["d", "e"])

    def test_global_select(self):
        # regression test: closing select and textarea tags should not be
        # ignored, causing a ParseError due to incorrect tag nesting

        parse_file_ex(
            StringIO("""\
<select name="a">
    <option>b</option>
    <option>c</option>
</select>
<select name="a">
    <option>d</option>
    <option>e</option>
</select>
"""),
            "http://example.com/", )

        parse_file(
            StringIO("""\
<textarea></textarea>
<textarea></textarea>
"""),
            "http://example.com/",
            backwards_compat=False, )

    def test_empty_document(self):
        forms = parse_file_ex(StringIO(""), "http://example.com/")
        self.assertEquals(len(forms), 1)  # just the "global form"

    def test_missing_closing_body_tag(self):
        # Even if there is no closing form or body tag, the last form on the
        # page should be returned.
        forms = parse_file_ex(
            StringIO('<form name="spam">'),
            "http://example.com/", )
        self.assertEquals(len(forms), 2)
        self.assertEquals(forms[1].name, "spam")


# }}}


class DisabledTests(unittest.TestCase):  # {{{
    def testOptgroup(self):
        file = StringIO("""<form action="abc" name="myform">

<select name="foo" multiple>
 <option>1</option>
 <optgroup>
 <option>2</option>
 </optgroup>
 <option>3</option>
 <optgroup>
 <option>4</option>
 <option>5</option>
 <option>6</option>
 </optgroup>
 <optgroup disabled>
 <option selected>7</option>
 <option>8</option>
 </optgroup>
 <option>9</option>
 <optgroup disabled>
 <option>10</option>
 </optgroup>
</select>

<select name="bar">
 <option>1</option>
 <optgroup>
 <option>2</option>
 </optgroup>
 <option>3</option>
 <optgroup>
 <option>4</option>
 <option>5</option>
 <option>6</option>
 </optgroup>
 <optgroup disabled>
 <option selected>7</option>
 <option>8</option>
 </optgroup>
 <option>9</option>
 <optgroup disabled>
 <option>10</option>
 </optgroup>
</select>

</form>""")

        def get_control(name, file=file):
            file.seek(0)
            forms = parse_file(
                file, "http://localhost/", backwards_compat=False)
            form = forms[0]
            return form.find_control(name)

        # can't call item_disabled with no args
        control = get_control("foo")
        self.assertRaises(TypeError, control.get_item_disabled)

        hide_deprecations()
        control.set_item_disabled(True, "2")
        reset_deprecations()
        self.assertEqual(
            str(control),
            "<SelectControl(foo=[1, (2), 3, 4, 5, 6, (*7), (8), 9, (10)])>")

        # list controls only allow assignment to .value if no attempt is
        # made to set any disabled item...

        # ...multi selection
        control = get_control("foo")
        extra = []
        # disabled items are not part of the submitted value, so "7" not
        # included (they are not "successful":
        # http://www.w3.org/TR/REC-html40/interact/forms.html#successful-controls
        # ).  This behavior was confirmed in Firefox 1.0.4 at least.
        self.assertEqual(control.value, [] + extra)
        control.value = ["1"]
        self.assertEqual(control.value, ["1"])
        control = get_control("foo")
        self.assertRaises(AttributeError, setattr, control, 'value', ['8'])
        self.assertEqual(control.value, [] + extra)
        # even though 7 is set already, attempt to set it fails
        self.assertRaises(AttributeError, setattr, control, 'value', ['7'])
        control.value = ["1", "3"]
        self.assertEqual(control.value, ["1", "3"])
        control = get_control("foo")
        self.assertRaises(AttributeError, setattr, control, 'value',
                          ['1', '7'])
        self.assertEqual(control.value, [] + extra)
        # enable all items
        control.set_all_items_disabled(False)
        control.value = ['1', '7']
        self.assertEqual(control.value, ["1", "7"])

        control = get_control("foo")
        hide_deprecations()
        for name in 7, 8, 10:
            self.assert_(control.get_item_disabled(str(name)))
            # a disabled option is never "successful" (see above) so never
            # in value
            self.assert_(str(name) not in control.value)
            # a disabled option always is always upset if you try to set it
            self.assertRaises(AttributeError, control.set, True, str(name))
            self.assert_(str(name) not in control.value)
            self.assertRaises(AttributeError, control.set, False, str(name))
            self.assert_(str(name) not in control.value)
            self.assertRaises(AttributeError, control.toggle, str(name))
            self.assert_(str(name) not in control.value)

        control = get_control("foo")
        for name in 1, 2, 3, 4, 5, 6, 9:
            self.assert_(not control.get_item_disabled(str(name)))
            control.set(False, str(name))
            self.assert_(str(name) not in control.value)
            control.toggle(str(name))
            self.assert_(str(name) in control.value)
            control.set(True, str(name))
            self.assert_(str(name) in control.value)
            control.toggle(str(name))
            self.assert_(str(name) not in control.value)

        control = get_control("foo")
        self.assert_(control.get_item_disabled("7"))
        control.set_item_disabled(True, "7")
        self.assert_(control.get_item_disabled("7"))
        self.assertRaises(AttributeError, control.set, True, "7")
        control.set_item_disabled(False, "7")
        self.assert_(not control.get_item_disabled("7"))
        control.set(True, "7")
        control.set(False, "7")
        control.toggle("7")
        control.toggle("7")
        reset_deprecations()

        # ...single-selection
        control = get_control("bar")
        # 7 is selected but disabled
        value = []
        self.assertEqual(control.value, value)
        self.assertEqual([ii.name for ii in control.items if ii.selected],
                         ["7"])
        control.value = ["2"]

        control = get_control("bar")

        def assign_8(control=control):
            control.value = ["8"]

        self.assertRaises(AttributeError, assign_8)
        self.assertEqual(control.value, value)

        def assign_7(control=control):
            control.value = ["7"]

        self.assertRaises(AttributeError, assign_7)
        # enable all items
        control.set_all_items_disabled(False)
        assign_7()
        self.assertEqual(control.value, ['7'])

        control = get_control("bar")
        hide_deprecations()
        for name in 7, 8, 10:
            self.assert_(control.get_item_disabled(str(name)))
            # a disabled option is never "successful" (see above) so never
            # in value
            self.assert_(str(name) not in control.value)
            # a disabled option always is always upset if you try to set it
            self.assertRaises(AttributeError, control.set, True, str(name))
            self.assert_(str(name) not in control.value)
            self.assertRaises(AttributeError, control.set, False, str(name))
            self.assert_(str(name) not in control.value)
            self.assertRaises(AttributeError, control.toggle, str(name))
            self.assert_(str(name) not in control.value)

        control = get_control("bar")
        for name in 1, 2, 3, 4, 5, 6, 9:
            self.assert_(not control.get_item_disabled(str(name)))
            control.set(False, str(name))
            self.assert_(str(name) not in control.value)
            control.toggle(str(name))
            self.assert_(str(name) == control.value[0])
            control.set(True, str(name))
            self.assert_(str(name) == control.value[0])
            control.toggle(str(name))
            self.assert_(str(name) not in control.value)

        control = get_control("bar")
        self.assert_(control.get_item_disabled("7"))
        control.set_item_disabled(True, "7")
        self.assert_(control.get_item_disabled("7"))
        self.assertRaises(AttributeError, control.set, True, "7")
        self.assertEqual(control.value, value)
        control.set_item_disabled(False, "7")
        self.assertEqual(control.value, ["7"])
        self.assert_(not control.get_item_disabled("7"))
        control.set(True, "7")
        control.set(False, "7")
        control.toggle("7")
        control.toggle("7")

        # set_all_items_disabled
        for name in "foo", "bar":
            control = get_control(name)
            control.set_all_items_disabled(False)
            control.set(True, "7")
            control.set(True, "1")
            control.set_all_items_disabled(True)
            self.assertRaises(AttributeError, control.set, True, "7")
            self.assertRaises(AttributeError, control.set, True, "1")
        reset_deprecations()

# XXX single select

    def testDisabledSelect(self):
        for compat in [False, True]:
            self._testDisabledSelect(compat)

    def _testDisabledSelect(self, compat):
        file = StringIO("""<form action="abc" name="myform">

<select name="foo" multiple>
 <option label="a">1</option>
 <option>2</option>
 <option>3</option>
</select>

<select name="bar" multiple>
 <option>1</option>
 <option disabled>2</option>
 <option>3</option>
</select>

<select name="baz" disabled multiple>
 <option>1</option>
 <option>2</option>
 <option>3</option>
</select>

<select name="spam" disabled multiple>
 <option>1</option>
 <option disabled>2</option>
 <option>3</option>
</select>

<!--This is disabled, but fixup still needs to select an option,
 rather than  raising AttributeError-->
<select name="blah" disabled>
 <option>1</option>
 <option>2</option>
 <option>3</option>
</select>

</form>
""")
        hide_deprecations()
        forms = parse_file(file, "http://localhost/", backwards_compat=compat)
        reset_deprecations()
        form = forms[0]
        for name, control_disabled, item_disabled in [
            ("foo", False, False), ("bar", False, True), ("baz", True, False),
            ("spam", True, True)
        ]:
            control = form.find_control(name)
            self.assertEqual(bool(control.disabled), control_disabled)
            hide_deprecations()
            item = control.get_item_attrs("2")
            reset_deprecations()
            self.assertEqual(bool('disabled' in item), item_disabled)

            def bad_assign(value, control=control):
                control.value = value

            hide_deprecations()
            if control_disabled:
                for name in "1", "2", "3":
                    self.assertRaises(AttributeError, control.set, True, name)
                    self.assertRaises(AttributeError, bad_assign, [name])
            elif item_disabled:
                self.assertRaises(AttributeError, control.set, True, "2")
                self.assertRaises(AttributeError, bad_assign, ["2"])
                for name in "1", "3":
                    control.set(True, name)
            else:
                control.value = ["1", "2", "3"]
            reset_deprecations()

        control = form.find_control("foo")
        # missing disabled arg
        hide_deprecations()
        self.assertRaises(TypeError, control.set_item_disabled, "1")
        # by_label
        self.assert_(not control.get_item_disabled("a", by_label=True))
        control.set_item_disabled(True, "a", by_label=True)
        self.assert_(control.get_item_disabled("a", by_label=True))
        reset_deprecations()

    def testDisabledRadio(self):
        for compat in False, True:
            self._testDisabledRadio(compat)

    def _testDisabledRadio(self, compat):
        file = StringIO("""<form>
<input type="checkbox" name="foo" value="1" disabled></input>
<input type="checkbox" name="foo" value="2" disabled></input>
<input type="checkbox" name="foo" value="3" disabled></input>
</form>""")
        hide_deprecations()
        forms = parse_file(file, "http://localhost/", backwards_compat=compat)
        form = forms[0]
        control = form.find_control('foo')

        # since all items are disabled, .fixup() should not select
        # anything
        self.assertEquals(
            [item.name for item in control.items if item.selected],
            [], )
        reset_deprecations()

    def testDisabledCheckbox(self):
        for compat in False, True:
            self._testDisabledCheckbox(compat)

    def _testDisabledCheckbox(self, compat):
        file = StringIO("""<form action="abc" name="myform">

<label><input type="checkbox" name="foo" value="1"></input> a</label>
<input type="checkbox" name="foo" value="2"></input>
<input type="checkbox" name="foo" value="3"></input>

<input type="checkbox" name="bar" value="1"></input>
<input type="checkbox" name="bar" value="2" disabled></input>
<input type="checkbox" name="bar" value="3"></input>

<input type="checkbox" name="baz" value="1" disabled></input>
<input type="checkbox" name="baz" value="2" disabled></input>
<input type="checkbox" name="baz" value="3" disabled></input>

</form>""")
        hide_deprecations()
        forms = parse_file(file, "http://localhost/", backwards_compat=compat)
        reset_deprecations()
        form = forms[0]
        for name, control_disabled, item_disabled in [("foo", False, False),
                                                      ("bar", False, True),
                                                      ("baz", False, True)]:
            control = form.find_control(name)
            self.assert_(bool(control.disabled) == control_disabled)
            hide_deprecations()
            item = control.get_item_attrs("2")
            self.assert_(bool('disabled' in item) == item_disabled)
            self.assert_(control.get_item_disabled("2") == item_disabled)

            def bad_assign(value, control=control):
                control.value = value

            if item_disabled:
                self.assertRaises(AttributeError, control.set, True, "2")
                self.assertRaises(AttributeError, bad_assign, ["2"])
                if not control.get_item_disabled("1"):
                    control.set(True, "1")
            else:
                control.value = ["1", "2", "3"]
            reset_deprecations()

        control = form.find_control("foo")
        hide_deprecations()
        control.set_item_disabled(False, "1")
        # missing disabled arg
        self.assertRaises(TypeError, control.set_item_disabled, "1")
        # by_label
        self.failIf(control.get_item_disabled('a', by_label=True))
        self.assert_(not control.get_item_disabled("1"))
        control.set_item_disabled(True, 'a', by_label=True)
        self.assert_(control.get_item_disabled("1"))
        reset_deprecations()


# }}}


class ControlTests(unittest.TestCase):  # {{{
    def testTextControl(self):
        attrs = {
            "type": "this is ignored",
            "name": "ath_Uname",
            "value": "",
            "maxlength": "20",
            "id": "foo"
        }
        c = _form_controls.TextControl("texT", "ath_Uname", attrs)
        c.fixup()
        self.assert_(c.type == "text")
        self.assert_(c.name == "ath_Uname")
        self.assert_(c.id == "foo")
        self.assert_(c.value == "")
        self.assert_(str(c) == "<TextControl(ath_Uname=)>")
        self.assert_(c.pairs() == [("ath_Uname", "")])

        def bad_assign(c=c):
            c.type = "sometype"

        self.assertRaises(AttributeError, bad_assign)
        self.assert_(c.type == "text")

        def bad_assign(c=c):
            c.name = "somename"

        self.assertRaises(AttributeError, bad_assign)
        self.assert_(c.name == "ath_Uname")
        c.value = "2"
        self.assert_(c.value == "2")

        c.readonly = True
        self.assertRaises(AttributeError, c.clear)
        c.readonly = False
        c.clear()
        self.assert_(c.value is None)

        self.assert_(c.pairs() == [])
        c.value = "2"  # reset value...
        self.assert_(str(c) == "<TextControl(ath_Uname=2)>")

        def bad_assign(c=c):
            c.value = ["foo"]

        self.assertRaises(TypeError, bad_assign)
        self.assert_(c.value == "2")
        self.assert_(not c.readonly)
        c.readonly = True

        def bad_assign(c=c):
            c.value = "foo"

        self.assertRaises(AttributeError, bad_assign)
        self.assert_(c.value == "2")
        c.disabled = True
        self.assert_(
            str(c) == "<TextControl(ath_Uname=2) (disabled, readonly)>")
        c.readonly = False
        self.assert_(str(c) == "<TextControl(ath_Uname=2) (disabled)>")
        self.assertRaises(AttributeError, bad_assign)
        self.assert_(c.value == "2")
        self.assert_(c.pairs() == [])
        c.disabled = False
        self.assert_(str(c) == "<TextControl(ath_Uname=2)>")

        self.assert_('maxlength' in c.attrs)
        for key in "name", "type", "value":
            self.assertIn(key, c.attrs)

        # initialisation of readonly and disabled attributes
        attrs["readonly"] = True
        c = _form_controls.TextControl("text", "ath_Uname", attrs)

        def bad_assign(c=c):
            c.value = "foo"

        self.assertRaises(AttributeError, bad_assign)
        del attrs["readonly"]
        attrs["disabled"] = True
        c = _form_controls.TextControl("text", "ath_Uname", attrs)

        def bad_assign(c=c):
            c.value = "foo"

        self.assertRaises(AttributeError, bad_assign)
        del attrs["disabled"]
        c = _form_controls.TextControl("hidden", "ath_Uname", attrs)
        self.assert_(c.readonly)

        def bad_assign(c=c):
            c.value = "foo"

        self.assertRaises(AttributeError, bad_assign)

    def testFileControl(self):
        c = _form_controls.FileControl("file", "test_file", {})
        fp = StringIO()
        c.add_file(fp)
        fp2 = StringIO()
        c.add_file(fp2, None, "fp2 file test")
        self.assert_(
            str(c) == '<FileControl(test_file=<Unnamed file>, fp2 file test)>')
        c.readonly = True
        self.assertRaises(AttributeError, c.clear)
        c.readonly = False
        c.clear()
        self.assert_(str(c) == '<FileControl(test_file=<No files added>)>')

    def testIgnoreControl(self):
        attrs = {"type": "this is ignored"}
        c = _form_controls.IgnoreControl("reset", None, attrs)
        self.assert_(c.type == "reset")
        self.assert_(c.value is None)
        self.assert_(str(c) == "<IgnoreControl(<None>=<None>)>")

        def set_value(value, c=c):
            c.value = value

        self.assertRaises(AttributeError, set_value, "foo")
        self.assert_(c.value is None)

        # this is correct, but silly; basically nothing should happen
        c.clear()
        self.assert_(c.value is None)

    def testSubmitControl(self):
        attrs = {
            "type": "this is ignored",
            "name": "name_value",
            "value": "value_value",
            "img": "foo.gif"
        }
        c = _form_controls.SubmitControl("submit", "name_value", attrs)
        self.assert_(c.type == "submit")
        self.assert_(c.name == "name_value")
        self.assert_(c.value == "value_value")
        self.assert_(
            str(c) == "<SubmitControl(name_value=value_value) (readonly)>")

        c.readonly = True
        self.assertRaises(AttributeError, c.clear)
        c.readonly = False
        c.clear()
        self.assert_(c.value is None)
        c.value = "value_value"
        c.readonly = True

        def set_value(value, c=c):
            c.value = value

        self.assertRaises(TypeError, set_value, ["foo"])
        c.disabled = True
        self.assertRaises(AttributeError, set_value, "value_value")
        self.assert_(
            str(c) == "<SubmitControl(name_value=value_value) "
            "(disabled, readonly)>")
        c.disabled = False
        c.readonly = False
        set_value("value_value")
        self.assert_(str(c) == "<SubmitControl(name_value=value_value)>")
        c.readonly = True

        # click on button
        form = _form_controls.HTMLForm("http://foo.bar.com/")
        c.add_to_form(form)
        self.assert_(c.pairs() == [])
        pairs = c._click(form, (1, 1), "pairs")
        request = c._click(form, (1, 1), "request")
        data = c._click(form, (1, 1), "request_data")
        self.assert_(c.pairs() == [])
        self.assert_(pairs == [("name_value", "value_value")])
        self.assert_(request.get_full_url() ==
                     "http://foo.bar.com/?name_value=value_value")
        self.assert_(
            data == ("http://foo.bar.com/?name_value=value_value", None, []))
        c.disabled = True
        pairs = c._click(form, (1, 1), "pairs")
        request = c._click(form, (1, 1), "request")
        data = c._click(form, (1, 1), "request_data")
        self.assert_(pairs == [])
        # XXX not sure if should have '?' on end of this URL, or if it really
        # matters...
        self.assert_(request.get_full_url() == "http://foo.bar.com/")
        self.assert_(data == ("http://foo.bar.com/", None, []))
        attrs = {
            "type": "this is ignored",
            "name": "name_value",
            'disabled': 'disabled',
        }
        c = _form_controls.SubmitControl("submit", "name_value", attrs)
        self.assertEqual(c.value, '')

        # form override attributes
        form = _form_controls.HTMLForm("http://foo.bar.com/")
        attrs = {
            "name": "override",
            'formaction': 'http://override.net',
            'formmethod': 'POST',
            'formenctype': 'multipart/form-data',
            'value': 'v'
        }
        c = _form_controls.SubmitControl("submit", "override", attrs)
        c.add_to_form(form)
        req = form.click(name='override')
        self.assertEqual(req.get_full_url(), 'http://override.net')
        self.assertEqual(req.get_method(), 'POST')
        url, data, headers = form.click_request_data(name='override')
        self.assertIn('multipart/form-data', dict(headers)['Content-type'])

    def testImageControl(self):
        attrs = {
            "type": "this is ignored",
            "name": "name_value",
            "img": "foo.gif"
        }
        c = _form_controls.ImageControl("image", "name_value", attrs, index=0)
        self.assert_(c.type == "image")
        self.assert_(c.name == "name_value")
        self.assert_(c.value == "")
        self.assert_(str(c) == "<ImageControl(name_value=)>")

        c.readonly = True
        self.assertRaises(AttributeError, c.clear)
        c.readonly = False
        c.clear()
        self.assert_(c.value is None)
        c.value = ""

        # click, at coordinate (0, 55), on image
        form = _form_controls.HTMLForm("http://foo.bar.com/")
        c.add_to_form(form)
        self.assert_(c.pairs() == [])
        request = c._click(form, (0, 55), "request")
        self.assert_(c.pairs() == [])
        self.assert_(request.get_full_url() ==
                     "http://foo.bar.com/?name_value.x=0&name_value.y=55")
        self.assert_(
            c._click(form, (0, 55), return_type="request_data") == (
                "http://foo.bar.com/?name_value.x=0&name_value.y=55", None,
                []))
        c.value = "blah"
        request = c._click(form, (0, 55), "request")
        self.assertEqual(request.get_full_url(), "http://foo.bar.com/?"
                         "name_value.x=0&name_value.y=55&name_value=blah")

        c.disabled = True
        self.assertEqual(c.value, "blah")
        self.assert_(str(c) == "<ImageControl(name_value=blah) (disabled)>")

        def set_value(value, c=c):
            c.value = value

        self.assertRaises(AttributeError, set_value, "blah")
        self.assert_(c._click(form, (1, 1), return_type="pairs") == [])
        c.readonly = True
        self.assert_(
            str(c) == "<ImageControl(name_value=blah) "
            "(disabled, readonly)>")
        self.assertRaises(AttributeError, set_value, "blah")
        self.assert_(c._click(form, (1, 1), return_type="pairs") == [])
        c.disabled = c.readonly = False
        self.assert_(
            c._click(form, (1, 1),
                     return_type="pairs") == [("name_value.x", "1"),
                                              ("name_value.y", "1"),
                                              ('name_value', 'blah')])

    def testCheckboxControl(self):
        attrs = {
            "type": "this is ignored",
            "name": "name_value",
            "value": "value_value",
            "alt": "some string"
        }
        form = DummyForm()
        c = _form_controls.CheckboxControl("checkbox", "name_value", attrs)
        c.add_to_form(form)
        c.fixup()
        self.assert_(c.type == "checkbox")
        self.assert_(c.name == "name_value")
        self.assert_(c.value == [])
        hide_deprecations()
        self.assert_(c.possible_items() == ["value_value"])
        reset_deprecations()

        def set_type(c=c):
            c.type = "sometype"

        self.assertRaises(AttributeError, set_type)
        self.assert_(c.type == "checkbox")

        def set_name(c=c):
            c.name = "somename"

        self.assertRaises(AttributeError, set_name)
        self.assert_(c.name == "name_value")

        # construct larger list from length-1 lists
        c = _form_controls.CheckboxControl("checkbox", "name_value", attrs)
        attrs2 = attrs.copy()
        attrs2["value"] = "value_value2"
        c2 = _form_controls.CheckboxControl("checkbox", "name_value", attrs2)
        c2.add_to_form(form)
        c.merge_control(c2)
        c.add_to_form(form)
        c.fixup()
        self.assert_(
            str(c) == "<CheckboxControl("
            "name_value=[value_value, value_value2])>")
        hide_deprecations()
        self.assert_(c.possible_items() == ["value_value", "value_value2"])

        attrs = c.get_item_attrs("value_value")
        for key in "alt", "name", "value", "type":
            self.assertIn(key, attrs)
        self.assertRaises(ItemNotFoundError, c.get_item_attrs, "oops")
        reset_deprecations()

        def set_value(value, c=c):
            c.value = value

        c.value = ["value_value", "value_value2"]
        self.assert_(c.value == ["value_value", "value_value2"])
        c.value = ["value_value"]
        self.assertEqual(c.value, ["value_value"])
        self.assertRaises(ItemNotFoundError, set_value, ["oops"])
        self.assertRaises(TypeError, set_value, "value_value")
        c.value = ["value_value2"]
        self.assert_(c.value == ["value_value2"])
        hide_deprecations()
        c.toggle("value_value")
        self.assert_(c.value == ["value_value", "value_value2"])
        c.toggle("value_value2")
        reset_deprecations()
        self.assert_(c.value == ["value_value"])
        hide_deprecations()
        self.assertRaises(ItemNotFoundError, c.toggle, "oops")
        reset_deprecations()

        self.assert_(c.value == ["value_value"])
        c.readonly = True
        self.assertRaises(AttributeError, c.clear)
        c.readonly = False
        c.clear()
        self.assert_(c.value == [])

        # set
        hide_deprecations()
        c.set(True, "value_value")
        self.assert_(c.value == ["value_value"])
        c.set(True, "value_value2")
        self.assert_(c.value == ["value_value", "value_value2"])
        c.set(True, "value_value2")
        self.assert_(c.value == ["value_value", "value_value2"])
        c.set(False, "value_value2")
        self.assert_(c.value == ["value_value"])
        c.set(False, "value_value2")
        self.assert_(c.value == ["value_value"])
        self.assertRaises(ItemNotFoundError, c.set, True, "oops")
        self.assertRaises(TypeError, c.set, True, ["value_value"])
        self.assertRaises(ItemNotFoundError, c.set, False, "oops")
        self.assertRaises(TypeError, c.set, False, ["value_value"])
        reset_deprecations()

        self.assert_(
            str(c) == "<CheckboxControl("
            "name_value=[*value_value, value_value2])>")
        c.disabled = True
        self.assertRaises(AttributeError, set_value, ["value_value"])
        self.assert_(
            str(c) == "<CheckboxControl("
            "name_value=[*value_value, value_value2]) "
            "(disabled)>")
        self.assert_(c.value == ["value_value"])
        self.assert_(c.pairs() == [])
        c.readonly = True
        self.assertRaises(AttributeError, set_value, ["value_value"])
        self.assert_(
            str(c) == "<CheckboxControl("
            "name_value=[*value_value, value_value2]) "
            "(disabled, readonly)>")
        self.assert_(c.value == ["value_value"])
        self.assert_(c.pairs() == [])
        c.disabled = False
        self.assert_(
            str(c) == "<CheckboxControl("
            "name_value=[*value_value, value_value2]) "
            "(readonly)>")
        self.assertRaises(AttributeError, set_value, ["value_value"])
        self.assert_(c.value == ["value_value"])
        self.assert_(c.pairs() == [("name_value", "value_value")])
        c.readonly = False
        c.value = []
        self.assert_(c.value == [])

    def testSelectControlMultiple(self):
        attrs = {
            "type": "this is ignored",
            "name": "name_value",
            "value": "value_value",
            "alt": "some string",
            "label": "contents_value",
            "contents": "contents_value",
            "__select": {
                "type": "this is ignored",
                "name": "select_name",
                "multiple": "",
                "alt": "alt_text"
            }
        }
        form = DummyForm()
        # with Netscape / IE default selection...
        c = _form_controls.SelectControl("select", "select_name", attrs)
        c.add_to_form(form)
        c.fixup()
        self.assert_(c.type == "select")
        self.assert_(c.name == "select_name")
        self.assert_(c.value == [])
        hide_deprecations()
        self.assert_(c.possible_items() == ["value_value"])
        reset_deprecations()
        self.assertIn('name', c.attrs)
        self.assertIn('type', c.attrs)
        self.assert_(c.attrs["alt"] == "alt_text")
        # ... and with RFC 1866 default selection
        c = _form_controls.SelectControl(
            "select", "select_name", attrs, select_default=True)
        c.add_to_form(form)
        c.fixup()
        self.assert_(c.value == ["value_value"])

        # construct larger list from length-1 lists
        c = _form_controls.SelectControl("select", "select_name", attrs)
        attrs2 = attrs.copy()
        attrs2["value"] = "value_value2"
        c2 = _form_controls.SelectControl("select", "select_name", attrs2)
        c2.add_to_form(form)
        c.merge_control(c2)
        c.add_to_form(form)
        c.fixup()
        self.assert_(
            str(c) == "<SelectControl("
            "select_name=[value_value, value_value2])>")
        hide_deprecations()
        self.assert_(c.possible_items() == ["value_value", "value_value2"])

        # get_item_attrs
        attrs3 = c.get_item_attrs("value_value")
        reset_deprecations()
        self.assertIn('alt', attrs3)
        self.assertNotIn('multiple', attrs3)
        # HTML attributes dictionary should have been copied by ListControl
        # constructor.
        attrs["new_attr"] = "new"
        attrs2["new_attr2"] = "new2"
        for key in ("new_attr", "new_attr2"):
            self.assertNotIn(key, attrs3)
        hide_deprecations()
        self.assertRaises(ItemNotFoundError, c.get_item_attrs, "oops")
        reset_deprecations()

        c.value = ["value_value", "value_value2"]
        self.assert_(c.value == ["value_value", "value_value2"])
        c.value = ["value_value"]
        self.assertEqual(c.value, ["value_value"])

        def set_value(value, c=c):
            c.value = value

        self.assertRaises(ItemNotFoundError, set_value, ["oops"])
        self.assertRaises(TypeError, set_value, "value_value")
        self.assertRaises(TypeError, set_value, None)
        c.value = ["value_value2"]
        self.assert_(c.value == ["value_value2"])
        hide_deprecations()
        c.toggle("value_value")
        self.assert_(c.value == ["value_value", "value_value2"])
        c.toggle("value_value2")
        self.assert_(c.value == ["value_value"])
        self.assertRaises(ItemNotFoundError, c.toggle, "oops")
        self.assert_(c.value == ["value_value"])
        reset_deprecations()

        c.readonly = True
        self.assertRaises(AttributeError, c.clear)
        c.readonly = False
        c.clear()
        self.assert_(c.value == [])

        # test ordering of items
        c.value = ["value_value2", "value_value"]
        self.assert_(c.value == ["value_value", "value_value2"])
        # set
        hide_deprecations()
        c.set(True, "value_value")
        self.assert_(c.value == ["value_value", "value_value2"])
        c.set(True, "value_value2")
        self.assert_(c.value == ["value_value", "value_value2"])
        c.set(False, "value_value")
        self.assert_(c.value == ["value_value2"])
        c.set(False, "value_value")
        self.assert_(c.value == ["value_value2"])
        self.assertRaises(ItemNotFoundError, c.set, True, "oops")
        self.assertRaises(TypeError, c.set, True, ["value_value"])
        self.assertRaises(ItemNotFoundError, c.set, False, "oops")
        self.assertRaises(TypeError, c.set, False, ["value_value"])
        reset_deprecations()
        c.value = []
        self.assert_(c.value == [])

    def testSelectControlMultiple_label(self):
        #         <SELECT name=year>
        #          <OPTION value=0 label="2002">current year</OPTION>
        #          <OPTION value=1>2001</OPTION>
        #          <OPTION>2000</OPTION>
        #         </SELECT>
        attrs = {
            "type": "ignored",
            "name": "year",
            "value": "0",
            "label": "2002",
            "contents": "current year",
            "__select": {
                "type": "this is ignored",
                "name": "select_name",
                "multiple": ""
            }
        }
        attrs2 = {
            "type": "ignored",
            "name": "year",
            "value": "1",
            "label": "2001",  # label defaults to contents
            "contents": "2001",
            "__select": {
                "type": "this is ignored",
                "name": "select_name",
                "multiple": ""
            }
        }
        attrs3 = {
            "type": "ignored",
            "name": "year",
            "value": "2000",  # value defaults to contents
            "label": "2000",  # label defaults to contents
            "contents": "2000",
            "__select": {
                "type": "this is ignored",
                "name": "select_name",
                "multiple": ""
            }
        }
        c = _form_controls.SelectControl("select", "select_name", attrs)
        c2 = _form_controls.SelectControl("select", "select_name", attrs2)
        c3 = _form_controls.SelectControl("select", "select_name", attrs3)
        form = DummyForm()
        c.merge_control(c2)
        c.merge_control(c3)
        c.add_to_form(form)
        c.fixup()

        hide_deprecations()
        self.assert_(c.possible_items() == ["0", "1", "2000"])
        self.assert_(
            c.possible_items(by_label=True) == ["2002", "2001", "2000"])

        self.assert_(c.value == [])
        c.toggle("2002", by_label=True)
        self.assert_(c.value == ["0"])
        c.toggle("0")
        self.assert_(c.value == [])
        c.toggle("0")
        self.assert_(c.value == ["0"])
        self.assert_(c.get_value_by_label() == ["2002"])
        c.toggle("2002", by_label=True)
        self.assertRaises(ItemNotFoundError, c.toggle, "blah", by_label=True)
        self.assert_(c.value == [])
        c.toggle("2000")
        reset_deprecations()
        self.assert_(c.value == ["2000"])
        self.assert_(c.get_value_by_label() == ["2000"])

        def set_value(value, c=c):
            c.value = value

        self.assertRaises(ItemNotFoundError, set_value, ["2002"])
        self.assertRaises(TypeError, set_value, "1")
        self.assertRaises(TypeError, set_value, None)
        self.assert_(c.value == ["2000"])
        c.value = ["0"]
        self.assertEqual(c.value, ["0"])
        c.value = []
        self.assertRaises(TypeError, c.set_value_by_label, "2002")
        c.set_value_by_label(["2002"])
        self.assert_(c.value == ["0"])
        self.assert_(c.get_value_by_label() == ["2002"])
        c.set_value_by_label(["2000"])
        self.assert_(c.value == ["2000"])
        self.assert_(c.get_value_by_label() == ["2000"])
        c.set_value_by_label(["2000", "2002"])
        self.assert_(c.value == ["0", "2000"])
        self.assert_(c.get_value_by_label() == ["2002", "2000"])

        c.readonly = True
        self.assertRaises(AttributeError, c.clear)
        c.readonly = False
        c.clear()
        self.assert_(c.value == [])

        c.set_value_by_label(["2000", "2002"])
        hide_deprecations()
        c.set(False, "2002", by_label=True)
        self.assert_(c.get_value_by_label() == c.value == ["2000"])
        c.set(False, "2002", by_label=True)
        self.assert_(c.get_value_by_label() == c.value == ["2000"])
        c.set(True, "2002", by_label=True)
        self.assert_(c.get_value_by_label() == ["2002", "2000"])
        self.assert_(c.value == ["0", "2000"])
        c.set(False, "2000", by_label=True)
        self.assert_(c.get_value_by_label() == ["2002"])
        self.assert_(c.value == ["0"])
        c.set(True, "2001", by_label=True)
        self.assert_(c.get_value_by_label() == ["2002", "2001"])
        self.assert_(c.value == ["0", "1"])
        self.assertRaises(
            ItemNotFoundError, c.set, True, "blah", by_label=True)
        self.assertRaises(
            ItemNotFoundError, c.set, False, "blah", by_label=True)
        reset_deprecations()

    def testSelectControlSingle_label(self):
        #         <SELECT name=year>
        #          <OPTION value=0 label="2002">current year</OPTION>
        #          <OPTION value=1>2001</OPTION>
        #          <OPTION>2000</OPTION>
        #         </SELECT>
        attrs = {
            "type": "ignored",
            "name": "year",
            "value": "0",
            "label": "2002",
            "contents": "current year",
            "__select": {
                "type": "this is ignored",
                "name": "select_name"
            }
        }
        attrs2 = {
            "type": "ignored",
            "name": "year",
            "value": "1",
            "label": "2001",  # label defaults to contents
            "contents": "2001",
            "__select": {
                "type": "this is ignored",
                "name": "select_name"
            }
        }
        attrs3 = {
            "type": "ignored",
            "name": "year",
            "value": "2000",  # value defaults to contents
            "label": "2000",  # label defaults to contents
            "contents": "2000",
            "__select": {
                "type": "this is ignored",
                "name": "select_name"
            }
        }
        c = _form_controls.SelectControl("select", "select_name", attrs)
        c2 = _form_controls.SelectControl("select", "select_name", attrs2)
        c3 = _form_controls.SelectControl("select", "select_name", attrs3)
        form = DummyForm()
        c.merge_control(c2)
        c.merge_control(c3)
        c.add_to_form(form)
        c.fixup()

        hide_deprecations()
        self.assert_(c.possible_items() == ["0", "1", "2000"])
        self.assert_(
            c.possible_items(by_label=True) == ["2002", "2001", "2000"])
        reset_deprecations()

        def set_value(value, c=c):
            c.value = value

        self.assertRaises(ItemNotFoundError, set_value, ["2002"])
        self.assertRaises(TypeError, set_value, "1")
        self.assertRaises(TypeError, set_value, None)
        self.assert_(c.value == ["0"])
        c.value = []
        self.assert_(c.value == [])
        c.value = ["0"]
        self.assert_(c.value == ["0"])

        c.value = []
        self.assertRaises(TypeError, c.set_value_by_label, "2002")
        self.assertRaises(ItemCountError, c.set_value_by_label,
                          ["2000", "2001"])
        self.assertRaises(ItemNotFoundError, c.set_value_by_label, ["foo"])
        c.set_value_by_label(["2002"])
        self.assert_(c.value == ["0"])
        self.assert_(c.get_value_by_label() == ["2002"])
        c.set_value_by_label(["2000"])
        self.assert_(c.value == ["2000"])
        self.assert_(c.get_value_by_label() == ["2000"])

        c.readonly = True
        self.assertRaises(AttributeError, c.clear)
        c.readonly = False
        c.clear()
        self.assert_(c.value == [])

    def testSelectControlSingle(self):
        attrs = {
            "type": "this is ignored",
            "name": "name_value",
            "value": "value_value",
            "label": "contents_value",
            "contents": "contents_value",
            "__select": {
                "type": "this is ignored",
                "name": "select_name",
                "alt": "alt_text"
            }
        }
        # Netscape and IE behaviour...
        c = _form_controls.SelectControl("select", "select_name", attrs)
        form = DummyForm()
        c.add_to_form(form)
        c.fixup()
        self.assert_(c.type == "select")
        self.assert_(c.name == "select_name")
        self.assert_(c.value == ["value_value"])
        hide_deprecations()
        self.assert_(c.possible_items() == ["value_value"])
        reset_deprecations()
        self.assertIn('name', c.attrs)
        self.assertIn('type', c.attrs)
        self.assert_(c.attrs["alt"] == "alt_text")
        # ...and RFC 1866 behaviour are identical (unlike multiple SELECT).
        c = _form_controls.SelectControl(
            "select", "select_name", attrs, select_default=1)
        c.add_to_form(form)
        c.fixup()
        self.assert_(c.value == ["value_value"])

        # construct larger list from length-1 lists
        c = _form_controls.SelectControl("select", "select_name", attrs)
        attrs2 = attrs.copy()
        attrs2["value"] = "value_value2"
        c2 = _form_controls.SelectControl("select", "select_name", attrs2)
        c.merge_control(c2)
        c.add_to_form(form)
        c.fixup()
        self.assert_(
            str(c) == "<SelectControl("
            "select_name=[*value_value, value_value2])>")
        c.value = []
        self.assert_(c.value == [])
        self.assert_(
            str(c) == "<SelectControl("
            "select_name=[value_value, value_value2])>")
        c.value = ["value_value"]
        self.assert_(c.value == ["value_value"])
        self.assert_(
            str(c) == "<SelectControl("
            "select_name=[*value_value, value_value2])>")
        hide_deprecations()
        self.assert_(c.possible_items() == ["value_value", "value_value2"])
        reset_deprecations()

        def set_value(value, c=c):
            c.value = value

        self.assertRaises(ItemCountError, set_value,
                          ["value_value", "value_value2"])
        self.assertRaises(TypeError, set_value, "value_value")
        self.assertRaises(TypeError, set_value, None)
        c.value = ["value_value2"]
        self.assert_(c.value == ["value_value2"])
        c.value = ["value_value"]
        self.assert_(c.value == ["value_value"])
        self.assertRaises(ItemNotFoundError, set_value, ["oops"])
        self.assert_(c.value == ["value_value"])
        hide_deprecations()
        c.toggle("value_value")
        self.assertRaises(ItemNotFoundError, c.toggle, "oops")
        self.assertRaises(TypeError, c.toggle, ["oops"])
        reset_deprecations()
        self.assert_(c.value == [])
        c.value = ["value_value"]
        self.assert_(c.value == ["value_value"])
        # nothing selected is allowed
        c.value = []
        self.assert_(c.value == [])

        hide_deprecations()
        c.set(True, "value_value")
        self.assert_(c.value == ["value_value"])
        c.readonly = True
        self.assertRaises(AttributeError, c.clear)
        c.readonly = False
        c.clear()
        self.assert_(c.value == [])

        # set
        c.set(True, "value_value")
        self.assert_(c.value == ["value_value"])
        c.set(True, "value_value")
        self.assert_(c.value == ["value_value"])
        c.set(True, "value_value2")
        self.assert_(c.value == ["value_value2"])
        c.set(False, "value_value")
        self.assert_("value_value2")
        c.set(False, "value_value2")
        self.assert_(c.value == [])
        c.set(False, "value_value2")
        self.assert_(c.value == [])
        self.assertRaises(ItemNotFoundError, c.set, True, "oops")
        self.assertRaises(TypeError, c.set, True, ["value_value"])
        self.assertRaises(ItemNotFoundError, c.set, False, "oops")
        self.assertRaises(TypeError, c.set, False, ["value_value"])
        reset_deprecations()

    def testRadioControl(self):
        attrs = {
            "type": "this is ignored",
            "name": "name_value",
            "value": "value_value",
            "id": "blah"
        }
        # Netscape and IE behaviour...
        c = _form_controls.RadioControl("radio", "name_value", attrs)
        form = DummyForm()
        c.add_to_form(form)
        c.fixup()
        self.assert_(c.type == "radio")
        self.assert_(c.name == "name_value")
        self.assert_(c.id == "blah")
        self.assert_(c.value == [])
        hide_deprecations()
        self.assert_(c.possible_items() == ["value_value"])
        reset_deprecations()
        # ...and RFC 1866 behaviour
        c = _form_controls.RadioControl(
            "radio", "name_value", attrs, select_default=True)
        c.add_to_form(form)
        c.fixup()
        self.assert_(c.value == ["value_value"])

        # construct larger list from length-1 lists
        c = _form_controls.RadioControl(
            "radio", "name_value", attrs, select_default=True)
        attrs2 = attrs.copy()
        attrs2["value"] = "value_value2"
        c2 = _form_controls.RadioControl(
            "radio", "name_value", attrs2, select_default=True)
        c.merge_control(c2)
        c.add_to_form(form)
        c.fixup()
        self.assert_(
            str(c) == "<RadioControl("
            "name_value=[*value_value, value_value2])>")
        hide_deprecations()
        self.assert_(c.possible_items() == ["value_value", "value_value2"])
        reset_deprecations()

        def set_value(value, c=c):
            c.value = value

        self.assertRaises(ItemCountError, set_value,
                          ["value_value", "value_value2"])
        self.assertRaises(TypeError, set_value, "value_value")
        self.assertEqual(c.value, ["value_value"])
        c.value = ["value_value2"]
        self.assertEqual(c.value, ["value_value2"])
        c.value = ["value_value"]
        self.assertEqual(c.value, ["value_value"])
        self.assertRaises(ItemNotFoundError, set_value, ["oops"])
        self.assertEqual(c.value, ["value_value"])
        hide_deprecations()
        c.toggle("value_value")
        self.assertEqual(c.value, [])
        c.toggle("value_value")
        self.assertEqual(c.value, ["value_value"])
        self.assertRaises(TypeError, c.toggle, ["value_value"])
        self.assertEqual(c.value, ["value_value"])
        # nothing selected is allowed
        c.value = []
        self.assertEqual(c.value, [])

        c.set(True, "value_value")
        reset_deprecations()
        self.assertEqual(c.value, ["value_value"])
        c.readonly = True
        self.assertRaises(AttributeError, c.clear)
        c.readonly = False
        c.clear()
        self.assertEqual(c.value, [])

        # set
        hide_deprecations()
        c.set(True, "value_value")
        self.assertEqual(c.value, ["value_value"])
        c.set(True, "value_value")
        self.assertEqual(c.value, ["value_value"])
        c.set(True, "value_value2")
        self.assertEqual(c.value, ["value_value2"])
        c.set(False, "value_value")
        self.assert_("value_value2")
        c.set(False, "value_value2")
        self.assertEqual(c.value, [])
        c.set(False, "value_value2")
        self.assertEqual(c.value, [])
        self.assertRaises(ItemNotFoundError, c.set, True, "oops")
        self.assertRaises(TypeError, c.set, True, ["value_value"])
        self.assertRaises(ItemNotFoundError, c.set, False, "oops")
        self.assertRaises(TypeError, c.set, False, ["value_value"])
        reset_deprecations()

        # tests for multiple identical values

        attrs = {
            "type": "this is ignored",
            "name": "name_value",
            "value": "value_value",
            "id": "name_value_1"
        }
        c1 = _form_controls.RadioControl("radio", "name_value", attrs)
        attrs = {
            "type": "this is ignored",
            "name": "name_value",
            "value": "value_value",
            "id": "name_value_2",
            "checked": "checked"
        }
        c2 = _form_controls.RadioControl("radio", "name_value", attrs)
        attrs = {
            "type": "this is ignored",
            "name": "name_value",
            "value": "another_value",
            "id": "name_value_3",
            "__label": "Third Option"
        }
        c3 = _form_controls.RadioControl("radio", "name_value", attrs)
        form = DummyForm()
        c1.merge_control(c2)
        c1.merge_control(c3)
        c1.add_to_form(form)
        c1.fixup()
        self.assertEqual(c1.value, ['value_value'])
        hide_deprecations()
        self.assertEqual(c1.possible_items(),
                         ['value_value', 'value_value', 'another_value'])
        reset_deprecations()
        self.assertEqual(c1.value, ['value_value'])
        self.failIf(c1.items[0].selected)
        self.failUnless(c1.items[1].selected)
        self.failIf(c1.items[2].selected)
        c1.value = ['value_value']  # should be no change
        self.failUnless(c1.items[1].selected)
        self.assertEqual(c1.value, ['value_value'])
        c1.value = ['another_value']
        self.failUnless(c1.items[2].selected)
        self.assertEqual(c1.value, ['another_value'])
        c1.value = ['value_value']
        self.failUnless(c1.items[0].selected)
        self.assertEqual(c1.value, ['value_value'])

        # id labels
        form._id_to_labels['name_value_1'] = [
            _form_controls.Label('First Option', 'name_value_1')
        ]
        form._id_to_labels['name_value_2'] = [
            _form_controls.Label('Second Option', 'name_value_2')
        ]
        form._id_to_labels['name_value_3'] = [
            _form_controls.Label('Last Option', 'name_value_3')
        ]  # notice __label above
        self.assertEqual([l.text for l in c1.items[0].get_labels()],
                         ['First Option'])
        self.assertEqual([l.text for l in c1.items[1].get_labels()],
                         ['Second Option'])
        self.assertEqual([l.text for l in c1.items[2].get_labels()],
                         ['Third Option', 'Last Option'])
        self.assertEqual(c1.get_value_by_label(), ['First Option'])
        c1.set_value_by_label(['Second Option'])
        self.assertEqual(c1.get_value_by_label(), ['Second Option'])
        self.assertEqual(c1.value, ['value_value'])
        c1.set_value_by_label(['Third Option'])
        self.assertEqual(c1.get_value_by_label(), ['Third Option'])
        self.assertEqual(c1.value, ['another_value'])
        c1.items[1].selected = True
        self.assertEqual(c1.get_value_by_label(), ['Second Option'])
        self.assertEqual(c1.value, ['value_value'])
        c1.set_value_by_label(['Last Option'])  # by second label
        self.assertEqual(c1.get_value_by_label(), ['Third Option'])
        self.assertEqual(c1.value, ['another_value'])
        c1.set_value_by_label(['irst'])  # by substring
        self.assertEqual(c1.get_value_by_label(), ['First Option'])


# }}}


class FormTests(unittest.TestCase):  # {{{

    base_uri = "http://auth.athensams.net/"

    def _get_test_file(self, filename):
        import test_form
        this_dir = os.path.dirname(test_form.__file__)
        path = os.path.join(this_dir, "test_form_data", filename)
        return open(path)

    def test_find_control(self):
        f = StringIO("""\
<form>
    <label for="form.title"> Book Title </label></td>
    <input type="text" id="form.title" name="form.title"
        value="The Grapes of Wrath" />

    <label for="form.quality">Book Quality</label></td>
    <select id="form.quality" name="form.country">
        <option>Good</option>
        <option>Bad</option>
    </select>

    <label><input type="checkbox" id="form.genre.western" name="form.genre"
        value="western" /> Western</label>
    <label><input type="checkbox" id="form.genre.horror" name="form.genre"
        value="horror" /> Horror</label>

    <label for="form.password">Password</label>
    <input type="password" id="pswd1" name="password" value="123" />
    <input type="password" id="pswd2" name="password" value="123" />
</form>
""")
        form = parse_file(f, "http://example.com/", backwards_compat=False)[0]
        fc = form.find_control

        self.assertEqual(fc("form.title").id, "form.title")
        self.assertEqual(fc("form.title", nr=0).id, "form.title")
        self.assertRaises(AmbiguityError, fc, "password")
        self.assertEqual(fc("password", id="pswd2").id, "pswd2")
        self.assertEqual(fc("password", nr=0).id, "pswd1")
        self.assertRaises(ControlNotFoundError, fc, "form.title", nr=1)
        self.assertRaises(ControlNotFoundError, fc, nr=50)
        self.assertRaises(ValueError, fc, nr=-1)
        self.assertRaises(ControlNotFoundError, fc, label="Bananas")

        # label
        self.assertEqual(fc(label="Title").id, "form.title")
        self.assertEqual(fc(label="Book Title").id, "form.title")
        self.assertRaises(ControlNotFoundError, fc, label=" Book Title ")
        self.assertRaises(ControlNotFoundError, fc, label="Bananas")
        self.assertRaises(ControlNotFoundError, fc, label="title")

        self.assertEqual(fc(label="Book", nr=0).id, "form.title")
        self.assertEqual(fc(label="Book", nr=1).id, "form.quality")
        self.assertRaises(AmbiguityError, fc, label="Book")

    def test_find_nameless_control(self):
        data = """\
<form>
  <input type="checkbox"/>
  <input type="checkbox" id="a" onclick="blah()"/>
</form>
"""
        f = StringIO(data)
        form = parse_file(f, "http://example.com/", backwards_compat=False)[0]
        self.assertRaises(
            AmbiguityError,
            form.find_control,
            type="checkbox",
            name=mechanize.Missing)
        ctl = form.find_control(type="checkbox", name=mechanize.Missing, nr=1)
        self.assertEqual(ctl.id, "a")

    def test_deselect_disabled(self):
        def get_new_form(f, compat):
            f.seek(0)
            form = parse_file(
                f, "http://example.com/", backwards_compat=False)[0]
            form.backwards_compat = compat
            return form

        f = StringIO("""\
<form>
    <input type="checkbox" name="p" value="a" disabled checked></input>
    <input type="checkbox" name="p" value="b"></input>
    <input type="checkbox" name="p" value="c"></input>
</form>
""")
        for compat in [False]:  # True, False:

            def new_form(compat=compat, f=f, get_new_form=get_new_form):
                form = get_new_form(f, compat)
                ctl = form.find_control("p")
                a = ctl.get("a")
                return ctl, a

            ctl, a = new_form()
            ctl.value = ["b"]

            # :-((
            if compat:
                # rationale: allowed to deselect, but not select, disabled
                # items
                ctl, a = new_form()
                self.assertRaises(AttributeError, setattr, a, "selected", True)
                self.assertRaises(AttributeError, setattr, ctl, "value", ["a"])
                a.selected = False
                ctl, a = new_form()
                ctl.value = ["b"]
                self.assertEqual(a.selected, False)
                self.assertEqual(ctl.value, ["b"])
                ctl, a = new_form()
                self.assertRaises(AttributeError, setattr, ctl, "value",
                                  ["a", "b"])
            else:

                # rationale: Setting an individual item's selected state to its
                # present value is a no-op, as is setting the whole control
                # value where an item name doesn't appear in the new value, but
                # that item is disabled anyway (but an item name that does
                # appear in the new value is treated an explicit request that
                # that item name get sent to the server).  However, if the
                # item's state does change, both selecting and deselecting are
                # disallowed for disabled items.

                ctl, a = new_form()
                self.assertRaises(AttributeError, setattr, a, "selected", True)
                ctl, a = new_form()
                self.assertRaises(AttributeError, setattr, ctl, "value", ["a"])
                ctl, a = new_form()
                self.assertRaises(AttributeError, setattr, a, "selected",
                                  False)
                ctl.value = ["b"]
                self.assertEqual(a.selected, True)
                self.assertEqual(ctl.value, ["b"])
                ctl, a = new_form()
                self.assertRaises(AttributeError, setattr, ctl, "value",
                                  ["a", "b"])

        f = StringIO("""\
<form>
    <input type="radio" name="p" value="a" disabled checked></input>
    <input type="radio" name="p" value="b"></input>
    <input type="radio" name="p" value="c"></input>
</form>
""")

        for compat in [False]:  # True, False:

            def new_form(compat=compat, f=f, get_new_form=get_new_form):
                form = get_new_form(f, compat)
                ctl = form.find_control("p")
                a = ctl.get("a")
                return ctl, a

            ctl, a = new_form()
            ctl.value = ["b"]

            if compat:
                ctl, a = new_form()
                self.assertRaises(AttributeError, setattr, a, "selected", True)
                self.assertRaises(AttributeError, setattr, ctl, "value", ["a"])
                a.selected = False
                ctl, a = new_form()
                ctl.value = ["b"]
                self.assertEqual(a.selected, False)
                self.assertEqual(ctl.value, ["b"])
                ctl, a = new_form()
                self.assertRaises(ItemCountError, setattr, ctl, "value",
                                  ["a", "b"])
            else:
                ctl, a = new_form()
                self.assertRaises(AttributeError, setattr, a, "selected", True)
                ctl, a = new_form()
                self.assertRaises(AttributeError, setattr, ctl, "value", ["a"])
                ctl, a = new_form()
                self.assertRaises(AttributeError, setattr, a, "selected",
                                  False)
                ctl.value = ["b"]
                self.assertEqual(a.selected, False)
                self.assertEqual(ctl.value, ["b"])
                ctl, a = new_form()
                self.assertRaises(ItemCountError, setattr, ctl, "value",
                                  ["a", "b"])

    def test_click(self):
        file = StringIO("""<form action="abc" name="myform">

<input type="submit" name="foo"></input>
<input type="submit" name="bar"></input>
</form>
""")
        form = parse_file(file, "http://blah/", backwards_compat=False)[0]
        self.assertRaises(ControlNotFoundError, form.click, nr=2)
        self.assert_(form.click().get_full_url() == "http://blah/abc?foo=")
        self.assert_(
            form.click(name="bar").get_full_url() == "http://blah/abc?bar=")

        for method in ["GET", "POST"]:
            file = StringIO(
                """<form method="%s" action="abc?bang=whizz#doh" name="myform">

<input type="submit" name="foo"></input>
</form>
""" % method)
            # " (this line is here for emacs)
            form = parse_file(file, "http://blah/", backwards_compat=False)[0]
            if method == "GET":
                url = "http://blah/abc?foo="
            else:
                url = "http://blah/abc?bang=whizz"
            self.assert_(form.click().get_full_url() == url)

    def testAuth(self):
        fh = self._get_test_file("Auth.html")
        forms = parse_file(fh, self.base_uri, backwards_compat=False)
        self.assert_(len(forms) == 1)
        form = forms[0]
        self.assert_(form.action == "http://auth.athensams.net/"
                     "?ath_returl=%22http%3A%2F%2Ftame.mimas.ac.uk%2Fisicgi"
                     "%2FWOS-login.cgi%22&ath_dspid=MIMAS.WOS")

        self.assertRaises(
            ControlNotFoundError,
            lambda form=form: form.toggle("d'oh", "oops"))
        self.assertRaises(ControlNotFoundError, lambda form=form: form["oops"])

        def bad_assign(form=form):
            form["oops"] = ["d'oh"]

        self.assertRaises(ControlNotFoundError, bad_assign)

        self.assertRaises(ValueError, form.find_control)

        keys = ["ath_uname", "ath_passwd"]
        values = ["", ""]
        types = ["text", "password"]
        for i in range(len(keys)):
            key = keys[i]
            c = form.find_control(key)
            self.assert_(c.value == values[i])
            self.assert_(c.type == types[i])
        c = form.find_control(type="image")
        self.assert_(c.name is None)
        self.assert_(c.value == "")
        self.assert_(c.type == "image")

        form["ath_uname"] = "jbloggs"
        form["ath_passwd"] = "foobar"

        self.assert_(form.click_pairs() == [("ath_uname", "jbloggs"),
                                            ("ath_passwd", "foobar")])

    def testSearchType(self):
        fh = self._get_test_file("SearchType.html")
        forms = parse_file(fh, self.base_uri, backwards_compat=False)
        self.assert_(len(forms) == 1)
        form = forms[0]

        keys = [
            "SID", "SESSION_DIR", "Full Search", "Easy Search", "New Session",
            "Log off", "Form", "JavaScript"
        ]
        values = [
            "PMrU0IJYy4MAAELSXic_E2011300_PMrU0IJYy4MAAELSXic-0", "", "", "",
            "", "", "Welcome", "No"
        ]
        types = [
            "hidden", "hidden", "image", "image", "image", "image", "hidden",
            "hidden"
        ]
        for i in range(len(keys)):
            key = keys[i]
            self.assert_(form.find_control(key).value == values[i])
            self.assert_(form.find_control(key).type == types[i])

        pairs = form.click_pairs("Full Search")
        self.assert_(pairs == [
            ("SID", "PMrU0IJYy4MAAELSXic_E2011300_PMrU0IJYy4MAAELSXic-0"),
            ("SESSION_DIR", ""), ("Full Search.x", "1"),
            ("Full Search.y", "1"), ("Form", "Welcome"), ("JavaScript", "No")
        ])

    def testFullSearch(self):
        pass  # XXX

    def testGeneralSearch(self):
        fh = self._get_test_file("GeneralSearch.html")
        forms = parse_file(fh, self.base_uri, backwards_compat=False)
        self.assert_(len(forms) == 1)
        form = forms[0]

        keys = [
            "SID", "SESSION_DIR", "Home", "Date & Database Limits",
            "Cited Ref Search", "Log off", "Search", "topic", "titleonly",
            "author", "journal", "address", "Search", "Save query", "Clear",
            "languagetype", "doctype", "Sort", "Form", "Func"
        ]
        values = [
            "PMrU0IJYy4MAAELSXic_E2011300_PMrU0IJYy4MAAELSXic-0", "", "", "",
            "", "", "", "", [], "", "", "", "", "", "", ["All languages"],
            ["All document types"], ["Latest date"], "General", "Search"
        ]
        types = [
            "hidden", "hidden", "image", "image", "image", "image", "image",
            "text", "checkbox", "text", "text", "text", "image", "image",
            "image", "select", "select", "select", "hidden", "hidden"
        ]
        fc = form.find_control
        for i in range(len(keys)):
            name = keys[i]
            type = types[i]
            self.assertEqual(fc(name, nr=0).value, form.get_value(name, nr=0))
            self.assertEqual(fc(name, nr=0).value, values[i])
            self.assertEqual(fc(name, nr=0).type, type)
            self.assertEqual(fc(name, type, nr=0).name, name)
        self.assert_(fc(type="hidden", nr=0).name == "SID")
        self.assert_(fc(type="image", nr=0).name == "Home")
        self.assert_(fc(nr=6).name == "Search")
        self.assertRaises(ControlNotFoundError, fc, nr=50)
        self.assertRaises(ValueError, fc, nr=-1)
        self.assert_(fc("Search", "image", nr=0).name == "Search")
        self.assertRaises(ControlNotFoundError, fc, "Search", "hidden")
        s0 = fc("Search", "image", nr=0)
        s0b = fc("Search", "image", nr=0)
        s1 = fc("Search", "image", nr=1)
        self.assert_(s0.name == s1.name == "Search")
        self.assert_(s0 is s0b)
        self.assert_(s0 is not s1)
        self.assertRaises(ControlNotFoundError, fc, "Search", "image", nr=2)
        self.assert_(fc(type="text", nr=2).name == "journal")
        self.assert_(fc("Search", nr=0) is not fc("Search", nr=1))

        form["topic"] = "foo"
        self.assert_(form["topic"] == "foo")
        form["author"] = "bar"
        form["journal"] = ""
        form["address"] = "baz"
        form["languagetype"] = ["English", "Catalan"]
        self.assert_(form["languagetype"] == ["English", "Catalan"])
        form["titleonly"] = ["on"]
        self.assert_(form["titleonly"] == ["on"])
        pairs = form.click_pairs("Search")
        self.assert_(pairs == [
            ("SID", "PMrU0IJYy4MAAELSXic_E2011300_PMrU0IJYy4MAAELSXic-0"),
            ("SESSION_DIR", ""), ("Search.x", "1"), ("Search.y", "1"),
            ("topic", "foo"), ("titleonly", "on"), ("author", "bar"),
            ("journal", ""), ("address", "baz"), ("languagetype", "English"),
            ("languagetype", "Catalan"), ("doctype", "All document types"),
            ("Sort", "Latest date"), ("Form", "General"), ("Func", "Search")
        ])

        hide_deprecations()
        pvs = form.possible_items("languagetype")
        self.assert_(pvs[0] == "All languages")
        self.assert_(len(pvs) == 47)

        self.assertRaises(
            ItemNotFoundError,
            lambda form=form: form.toggle("d'oh", "languagetype"))
        form.toggle("English", "languagetype")
        self.assert_(form["languagetype"] == ["Catalan"])
        self.assertRaises(TypeError, form.toggle, ["Catalan"], "languagetype")
        self.assertRaises(TypeError, form.toggle, "Catalan", ["languagetype"])

        # XXX type, nr, by_label args

        self.assertRaises(ControlNotFoundError, form.set, True, "blah", "SID")

        # multiple select
        form["languagetype"] = []
        self.assert_(form["languagetype"] == [])
        form.set(True, "Catalan", "languagetype")
        self.assert_(form["languagetype"] == ["Catalan"])
        form.set(True, "English", "languagetype")
        self.assert_(form["languagetype"] == ["English", "Catalan"])
        form.set(False, "English", "languagetype")
        self.assert_(form["languagetype"] == ["Catalan"])
        form.set(False, "Catalan", "languagetype")
        self.assert_(form["languagetype"] == [])
        self.assertRaises(ItemNotFoundError, form.set, True, "doh",
                          "languagetype")
        self.assertRaises(ItemNotFoundError, form.set, False, "doh",
                          "languagetype")
        self.assertRaises(ControlNotFoundError, form.set, True, "blah", "oops")
        self.assertRaises(TypeError, form.set, True, ["Catalan"],
                          "languagetype")
        self.assertRaises(TypeError, form.set, False, ["Catalan"],
                          "languagetype")
        self.assertRaises(TypeError, form.set, True, "Catalan",
                          ["languagetype"])
        self.assertRaises(TypeError, form.set, False, "Catalan",
                          ["languagetype"])

        def setitem(name, value, form=form):
            form[name] = value

        form["languagetype"] = ["Catalan"]
        self.assert_(form["languagetype"] == ["Catalan"])
        self.assertRaises(ItemNotFoundError, setitem, "languagetype", ["doh"])
        self.assertRaises(ControlNotFoundError, setitem, "oops", ["blah"])
        self.assertRaises(TypeError, setitem, ["languagetype"], "Catalan")

        # single select
        form["Sort"] = []
        self.assert_(form["Sort"] == [])
        form.set(True, "Relevance", "Sort")
        self.assert_(form["Sort"] == ["Relevance"])
        form.set(True, "Times Cited", "Sort")
        self.assert_(form["Sort"] == ["Times Cited"])
        form.set(False, "Times Cited", "Sort")
        self.assert_(form["Sort"] == [])
        self.assertRaises(ItemNotFoundError, form.set, True, "doh", "Sort")
        self.assertRaises(ItemNotFoundError, form.set, False, "doh", "Sort")
        self.assertRaises(ControlNotFoundError, form.set, True, "blah", "oops")
        self.assertRaises(TypeError, form.set, True, ["Relevance"], "Sort")
        self.assertRaises(TypeError, form.set, False, ["Relevance"], "Sort")
        self.assertRaises(TypeError, form.set, True, "Relevance", ["Sort"])
        self.assertRaises(TypeError, form.set, False, "Relevance", ["Sort"])
        reset_deprecations()

        form["Sort"] = ["Relevance"]
        self.assert_(form["Sort"] == ["Relevance"])
        self.assertRaises(ItemNotFoundError, setitem, "Sort", ["doh"])
        self.assertRaises(ControlNotFoundError, setitem, "oops", ["blah"])
        self.assertRaises(TypeError, setitem, ["Sort"], ["Relevance"])

    def testSetValueByLabelIgnoringAmbiguity(self):
        # regression test: follow ClientForm 0.1 behaviour
        # also test that backwards_compat argument to ParseFile works
        f = StringIO("""\
<form>
    <select multiple name="form.grocery">
        <option value="bread" id="1">Loaf of Bread</option>
        <option value="bread" id="2">Loaf of Bread</option>
        <option value="challah">Loaf of Challah</option>
    </select>
    <input type="submit" value="Submit" />
</form>
""")
        for kwds, backwards_compat in [
            ({
                "backwards_compat": False
            }, False),
        ]:
            hide_deprecations()
            form = parse_file(f, "http://localhost/", **kwds)[0]
            reset_deprecations()
            f.seek(0)
            c = form.find_control("form.grocery")
            # for item in c.items:
            #    print [label.text for label in item.get_labels()]
            c.set_value_by_label(
                ["Loaf of Bread", "Loaf of Bread", "Loaf of Challah"])
            if backwards_compat:
                # select first item of ambiguous set
                self.assertEqual(c.get_value_by_label(),
                                 ["Loaf of Bread", "Loaf of Challah"])
                self.assertEqual(
                    [item.id for item in c.items if item.selected],
                    ["1", None])
                # disabled items still part of 'value by label'
                c.get(label="Loaf of Challah").disabled = True
                self.assertEqual(c.get_value_by_label(),
                                 ["Loaf of Bread", "Loaf of Challah"])
            else:
                self.assertEqual(
                    c.get_value_by_label(),
                    ["Loaf of Bread", "Loaf of Bread", "Loaf of Challah"])
                self.assertEqual(
                    [item.id for item in c.items if item.selected],
                    ["1", "2", None])
                # disabled items NOT part of 'value by label'
                c.get(label="Challah").disabled = True
                self.assertEqual(c.get_value_by_label(),
                                 ["Loaf of Bread", "Loaf of Bread"])

    def testClearValue(self):
        # regression test: follow ClientForm 0.1 behaviour
        # assigning [] to value is implemented as a special case
        f = StringIO("""\
<form>
    <select multiple name="s">
        <option disabled selected>a</option>
        <option selected>b</option>
    </select>
</form>
""")
        for kwds, backwards_compat in [
            ({
                "backwards_compat": False
            }, False),
        ]:
            hide_deprecations()
            form = parse_file(f, "http://localhost/", **kwds)[0]
            reset_deprecations()
            f.seek(0)
            cc = form.find_control("s")
            if backwards_compat:
                self.assertEqual(cc.value, ["a", "b"])
                cc.value = []
                self.assertEqual([ii.name for ii in cc.items if ii.selected],
                                 [])
            else:
                self.assertEqual(cc.value, ["b"])
                cc.value = []
                # first is disabled, so no need to deselect
                self.assertEqual([ii.name for ii in cc.items if ii.selected],
                                 ["a"])

    def testSearchByLabel(self):
        f = StringIO("""\
<form>
<table>
  <tr>
    <td><label for="form.title">Book Title</label></td>
    <td><input type="text" id="form.title" name="form.title"
               value="The Grapes of Wrath" /></tr>
  </tr>
  <tr>
    <td>Quality</td>
    <td>
      <div>
        <label><input type="radio" id="form.quality.good" name="form.quality"
                      value="good" /> Good</label>
      </div><div>
        <label><input type="radio" id="form.quality.indifferent"
                      name="form.quality" value="indifferent" />
          Indifferent</label>
      </div><div>
        <label><input type="radio" id="form.quality.bad" name="form.quality"
                      value="bad" /> Bad</label>
      </div>
    </td>
  </tr>
  <tr>
    <td><label for="form.country" blah="foo">Country of Origin</label></td>
    <td>
      <select id="form.country" name="form.country">
        <option value="albania">Albania</option>
        <optgroup label="European Union">
          <option label="GB" value="EU: Great Britain">Great Britain</option>
        </optgroup>
        <option value="USA">United States of America</option>
        <option value="zimbabwe">Zimbabwe</option>
      </select>
    </td>
  </tr>
  <tr>
    <td>Genre</label></td>
    <td>
      <div>
        <label><input type="checkbox" id="form.genre.western" name="form.genre"
                      value="western" /> Western</label>
      </div><div>
        <label><input type="checkbox" id="form.genre.sciencefiction"
                      name="form.genre" value="scifi" />
          Science Fiction</label>
      </div><div>
        <label><input type="checkbox" id="form.genre.horror" name="form.genre"
                      value="horror" /> Horror</label>
      </div>
    </td>
  </tr>
  <tr>
    <td><label for="form.password">Password</label></td>
    <td><input type="text" id="form.password" name="form.password"
               value="123" /></tr>
  </tr>
  <tr>
    <td>In this grocery list of requested food items, mark the items you intend
        to purchase:
    </td>
    <td>
      <label><input type="checkbox" name="form.grocery" value="bread" id="1"/>
        Loaf of Bread</label>&nbsp;|
      <label><input type="checkbox" name="form.grocery" value="bread" id="2"/>
        Loaf of Bread</label>&nbsp;|
      <label><input type="checkbox" name="form.grocery" value="bread" id="3"/>
        Loaf of Bread</label>&nbsp;|
      <label><input type="checkbox" name="form.grocery" value="challah"/>
        Loaf of Challah</label>&nbsp;|
      <label><input type="checkbox" name="form.grocery" value="eggs"/>
        Dozen Eggs</label>&nbsp;|
      <label><input type="checkbox" name="form.grocery" value="milk"/>
        Half-Gallon of Milk</label>&nbsp;|
      <label><input type="checkbox" name="form.grocery" value="milk"/>
        Half-Gallon of Milk</label>&nbsp;|
      <label><input type="checkbox" name="form.grocery" value="diapers"/>
        36 30lb. Diapers</label>&nbsp;|
      <label><input type="checkbox" name="form.grocery" value="diapers"/>
        36 30lb. Diapers</label>&nbsp;|
      <label><input type="checkbox" name="form.grocery" value="diapers"/>
        36 30lb. Diapers</label>&nbsp;|
      <label><input type="checkbox" name="form.grocery" value="diapers"/>
        36 30lb. Diapers</label>
    </td>
</table>
<input type="submit" value="Submit" />
</form>
""")
        form = parse_file(f, "http://localhost/", backwards_compat=False)[0]

        # basic tests
        self.assertEqual(
            form.find_control(label="Title").value, "The Grapes of Wrath")
        self.assertEqual(form.find_control(label="Submit").value, "Submit")
        self.assertEqual(
            form.find_control(label="Country").get(label="Britain").name,
            "EU: Great Britain")
        self.assertEqual(
            form.find_control(label="Origin").get(label="GB").name,
            "EU: Great Britain")
        self.assertEqual(form.find_control(label="Password").value, "123")
        self.assertEqual(
            form.find_control(label="Title").value, "The Grapes of Wrath")

        # Test item ambiguity, get, get_items, and set_value_by_label.
        c = form.find_control("form.grocery")
        self.assertRaises(mechanize.AmbiguityError, c.get, label="Loaf")
        self.assertRaises(mechanize.AmbiguityError, c.set_value_by_label,
                          ["Loaf"])
        # If items have the same name (value), set_value_by_label will
        # be happy (since it is just setting the value anyway).
        c.set_value_by_label(["Loaf of Bread"])
        self.assertEqual(c.get_value_by_label(), ["Loaf of Bread"])
        c.set_value_by_label(
            ["Loaf of Bread", "Loaf of Bread", "Loaf of Challah"])
        self.assertEqual(c.get_value_by_label(),
                         ["Loaf of Bread", "Loaf of Bread", "Loaf of Challah"])
        # "get" will still raise an exception, though.
        self.assertRaises(
            mechanize.AmbiguityError, c.get, label="Loaf of Bread")
        # If you want an item, you need to specify which one you want (or use
        # get_items to explicitly get all of them).
        self.assertEqual(c.get(label="Loaf of Bread", nr=0).selected, True)
        self.assertEqual(c.get(label="Loaf of Bread", nr=1).selected, True)
        self.assertEqual(c.get(label="Loaf of Bread", nr=2).selected, False)
        self.assertEqual(c.get(label="Loaf of Challah").selected, True)
        self.assertEqual(
            [i.selected for i in c.get_items(label="Loaf of Bread")],
            [True, True, False])
        self.assertEqual(
            [i.selected for i in c.get_items(label="Loaf of Challah")], [True])
        self.assertEqual(
            [i.name for i in c.get_items(label="Loaf")],
            ["bread", "bread", "bread", "challah"])
        self.assertEqual(
            [i.get_labels()[0].text for i in c.get_items("bread")],
            ["Loaf of Bread", "Loaf of Bread", "Loaf of Bread"])

        # test deprecation
        try:
            for c, f in ((form.find_control("form.genre"), "western"),
                         (form.find_control("form.country"), "zimbabwe"),
                         (form.find_control("form.quality"), "good")):
                # warnings are nasty. :-(
                raise_deprecations()  # clear onceregistry
                try:
                    c.possible_items()
                except DeprecationWarning:
                    pass
                else:
                    self.fail("deprecation failed")
                try:
                    c.toggle_single()
                except DeprecationWarning:
                    pass
                else:
                    self.fail("deprecation failed")
                try:
                    c.set_single(True)
                except DeprecationWarning:
                    pass
                else:
                    self.fail("deprecation failed")
                try:
                    c.toggle(f)
                except DeprecationWarning:
                    pass
                else:
                    self.fail("deprecation failed")
                try:
                    c.get_item_disabled(f)
                except DeprecationWarning:
                    pass
                else:
                    self.fail("deprecation failed")
                try:
                    c.set_item_disabled(True, f)
                except DeprecationWarning:
                    pass
                else:
                    self.fail("deprecation failed")
                try:
                    c.get_item_attrs(True, f)
                except DeprecationWarning:
                    pass
                else:
                    self.fail("deprecation failed")
        finally:
            reset_deprecations()

    def testResults(self):
        fh = self._get_test_file("Results.html")
        forms = parse_file(fh, self.base_uri, backwards_compat=False)
        self.assert_(len(forms) == 1)
        form = forms[0]

        hide_deprecations()
        pvs = form.possible_items("marked_list_candidates")
        reset_deprecations()
        self.assert_(pvs == [
            "000174872000059/1", "000174858300003/2", "000174827900006/3"
        ])

        def bad_setitem(form=form):
            form["marked_list_candidates"] = ["blah"]

        self.assertRaises(ItemNotFoundError, bad_setitem)
        form["marked_list_candidates"] = [pvs[0]]

        # I've removed most of the INPUT elements from this page, and
        # corrected an HTML error
        keys = [
            "Add marked records to list", "Add records on page to list",
            "Add all records retrieved to list", "marked_list_candidates",
            "Add marked records to list", "Add records on page to list",
            "Add all records retrieved to list"
        ]
        types = [
            "image", "image", "image", "checkbox", "image", "image", "image"
        ]
        values = [
            "",
            "",
            "",
            [pvs[0]],
            "",
            "",
            "",
        ]

        for i in range(len(keys)):
            key = keys[i]
            control = form.find_control(key, nr=0)
            self.assert_(control.value == values[i])
            self.assert_(control.type == types[i])

        pairs = form.click_pairs("Add all records retrieved to list")
        self.assert_(pairs == [("Add all records retrieved to list.x", "1"),
                               ("Add all records retrieved to list.y", "1"),
                               ("marked_list_candidates", pvs[0])])

    def testMarkedResults(self):
        fh = self._get_test_file("MarkedResults.html")
        forms = parse_file(fh, self.base_uri, backwards_compat=False)
        self.assert_(len(forms) == 1)
        form = forms[0]

        pairs = form.click_pairs()
        # I've removed most of the INPUT elements from this page, and
        # corrected an HTML error
        self.assert_(
            pairs == [("Add marked records to list.x", "1"),
                      ("Add marked records to list.y", "1"),
                      ("marked_list_candidates", "000174872000059/1"),
                      ("marked_list_candidates", "000174858300003/2"),
                      ("marked_list_candidates", "000174827900006/3")])

    def testMarkedRecords(self):
        pass  # XXX


# }}}


def make_form(html):
    global_form, form = parse_file_ex(StringIO(html), "http://example.com/")
    assert len(global_form.controls) == 0
    return form


def make_form_global(html):
    return get1(parse_file_ex(StringIO(html), "http://example.com/"))


class MoreFormTests(unittest.TestCase):  # {{{
    def test_interspersed_controls(self):
        # must preserve item ordering even across controls
        f = StringIO("""\
<form name="formname">
    <input type="checkbox" name="murphy" value="a"></input>
    <input type="checkbox" name="woof" value="d"></input>
    <input type="checkbox" name="murphy" value="b"></input>
    <input type="checkbox" name="murphy" value="c"></input>
    <input type="submit"></input>
</form>
""")
        form = parse_file(f, "http://blah/", backwards_compat=False)[0]
        form["murphy"] = ["a", "b", "c"]
        form["woof"] = ["d"]
        self.assertEqual(form.click_pairs(), [
            ("murphy", "a"),
            ("woof", "d"),
            ("murphy", "b"),
            ("murphy", "c"),
        ])

        form.method = "POST"
        form.enctype = "multipart/form-data"
        lines = [
            line for line in form.click_request_data()[1].split("\r\n")
            if line != '' and not line.startswith("--")
        ]
        self.assertEqual(lines, [
            'Content-Disposition: form-data; name="murphy"',
            'a',
            'Content-Disposition: form-data; name="woof"',
            'd',
            'Content-Disposition: form-data; name="murphy"',
            'b',
            'Content-Disposition: form-data; name="murphy"',
            'c',
        ])

    def make_form(self):
        f = StringIO("""\
<form blah="nonsense" name="formname">
  <label><input type="checkbox" name="a" value="1" id="1a" blah="spam"></input>
      One</label>
  <label><input type="checkbox" name="a" value="2" blah="eggs"></input>
      Two</label>
  <input type="checkbox" name="a" value="3" id="3a"></input>
      <label for="3a">Three</label>

  <label><input type="radio" name="b" value="1"></input> One</label>
  <label><input type="radio" name="b" value="2" id="2"></input> Two</label>
  <input type="radio" name="b" value="3" id="3"></input>
      <label for="3">Three</label>
  <label for="4"><input type="radio" name="b" value="4" id="4"></input>
      Four</label>

  <select name="c" id="cselect" blah="foo">
    <option id="coption1" blah="bar">1</option>
    <option selected blah="baz">2</option>
    <option id="coption3">3</option>
  </select>

  <select name="d" multiple>
    <option value="v1">l1</option>
    <option value="v2">l2</option>
    <option blah="fee" rhubarb="fi" value="v3">l3</option>
  </select>

  <input type="checkbox" name="e" value="1"></input>
</form>
""")
        return parse_file(f, "http://blah/", backwards_compat=False)[0]

    def test_value(self):
        form = self.make_form()

        form.set_value(["v3"], type="select", kind="multilist")
        self.assert_(form.get_value("d") == ["v3"])
        hide_deprecations()
        form.set_value(["l2"], type="select", kind="multilist", by_label=True)
        self.assert_(form.get_value("d", by_label=True) == ["l2"])

        self.assert_(
            form.get_value("b", "radio", "singlelist", None, 0, False) == [])
        form.set_value(["One"], "b", by_label=True)
        self.assertEqual(
            form.get_value("b", "radio", "singlelist", None, 0, False), ["1"])
        form.set_value(["Three"], "b", by_label=True)
        reset_deprecations()
        self.assertEqual(
            form.get_value("b", "radio", "singlelist", None, 0, False), ["3"])

    def test_id(self):
        form = self.make_form()

        self.assert_(form.find_control("c").id == "cselect")
        self.assert_(form.find_control("a").id == "1a")
        self.assert_(form.find_control("b").id is None)

        self.assert_(form.find_control(id="cselect").id == "cselect")
        self.assertRaises(
            ControlNotFoundError, form.find_control, id="coption1")
        self.assert_(form.find_control(id="1a").id == "1a")
        self.assertRaises(ControlNotFoundError, form.find_control, id="1")

    def test_single(self):
        form = self.make_form()

        hide_deprecations()
        self.assertRaises(ItemCountError, form.set_single, True, "d")
        form.set_single(True, 'e', by_label=True)
        self.assertEqual(form.get_value("e"), ["1"])
        form.set_single(False, 'e', by_label=True)
        self.assertEqual(form.get_value("e"), [])
        form.toggle_single("e", "checkbox", "list", nr=0)
        self.assert_("1" in form.get_value("e"))
        form.set_single(False, "e", "checkbox", "list", nr=0)
        self.assert_("1" not in form.get_value("e"))
        form.set_single(True, "e", "checkbox", "list", nr=0)
        self.assert_("1" in form.get_value("e"))
        reset_deprecations()

    def test_possible_items(self):
        form = self.make_form()
        hide_deprecations()
        self.assert_(form.possible_items("c") == ["1", "2", "3"])
        self.assert_(
            form.possible_items("d", by_label=True) == ["l1", "l2", "l3"])

        self.assert_(form.possible_items("a") == ["1", "2", "3"])
        self.assertEqual(form.possible_items('e', by_label=True), [None])
        self.assertEqual(
            form.possible_items('a', by_label=True), ['One', 'Two', 'Three'])
        self.assertEqual(
            form.possible_items('b', by_label=True),
            ['One', 'Two', 'Three', 'Four'])
        reset_deprecations()

    def test_set_all_readonly(self):
        form = self.make_form()

        form.set_all_readonly(True)
        for c in form.controls:
            self.assert_(c.readonly)
        form.set_all_readonly(False)
        for c in form.controls:
            self.assert_(not c.readonly)

    def test_clear_all(self):
        form = self.make_form()
        form.set_all_readonly(True)
        self.assertRaises(AttributeError, form.clear_all)
        form.set_all_readonly(False)
        form.clear_all()
        for c in form.controls:
            self.assert_(not c.value)

    def test_clear(self):
        form = self.make_form()
        form.set_all_readonly(True)
        self.assertRaises(AttributeError, form.clear, "b")
        form.set_all_readonly(False)
        form["b"] = ["1"]
        self.assertEqual(form["b"], ["1"])
        form.clear("b")
        self.assertEqual(form["b"], [])

    def test_attrs(self):
        form = self.make_form()

        self.assert_(form.attrs["blah"] == "nonsense")
        self.assert_(form.attrs["name"] == "formname")

        a = form.find_control("a")
        self.assertRaises(AttributeError, getattr, a, 'attrs')
        hide_deprecations()
        self.assert_(a.get_item_attrs("1")["blah"] == "spam")
        self.assert_(a.get_item_attrs("2")["blah"] == "eggs")
        self.assertNotIn('blah', a.get_item_attrs("3"))

        c = form.find_control("c")
        self.assert_(c.attrs["blah"] == "foo")
        self.assert_(c.get_item_attrs("1")["blah"] == "bar")
        self.assert_(c.get_item_attrs("2")["blah"] == "baz")
        self.assertNotIn('blah', c.get_item_attrs("3"))
        reset_deprecations()

    def test_select_control_nr_and_label(self):
        for compat in [False, True]:
            self._test_select_control_nr_and_label(compat)

    def _test_select_control_nr_and_label(self, compat):
        f = StringIO("""\
<form>
    <select multiple name="form.grocery">
        <option value="p" label="a" id="1">a</option>
        <option value="q" label="b" id="2">a</option>
        <option value="p" label="a" id="3">b</option>
    </select>
</form>
""")
        if compat:
            hide_deprecations()
        form = parse_file(f, "http://example.com/", backwards_compat=compat)[0]
        if compat:
            reset_deprecations()
        ctl = form.find_control("form.grocery")
        # ordinary case
        self.assertEqual(ctl.get("p", nr=1).id, "3")
        # nr too high
        self.assertRaises(ItemNotFoundError, ctl.get, "p", nr=50)
        # first having label "a"
        self.assertEqual(ctl.get(label="a", nr=0).id, "1")
        # second having label "a"...
        item = ctl.get(label="a", nr=1)
        # ...as opposed to second with label attribute "a"! -- each item
        # has multiple labels accessible by .get_labels(), but only one
        # label HTML-attribute
        self.assertEqual(item.id, "2")
        self.assertEqual(item.attrs.get("label"), "b")  # !
        # third having label "a" (but only the second whose label is "a")
        self.assertEqual(ctl.get(label="a", nr=1).id, "2")
        # nr too high again
        self.assertRaises(ItemNotFoundError, ctl.get, label="a", nr=3)

        self.assertEqual(ctl.get(id="2").id, "2")
        self.assertRaises(ItemNotFoundError, ctl.get, id="4")
        self.assertRaises(ItemNotFoundError, ctl.get, id="4")

    def test_label_whitespace(self):
        f = StringIO("""\
<form>
<select multiple name="eg">
    <option value="p"> a b  c  </option>
    <option value="q">b</option>
</select>
</form>
""")
        form = parse_file(f, "http://example.com/")[0]
        ctl = form.find_control("eg")
        p = ctl.get("p")
        q = ctl.get("q")
        self.assertEqual(p.get_labels()[0].text, ("a b c"))
        self.assertEqual(q.get_labels()[0].text, "b")

    def test_nameless_list_control(self):
        # ListControls are built up from elements that match by name and type
        # attributes.  Nameless controls cause some tricky cases.  We should
        # get a new control for nameless controls.
        for data in [
                """\
<form>
  <input type="checkbox" name="foo"/>
  <input type="checkbox" name="bar"/>
  <input type="checkbox" id="a" onclick="bar()" checked />
</form>
""",
                """\
<form>
  <input type="checkbox" name="foo"/>
  <input type="checkbox" id="a" onclick="bar()" checked />
</form>
""",
                """\
<form>
  <input type="checkbox"/>
  <input type="checkbox"/>
  <input type="checkbox" id="a" onclick="bar()" checked />
</form>
""",
        ]:
            f = StringIO(data)
            form = parse_file(
                f, "http://example.com/", backwards_compat=False)[0]
            bar = form.find_control(type="checkbox", id="a")
            # should have value "on", but not be successful
            self.assertEqual([item.name for item in bar.items], ["on"])
            self.assertEqual(bar.value, [])
            self.assertEqual(form.click_pairs(), [])

    def test_action_with_fragment(self):
        for method in ["GET", "POST"]:
            data = ('<form action="" method="%s">'
                    '<input type="submit" name="s"/></form>' % method)
            f = StringIO(data)
            form = parse_file(
                f, "http://example.com/", backwards_compat=False)[0]
            self.assertEqual(
                form.click().get_full_url(),
                "http://example.com/" + (method == "GET" and "?s=" or ""), )

    def test_click_empty_form_by_label(self):
        # http://github.com/jjlee/mechanize/issues#issue/16
        form = make_form_global("")
        assert len(form.controls) == 0
        self.assertRaises(
            mechanize.ControlNotFoundError,
            form.click,
            label="no control has this label")


# }}}


class ContentTypeTests(unittest.TestCase):  # {{{
    def test_content_type(self):
        class OldStyleRequest:
            def __init__(self, url, data=None, hdrs=None):
                self.ah = self.auh = False

            def add_header(self, key, val):
                self.ah = True

        class NewStyleRequest(OldStyleRequest):
            def add_unredirected_header(self, key, val):
                self.auh = True

        class FakeForm(_form_controls.HTMLForm):
            def __init__(self, hdr):
                self.hdr = hdr

            def _request_data(self):
                return "http://example.com", "", [(self.hdr, "spam")]

        for request_class, hdr, auh in [
            (OldStyleRequest, "Foo", False),
            (NewStyleRequest, "Foo", False),
            (OldStyleRequest, "Content-type", False),
            (NewStyleRequest, "Content-type", True),
        ]:
            form = FakeForm(hdr)
            req = form._switch_click("request", request_class)
            self.assertEqual(req.auh, auh)
            self.assertEqual(req.ah, not auh)


# }}}


class FunctionTests(unittest.TestCase):  # {{{
    def test_normalize_line_endings(self):
        def check(text, expected, self=self):
            got = _form.normalize_line_endings(text)
            self.assertEqual(got, expected)

        # unix
        check("foo\nbar", "foo\r\nbar")
        check("foo\nbar\n", "foo\r\nbar\r\n")
        # mac
        check("foo\rbar", "foo\r\nbar")
        check("foo\rbar\r", "foo\r\nbar\r\n")
        # dos
        check("foo\r\nbar", "foo\r\nbar")
        check("foo\r\nbar\r\n", "foo\r\nbar\r\n")

        # inconsistent -- we just blithely convert anything that looks like a
        # line ending to the DOS convention, following Firefox's behaviour when
        # normalizing textarea content
        check("foo\r\nbar\nbaz\rblah\r\n", "foo\r\nbar\r\nbaz\r\nblah\r\n")

        # pathological ;-O
        check("\r\n\n\r\r\r\n", "\r\n" * 5)


# }}}


class CaseInsensitiveDict:  # {{{
    def __init__(self, items):
        self._dict = {}
        for key, val in items:
            self._dict[string.lower(key)] = val

    def __getitem__(self, key):
        return self._dict[key]

    def __getattr__(self, name):
        return getattr(self._dict, name)


# }}}


class UploadTests(_testcase.TestCase):  # {{{
    def test_choose_boundary(self):
        bndy = _form_controls.choose_boundary()
        ii = string.find(bndy, '.')
        self.assert_(ii < 0)

    def make_form(self):
        html = """\
<form action="/cgi-bin/upload.cgi" method="POST" enctype="multipart/form-data">
<input type="file" name="data">
<input type="text" name="user" value="nobody">
<br>
<input type="submit">
</form>
"""

        return parse_file(
            StringIO(html),
            "http://localhost/cgi-bin/upload.cgi",
            backwards_compat=False)[0]

    def test_file_request(self):
        import cgi

        # fill in a file upload form...
        form = self.make_form()
        form["user"] = "john"
        data_control = form.find_control("data")
        data = "blah\nbaz\n"
        data_control.add_file(StringIO(data))
        # print "data_control._upload_data", data_control._upload_data
        req = form.click()
        self.assertTrue(
            get_header(req, "Content-type").startswith(
                "multipart/form-data; boundary="))

        # print "req.get_data()\n>>%s<<" % req.get_data()

        # ...and check the resulting request is understood by cgi module
        fs = cgi.FieldStorage(
            StringIO(req.get_data()),
            CaseInsensitiveDict(header_items(req)),
            environ={"REQUEST_METHOD": "POST"})
        self.assert_(fs["user"].value == "john")
        self.assert_(fs["data"].value == data)
        self.assertEquals(fs["data"].filename, "")

    def test_file_request_with_filename(self):
        import cgi

        # fill in a file upload form...
        form = self.make_form()
        form["user"] = "john"
        data_control = form.find_control("data")
        data = "blah\nbaz\n"
        data_control.add_file(StringIO(data), filename="afilename")
        req = form.click()
        self.assert_(
            get_header(req, "Content-type").startswith(
                "multipart/form-data; boundary="))

        # ...and check the resulting request is understood by cgi module
        fs = cgi.FieldStorage(
            StringIO(req.get_data()),
            CaseInsensitiveDict(header_items(req)),
            environ={"REQUEST_METHOD": "POST"})
        self.assert_(fs["user"].value == "john")
        self.assert_(fs["data"].value == data)
        self.assert_(fs["data"].filename == "afilename")

    def test_multipart_file_request(self):
        import cgi

        # fill in a file upload form...
        form = self.make_form()
        form["user"] = "john"
        data_control = form.find_control("data")
        data = "blah\nbaz\n"
        data_control.add_file(StringIO(data), filename="filenamea")
        more_data = "rhubarb\nrhubarb\n"
        data_control.add_file(StringIO(more_data))
        yet_more_data = "rheum\nrhaponicum\n"
        data_control.add_file(StringIO(yet_more_data), filename="filenamec")
        req = form.click()
        self.assertTrue(
            get_header(req, "Content-type").startswith(
                "multipart/form-data; boundary="))

        # print "req.get_data()\n>>%s<<" % req.get_data()

        # ...and check the resulting request is understood by cgi module
        fs = cgi.FieldStorage(
            StringIO(req.get_data()),
            CaseInsensitiveDict(header_items(req)),
            environ={"REQUEST_METHOD": "POST"})
        self.assert_(fs["user"].value == "john")

        fss = fs["data"][None]
        filenames = "filenamea", "", "filenamec"
        datas = data, more_data, yet_more_data
        for i in range(len(fss)):
            fs = fss[i]
            filename = filenames[i]
            data = datas[i]
            self.assert_(fs.filename == filename)
            self.assert_(fs.value == data)

    def test_upload_data(self):
        form = self.make_form()
        data = form.click().get_data()
        self.assertTrue(data.startswith("--"))

    def test_empty_upload(self):
        # no controls except for INPUT/SUBMIT
        forms = parse_file(
            StringIO("""<html>
<form method="POST" action="./weird.html" enctype="multipart/form-data">
<input type="submit" name="submit"></input>
</form></html>"""),
            ".",
            backwards_compat=False)
        form = forms[0]
        data = form.click().get_data()
        lines = string.split(data, "\r\n")
        self.assertTrue(lines[0].startswith("--"))
        self.assertEqual(lines[1],
                         'Content-Disposition: form-data; name="submit"')
        self.assertEqual(lines[2], "")
        self.assertEqual(lines[3], "")
        self.assertTrue(lines[4].startswith("--"))

    def test_no_files(self):
        # no files uploaded
        self.monkey_patch(_form_controls, "choose_boundary", lambda: "123")
        forms = parse_file_ex(
            StringIO("""<html>
<form method="POST" action="spam" enctype="multipart/form-data">
<INPUT type="file" name="spam" />
</form></html>"""), ".")
        form = forms[1]
        data = form.click().get_data()
        self.assertEquals(data, """\
--123\r
Content-Disposition: form-data; name="spam"; filename=""\r
Content-Type: application/octet-stream\r
\r
\r
--123--\r
""")


# }}}


class MutationTests(unittest.TestCase):  # {{{
    def test_add_textfield(self):
        form = first_form('<input type="text" name="foo" value="bar" />')
        more = first_form('<input type="text" name="spam" value="eggs" />')
        combined = form.controls + more.controls
        for control in more.controls:
            control.add_to_form(form)
        self.assertEquals(form.controls, combined)


# }}}

if __name__ == "__main__":
    unittest.main()
