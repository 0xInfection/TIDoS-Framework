#!/usr/bin/env python

import sys

import mechanize

if len(sys.argv) == 1:
    uri = "http://wwwsearch.sourceforge.net/"
else:
    uri = sys.argv[1]

br = mechanize.Browser()
br.open(mechanize.urljoin(uri, "mechanize/example.html"))
forms = list(br.forms())
# f = open("example.html")
# forms = mechanize.ParseFile(f, "http://example.com/example.html",
# backwards_compat=False)
# f.close()
form = forms[0]
print form  # very useful!

# A 'control' is a graphical HTML form widget: a text entry box, a
# dropdown 'select' list, a checkbox, etc.

# Indexing allows setting and retrieval of control values
original_text = form["comments"]  # a string, NOT a Control instance
form["comments"] = "Blah."

# Controls that represent lists (checkbox, select and radio lists) are
# ListControl instances.  Their values are sequences of list item names.
# They come in two flavours: single- and multiple-selection:
form["favorite_cheese"] = ["brie"]  # single
form["cheeses"] = ["parmesan", "leicester", "cheddar"]  # multi
#  equivalent, but more flexible:
form.set_value(["parmesan", "leicester", "cheddar"], name="cheeses")

# Add files to FILE controls with .add_file().  Only call this multiple
# times if the server is expecting multiple files.
#  add a file, default value for MIME type, no filename sent to server
form.add_file(open("data.dat"))
#  add a second file, explicitly giving MIME type, and telling the server
#   what the filename is
form.add_file(open("data.txt"), "text/plain", "data.txt")

# All Controls may be disabled (equivalent of greyed-out in browser)...
control = form.find_control("comments")
print control.disabled
#  ...or readonly
print control.readonly
#  readonly and disabled attributes can be assigned to
control.disabled = False
#  convenience method, used here to make all controls writable (unless
#   they're disabled):
form.set_all_readonly(False)

# A couple of notes about list controls and HTML:

# 1. List controls correspond to either a single SELECT element, or
# multiple INPUT elements.  Items correspond to either OPTION or INPUT
# elements.  For example, this is a SELECT control, named "control1":

#    <select name="control1">
#     <option>foo</option>
#     <option value="1">bar</option>
#    </select>

# and this is a CHECKBOX control, named "control2":

#    <input type="checkbox" name="control2" value="foo" id="cbe1">
#    <input type="checkbox" name="control2" value="bar" id="cbe2">

# You know the latter is a single control because all the name attributes
# are the same.

# 2. Item names are the strings that go to make up the value that should
# be returned to the server.  These strings come from various different
# pieces of text in the HTML.  The HTML standard and the mechanize
# docstrings explain in detail, but playing around with an HTML file,
# ParseFile() and 'print form' is very useful to understand this!

# You can get the Control instances from inside the form...
control = form.find_control("cheeses", type="select")
print control.name, control.value, control.type
control.value = ["mascarpone", "curd"]
# ...and the Item instances from inside the Control
item = control.get("curd")
print item.name, item.selected, item.id, item.attrs
item.selected = False

# Controls may be referred to by label:
#  find control with label that has a *substring* "Cheeses"
#  (e.g., a label "Please select a cheese" would match).
control = form.find_control(label="select a cheese")

# You can explicitly say that you're referring to a ListControl:
#  set value of "cheeses" ListControl
form.set_value(["gouda"], name="cheeses", kind="list")
#  equivalent:
form.find_control(name="cheeses", kind="list").value = ["gouda"]
#  the first example is also almost equivalent to the following (but
#  insists that the control be a ListControl -- so it will skip any
#  non-list controls that come before the control we want)
form["cheeses"] = ["gouda"]
# The kind argument can also take values "multilist", "singlelist", "text",
# "clickable" and "file":
#  find first control that will accept text, and scribble in it
form.set_value("rhubarb rhubarb", kind="text", nr=0)
#  find, and set the value of, the first single-selection list control
form.set_value(["spam"], kind="singlelist", nr=0)

# You can find controls with a general predicate function:


def control_has_caerphilly(control):
    for item in control.items:
        if item.name == "caerphilly":
            return True


form.find_control(kind="list", predicate=control_has_caerphilly)

# HTMLForm.controls is a list of all controls in the form
for control in form.controls:
    if control.value == "inquisition":
        sys.exit()

# Control.items is a list of all Item instances in the control
for item in form.find_control("cheeses").items:
    print item.name

# To remove items from a list control, remove it from .items:
cheeses = form.find_control("cheeses")
curd = cheeses.get("curd")
del cheeses.items[cheeses.items.index(curd)]
# To add items to a list container, instantiate an Item with its control
# and attributes:
# Note that you are responsible for getting the attributes correct here,
# and these are not quite identical to the original HTML, due to
# defaulting rules and a few special attributes (e.g. Items that represent
# OPTIONs have a special "contents" key in their .attrs dict).  In future
# there will be an explicitly supported way of using the parsing logic to
# add items and controls from HTML strings without knowing these details.
mechanize.Item(cheeses, {"contents": "mascarpone",
                         "value": "mascarpone"})

# You can specify list items by label using set/get_value_by_label() and
# the label argument of the .get() method.  Sometimes labels are easier to
# maintain than names, sometimes the other way around.
form.set_value_by_label(["Mozzarella", "Caerphilly"], "cheeses")

# Which items are present, selected, and successful?
#  is the "parmesan" item of the "cheeses" control successful (selected
#   and not disabled)?
print "parmesan" in form["cheeses"]
#  is the "parmesan" item of the "cheeses" control selected?
print "parmesan" in [
    item.name for item in form.find_control("cheeses").items if item.selected]
#  does cheeses control have a "caerphilly" item?
print "caerphilly" in [
    item.name for item in form.find_control("cheeses").items]

# Sometimes one wants to set or clear individual items in a list, rather
# than setting the whole .value:
#  select the item named "gorgonzola" in the first control named "cheeses"
form.find_control("cheeses").get("gorgonzola").selected = True
# You can be more specific:
#  deselect "edam" in third CHECKBOX control
form.find_control(type="checkbox", nr=2).get("edam").selected = False
#  deselect item labelled "Mozzarella" in control with id "chz"
form.find_control(id="chz").get(label="Mozzarella").selected = False

# Often, a single checkbox (a CHECKBOX control with a single item) is
# present.  In that case, the name of the single item isn't of much
# interest, so it's a good idea to check and uncheck the box without
# using the item name:
form.find_control("smelly").items[0].selected = True  # check
form.find_control("smelly").items[0].selected = False  # uncheck

# Items may be disabled (selecting or de-selecting a disabled item is
# not allowed):
control = form.find_control("cheeses")
print control.get("emmenthal").disabled
control.get("emmenthal").disabled = True
#  enable all items in control
control.set_all_items_disabled(False)

request2 = form.click()  # mechanize.Request object
try:
    response2 = mechanize.urlopen(request2)
except mechanize.HTTPError, response2:
    pass

print response2.geturl()
# headers
for name, value in response2.info().items():
    if name != "date":
        print "%s: %s" % (name.title(), value)
print response2.read()  # body
response2.close()
