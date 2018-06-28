#!/usr/bin/env python
#
# Copyright 2001-2004 by Vinay Sajip. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Vinay Sajip
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
# VINAY SAJIP DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# VINAY SAJIP BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
# This file is part of the standalone Python logging distribution. See
# http://www.red-dove.com/python_logging.html
#
"""
A simple-minded GUI configurator for the logging module, using Tkinter.

Should work under Python versions >= 1.5.2.

Copyright (C) 2002-2004 Vinay Sajip. All Rights Reserved.

Configuration files are read/written using ConfigParser.
"""
"""

(C) 2002 Vinay Sajip. All rights reserved.
"""
from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *

import os, sys, string, types
import ConfigParser

active = None

__version__ = "0.4.1"

DEFAULT_FILENAME = "logconf.ini"

LOGGING_LEVELS = (
    ("NOTSET", "NOTSET"),
    ("DEBUG", "DEBUG"),
    ("INFO", "INFO"),
    ("WARNING", "WARNING"),
    ("ERROR", "ERROR"),
    ("CRITICAL", "CRITICAL")
)

HANDLER_TYPES = (
    ("StreamHandlerProxy", "StreamHandler"),
    ("FileHandlerProxy", "FileHandler"),
    ("RotatingFileHandlerProxy", "RotatingFileHandler"),
    ("SocketHandlerProxy", "SocketHandler"),
    ("DatagramHandlerProxy", "DatagramHandler"),
    ("SysLogHandlerProxy", "SysLogHandler"),
    ("NTEventLogHandlerProxy", "NTEventLogHandler"),
    ("SMTPHandlerProxy", "SMTPHandler"),
    ("MemoryHandlerProxy", "MemoryHandler"),
    ("HTTPHandlerProxy", "HTTPHandler"),
#    ("SOAPHandlerProxy", "SOAPHandler"),
)

OUTPUT_STREAMS = (
    ("sys.stdout", "sys.stdout"),
    ("sys.stderr", "sys.stderr")
)

FILE_MODES = (
    ("a", "a"),
    ("w", "w")
 )

HTTP_METHODS = (
    ("GET", "GET"),
    ("POST", "POST")
)

SYSLOG_FACILITIES = (
    ("LOG_AUTH", "auth"),
    ("LOG_AUTHPRIV", "authpriv"),
    ("LOG_CRON", "cron"),
    ("LOG_DAEMON", "daemon"),
    ("LOG_KERN", "kern"),
    ("LOG_LPR", "lpr"),
    ("LOG_MAIL", "mail"),
    ("LOG_NEWS", "news"),
    ("LOG_AUTH", "security"),
    ("LOG_SYSLOG", "syslog"),
    ("LOG_USER", "user"),
    ("LOG_UUCP", "uucp"),
    ("LOG_LOCAL0", "local0"),
    ("LOG_LOCAL1", "local1"),
    ("LOG_LOCAL2", "local2"),
    ("LOG_LOCAL3", "local3"),
    ("LOG_LOCAL4", "local4"),
    ("LOG_LOCAL5", "local5"),
    ("LOG_LOCAL6", "local6"),
    ("LOG_LOCAL7", "local7"),
)

LOG_TYPES = (
    ("Application", "Application"),
    ("System", "System"),
    ("Security", "Security")
)

BOOLEAN_VALUES = (
    ("0", "False"),
    ("1", "True")
)

class Property:
    def __init__(self, name, caption, value=None, choices=None):
        self.name = name
        self.caption = caption
        self.value = value
        self.choices = choices

    def getChoices(self):
        return self.choices

    def isvalid(self, s):
        return 0

    def getCaption(self):
        return self.caption

    def getValue(self):
        return self.value

    def getChoiceText(self, val):
        rv = ""
        choices = self.getChoices()
        if choices:
            for choice in choices:
                if choice[0] == val:
                    rv = choice[1]
                    break
        return rv

    def setValue(self, val):
        self.value = val

    def getValueText(self):
        if type(self.value) in [types.ListType, types.TupleType]:
            v = list(self.value)
        else:
            v = [self.value]
        choices = self.getChoices()
        if choices:
            v = map(self.getChoiceText, v)
        return string.join(v, ',')

class PropertyHolder:
    def __init__(self, dict):
        self.dict = dict
        self.propnames = []
        self.onPropListChanged = None

    def getPropNames(self):
        """
        Return the property names in the order in which they are to
        be listed.
        """
        return self.propnames

    def getProp(self, name):
        return self.dict[name]

    def isReadonly(self, name):
        return 0

    #convenience methods
    def getPropValue(self, name):
        return self.dict[name].value

    def setPropValue(self, name, value):
        self.dict[name].setValue(value)

LINE_COLOUR = '#999999'

class ScrollingList(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent)
        self.parent = parent
        self.listener = self.parent
        self.sb = Scrollbar(self, orient=VERTICAL)
        kwargs["yscrollcommand"] = self.sb.set
        self.list = apply(Listbox, (self,) + args, kwargs)
        self.sb.config(command=self.list.yview)
        self.sb.pack(side=RIGHT, fill=Y)
        self.list.pack(side=LEFT, fill=BOTH,expand=1)
        self.list.bind('<ButtonRelease-1>', self.onListChange)
        self.choices = None

    def setContents(self, choices, value):
        self.choices = choices
        self.value = value
        self.list.delete(0, END)
        if type(value) == types.ListType:
            sm = EXTENDED
        else:
            sm = BROWSE
        self.list.configure(selectmode=sm)
        i = 0
        for choice in choices:
            self.list.insert(END, choice[1])
            if sm == EXTENDED:
                if choice[0] in value:
                    self.list.select_set(i)
            else:
                if choice[0] == value:
                    self.list.select_set(i)
            i = i + 1

    def getValue(self):
        if type(self.value) == types.ListType:
            multi = 1
            rv = []
        else:
            multi = 0
        for i in xrange(len(self.choices)):
            if self.list.select_includes(i):
                if not multi:
                    rv = self.choices[i][0]
                    break
                else:
                    rv.append(self.choices[i][0])
        return rv

    def onListChange(self, event):
        self.value = self.getValue()
        self.listener.onListChange(self.value)

class PropertyHeader(Canvas):
    def __init__(self, parent, *args, **kwargs):
        self.namewidth = 120
        if kwargs.has_key("namewidth"):
            self.namewidth = kwargs["namewidth"]
            del kwargs["namewidth"]
        self.rowheight = 16
        if kwargs.has_key("rowheight"):
            self.rowheight = kwargs["rowheight"]
            del kwargs["rowheight"]
        apply(Canvas.__init__, (self, parent)+args, kwargs)
        self.bind('<Configure>', self.onConfigure)
        x = 5
        y = 0
        wid = int(self.cget('width'))
        self.create_text(x, y, text='Property', anchor='nw')
        self.create_text(x + self.namewidth, y, text='Value', anchor='nw')
        self.create_line(self.namewidth, 0, self.namewidth, self.rowheight, fill=LINE_COLOUR)
        self.tline = self.create_line(0, 0, wid, 0, fill=LINE_COLOUR)
        #self.create_line(0, 0, 0, self.rowheight, fill=LINE_COLOUR)
        #self.create_line(wid - 1, 0, wid - 1, self.rowheight, fill=LINE_COLOUR)

    def onConfigure(self, event):
        self.delete(self.tline)
        self.tline = self.create_line(0, 0, event.width, 0, fill=LINE_COLOUR)

_popup = None

class PropertyCanvas(Canvas):
    def __init__(self, parent, *args, **kwargs):
        self.namewidth = 120
        if kwargs.has_key("namewidth"):
            self.namewidth = kwargs["namewidth"]
            del kwargs["namewidth"]
        self.rowheight = 16
        if kwargs.has_key("rowheight"):
            self.rowheight = kwargs["rowheight"]
            del kwargs["rowheight"]
        apply(Canvas.__init__, (self, parent)+args, kwargs)
        self.namitems = []
        self.valitems = []
        self.lines = []
        self.pnames = []
        #Event bindings...
        self.bind('<Enter>', self.onEnter)
        self.bind('<Button-1>', self.onClick)
        self.bind('<Configure>', self.onConfigure)
        self.button = Button(height=self.rowheight, width=self.rowheight, text='...', command=self.onEdit)
        self.btnitem = None
        self.editor = Entry()
        self.edititem = None
        self.popup = Toplevel()
        self.popup.withdraw()
        self.popup.overrideredirect(1)
        self.list = ScrollingList(self.popup, background='white', relief=FLAT, borderwidth=0)
        self.list.pack(fill=BOTH, expand=1)
        self.list.listener = self
        self.listvisible = 0

    def clear(self):
        for itm in self.namitems:
            self.delete(itm)
        self.namitems = []
        for itm in self.valitems:
            self.delete(itm)
        self.valitems = []
        for lin in self.lines:
            self.delete(lin)
        self.lines = []

    def setPropertyHolder(self, ph):
        self.ph = ph
        self.pnames = ph.getPropNames()
        wid = int(self.cget('width'))
        hei = int(self.cget('height'))
        self.clear()
        x = 5
        y = 0
        i = 0
        self.props = []
        for n in self.pnames:
            prop = self.ph.getProp(n)
            self.props.append(prop)
            tn = "n%d" % i
            tv = "v%d" % i
            self.namitems.append(self.create_text(x, y + 2, text=prop.getCaption(), anchor='nw', tags=tn))
            self.valitems.append(self.create_text(x + self.namewidth, y + 2, text=prop.getValueText(), anchor='nw', tags=tv))
            y = y + self.rowheight
            i = i + 1
        self.drawLines(wid, hei)
        #self.config(height=y)

    def drawLines(self, wid, hei):
        for lin in self.lines:
            self.delete(lin)
        self.lines = []
        y = 0
        for i in xrange(len(self.pnames)):
            self.lines.append(self.create_line(0, y, wid, y, fill=LINE_COLOUR))
            y = y + self.rowheight
        self.lines.append(self.create_line(0, y, wid, y, fill=LINE_COLOUR))
        self.create_line(self.namewidth, 0, self.namewidth, hei, fill=LINE_COLOUR)

    def onEnter(self, event):
        if not self.edititem and not self.listvisible:
            self.focus_set()

    def hideControls(self):
        if self.listvisible:
            self.popup.withdraw()
            global _popup
            _popup = None
            self.listvisible = 0
        if self.edititem:
            self.ph.setPropValue(self.editprop.name, self.editor.get())
            self.itemconfig(self.valitems[self.editrow], text=self.editprop.getValueText())
            self.delete(self.edititem)
            self.edititem = None
        if self.btnitem:
            self.delete(self.btnitem)
            self.btnitem = None

    def onClick(self, event):
        row = event.y / self.rowheight
        self.hideControls()
        if row < len(self.pnames):
            wid = int(self.cget('width'))
            hei = self.rowheight
            prop = self.props[row]
            if not self.ph.isReadonly(self.pnames[row]):
                self.editrow = row
                self.editprop = prop
                choices = prop.getChoices()
                if choices != None:
                    val = prop.getValue()
                    self.list.setContents(choices, val)
                    self.listy = row * hei + self.rowheight
                    self.btnitem = self.create_window(wid - hei, row * hei, width=hei, height=hei, window=self.button, anchor='nw', tags='button')
                else:
                    self.editor.delete(0, END)
                    self.editor.insert(0, prop.getValueText())
                    self.editor.select_range(0, END)
                    self.edititem = self.create_window(self.namewidth + 1, row * hei, width=wid - self.namewidth, height = hei + 1, window=self.editor, anchor='nw', tags='editor')
                    self.editor.focus_set()

    def onConfigure(self, event):
        self.hideControls()
        self.drawLines(event.width, event.height)
        self.configure(width=event.width, height=event.height)

    def onEdit(self):
        wid = int(self.cget('width'))
        #self.listitem = self.create_window(self.namewidth + 1, self.listy, width=wid - self.namewidth - 1, height = self.rowheight * 3, window=self.list, anchor='nw', tags='list')
        w = wid - self.namewidth - 1
        h = self.rowheight * 5
        x = self.winfo_rootx() + self.namewidth + 1
        y = self.winfo_rooty() + self.listy
        s = "%dx%d+%d+%d" % (w, h, x, y)
        self.popup.deiconify()
        self.popup.lift()
        self.popup.focus_set()
        self.listvisible = 1
        self.list.focus_set()
        #For some reason with 1.5.2 (Windows), making the geometry call
        #immediately following the assignment to s doesn't work. So we
        #do it here
        self.popup.geometry(s)
        global _popup
        _popup = self.popup

    def onListChange(self, val):
        self.ph.setPropValue(self.editprop.name, val)
        self.itemconfig(self.valitems[self.editrow], text=self.editprop.getValueText())
        if type(val) != types.ListType:
            self.hideControls()

class PropertyEditor(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent)
        self.parent = parent
        nw = kwargs.get("namewidth", 120)
        rh = kwargs.get("rowheight", 16)
        wid = kwargs.get("width", 300)
        hei = kwargs.get("height", 60)
        self.header = PropertyHeader(self, namewidth=nw, rowheight=rh, height=14, highlightthickness=0)
        self.body = PropertyCanvas(self, namewidth=nw, rowheight=rh, width=wid, height=hei, background='white', highlightthickness=0)
        self.header.pack(side=TOP, fill=X)
        self.body.pack(side=BOTTOM, fill=BOTH, expand=1)

    def setPropertyHolder(self, ph):
        self.body.setPropertyHolder(ph)

class ADUPanel(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.add = Button(self, text="New", command=parent.onAdd)
        self.add.pack(side=LEFT) #, fill=X, expand=1)
        self.rmv = Button(self, text="Delete", command=parent.onDelete)
        self.rmv.pack(side=LEFT) #, fill=X, expand=1)
        #self.upd = Button(self, text="Update", command=parent.onUpdate)
        #self.upd.pack(side=RIGHT, fill=X, expand=1)

class ScrollList(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent)
        self.parent = parent
        self.sb = Scrollbar(self, orient=VERTICAL)
        kwargs["yscrollcommand"] = self.sb.set
        self.list = apply(Listbox, (self,) + args, kwargs)
        self.sb.config(command=self.list.yview)
        self.sb.pack(side=RIGHT, fill=Y)
        self.list.pack(side=LEFT, fill=BOTH,expand=1)

def sortqn(log1, log2):
    qn1 = log1.getQualifiedName()
    qn2 = log2.getQualifiedName()
    if qn1 == "(root)":
        rv = -1
    elif qn2 == "(root)":
        rv = 1
    else:
        rv = cmp(qn1, qn2)
    return rv

def sortn(obj1, obj2):
    return cmp(obj1.getPropValue("name"), obj2.getPropValue("name"))

class LoggerPanel(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        label = Label(self, text="Loggers:")
        label.grid(row=0, column=0, sticky='w')
        self.slist = ScrollList(self, height=15, background='white')
        self.slist.list.bind('<ButtonRelease-1>', self.onListChange)
        self.slist.grid(row=1, column=0, sticky="nsew")
        self.adu = ADUPanel(self)
        self.adu.grid(row=2, column=0, sticky="we")
        label = Label(self, text="Properties of selected logger:")
        label.grid(row=3, column=0, sticky='w')
        self.pe = PropertyEditor(self, height=120, borderwidth=1)
        self.pe.grid(row=4, column=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(4, weight=1)

    def setConfig(self, config):
        self.config = config
        #populate list of loggers
        llist = config.getLoggers()
        llist.sort(sortqn)
        self.slist.list.delete(0, END)
        self.pe.body.clear()
        self.names = []
        for logger in llist:
            self.names.append(logger.getPropValue("name"))
            self.slist.list.insert(END, logger.getQualifiedName())

    def onAdd(self):
        items = self.slist.list.curselection()
        if not len(items):
            showerror("No Parent Selected", "You haven't selected a parent logger.")
        else:
            idx = int(items[0])
            parent = self.config.getLogger(self.names[idx])
            log = self.config.getLogger(None)
            log.onChannelChanged = self.onChannelChanged
            log.setPropValue("parent", parent.getPropValue("name"))
            self.names.insert(1 + idx, log.getPropValue("name"))
            self.slist.list.insert(1 + idx, log.getQualifiedName())
            self.slist.list.select_clear(0, END)
            self.slist.list.select_set(1 + idx)
            self.pe.setPropertyHolder(log)

    def onDelete(self):
        items = self.slist.list.curselection()
        if not len(items):
            showerror("No Item Selected", "You haven't selected anything to delete.")
        else:
            idx = int(items[0])
            name = self.slist.list.get(idx)
            if name == "(root)":
                showerror("Root Item Selected", "You cannot delete the root logger.")
            else:
                resp = askyesno("Logger Deletion", "Are you sure you want to delete logger '%s'?" % name)
                if resp:
                    #self.config.removeLogger(self.names[idx])
                    log = self.config.getLogger(self.names[idx])
                    log.deleted = 1
                    self.slist.list.delete(idx)
                    del self.names[idx]
                    self.pe.body.clear()

    def onChannelChanged(self, nm, chname):
        i = self.names.index(nm)
        sel = i
        while i < len(self.names):
            log = self.config.getLogger(self.names[i])
            self.slist.list.delete(i)
            self.slist.list.insert(i, log.getQualifiedName())
            i = i + 1
        self.slist.list.select_clear(0, END)
        self.slist.list.select_set(sel)

    def onListChange(self, event):
        self.pe.body.hideControls()
        items = self.slist.list.curselection()
        idx = int(items[0])
        name = self.names[idx]
        log = self.config.getLogger(name)
        self.pe.setPropertyHolder(log)

class HandlerPanel(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        label = Label(self, text="Handlers:")
        label.grid(row=0, column=0, sticky='w')
        self.slist = ScrollList(self, height=6, background='white')
        self.slist.list.bind('<ButtonRelease-1>', self.onListChange)
        self.slist.grid(row=1, column=0, sticky="nsew")
        self.adu = ADUPanel(self)
        self.adu.grid(row=2, column=0, sticky="we")
        label = Label(self, text="Properties of selected handler:")
        label.grid(row=3, column=0, sticky='w')
        self.pe = PropertyEditor(self, height=90, borderwidth=1)
        self.pe.grid(row=4, column=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)

    def setConfig(self, config):
        self.config = config
        #populate list of handlers
        hlist = config.getHandlers()
        hlist.sort(sortn)
        self.slist.list.delete(0, END)
        self.pe.body.clear()
        for hand in hlist:
            hand.onPropListChanged = self.onPropListChanged
            self.slist.list.insert(END, hand.getPropValue("name"))

    def onAdd(self):
        self.pe.body.hideControls()
        hand = self.config.getHandler(None)
        self.slist.list.insert(END, hand.getProp("name").getValueText())
        self.slist.list.select_clear(0, END)
        self.slist.list.select_set(END)
        hand.onPropListChanged = self.onPropListChanged
        self.pe.setPropertyHolder(hand)

    def onDelete(self):
        items = self.slist.list.curselection()
        if not len(items):
            showerror("No Item Selected", "You haven't selected anything to delete")
        else:
            name = self.slist.list.get(int(items[0]))
            log = self.config.handlerIsUsed(name)
            if log:
                showerror("Handler in use",
                          "The handler '%s' is being used by logger '%s'"\
                          ", so it cannot be deleted." % (
                          name, log))
            else:
                self.config.removeHandler(name)
                self.slist.list.delete(items)
                self.pe.body.clear()

    def onUpdate(self):
        print "handler update"

    def onListChange(self, event):
        self.pe.body.hideControls()
        items = self.slist.list.curselection()
        name = self.slist.list.get(int(items[0]))
        hand = self.config.getHandler(name)
        self.pe.setPropertyHolder(hand)

    def onPropListChanged(self, newhand):
        newhand.onPropListChanged = self.onPropListChanged
        self.pe.setPropertyHolder(newhand)

class FormatterPanel(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        label = Label(self, text="Formatters:")
        label.grid(row=0, column=0, sticky='w')
        self.slist = ScrollList(self, height=4, background='white')
        self.slist.list.bind('<ButtonRelease-1>', self.onListChange)
        self.slist.grid(row=1, column=0, sticky="nsew")
        self.adu = ADUPanel(self)
        self.adu.grid(row=2, column=0, sticky="ew")
        label = Label(self, text="Properties of selected formatter:")
        label.grid(row=3, column=0, sticky='w')
        self.pe = PropertyEditor(self, height=60, borderwidth=1)
        self.pe.grid(row=4, column=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)

    def setConfig(self, config):
        self.config = config
        #populate list of formatters
        flist = config.getFormatters()
        flist.sort(sortn)
        self.slist.list.delete(0, END)
        self.pe.body.clear()
        for form in flist:
            self.slist.list.insert(END, form.getPropValue("name"))

    def onAdd(self):
        self.pe.body.hideControls()
        fmt = self.config.getFormatter(None)
        self.slist.list.insert(END, fmt.getProp("name").getValueText())
        self.slist.list.select_clear(0, END)
        i = self.slist.list.size()
        self.slist.list.select_set(i - 1)
        self.pe.setPropertyHolder(fmt)

    def onDelete(self):
        self.pe.body.hideControls()
        items = self.slist.list.curselection()
        if not len(items):
            showerror("No Item Selected", "You haven't selected anything to delete")
        else:
            name = self.slist.list.get(int(items[0]))
            h = self.config.formatterIsUsed(name)
            if h:
                showerror("Formatter in use",
                          "The formatter '%s' is being used by handler '%s'"\
                          ", so it cannot be deleted." % (
                          name, h))
            else:
                self.config.removeFormatter(name)
                self.slist.list.delete(items)
                self.pe.body.clear()

    def onUpdate(self):
        self.pe.body.hideControls()

    def onListChange(self, event):
        self.pe.body.hideControls()
        items = self.slist.list.curselection()
        name = self.slist.list.get(int(items[0]))
        fmt = self.config.getFormatter(name)
        self.pe.setPropertyHolder(fmt)

class FilterPanel(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        label = Label(self, text="Filters:")
        label.grid(row=0, column=0, sticky='w')
        self.slist = ScrollList(self, height=4, background='white')
        self.slist.list.bind('<ButtonRelease-1>', self.onListChange)
        self.slist.grid(row=1, column=0, sticky="nsew")
        self.adu = ADUPanel(self)
        self.adu.grid(row=2, column=0, sticky="ew")
        label = Label(self, text="Properties of selected filter:")
        label.grid(row=3, column=0, sticky='w')
        self.pe = PropertyEditor(self, height=60, borderwidth=1)
        self.pe.grid(row=4, column=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)

    def setConfig(self, config):
        self.config = config
        #populate list of filters
        flist = config.getFilters()
        flist.sort(sortn)
        self.slist.list.delete(0, END)
        self.pe.body.clear()
        for filt in flist:
            self.slist.list.insert(END, filt.getPropValue("name"))

    def onAdd(self):
        self.pe.body.hideControls()
        filt = self.config.getFilter(None)
        self.slist.list.insert(END, filt.getProp("name").getValueText())
        self.slist.list.select_clear(0, END)
        i = self.slist.list.size()
        self.slist.list.select_set(i - 1)
        self.pe.setPropertyHolder(filt)

    def onDelete(self):
        self.pe.body.hideControls()
        items = self.slist.list.curselection()
        if not len(items):
            showerror("No Item Selected", "You haven't selected anything to delete")
        else:
            name = self.slist.list.get(int(items[0]))
            h = self.config.filterIsUsed(name)
            if h:
                showerror("Filter in use",
                          "The filter '%s' is being used by '%s'"\
                          ", so it cannot be deleted." % (
                          name, h))
            else:
                self.config.removeFilter(name)
                self.slist.list.delete(items)
                self.pe.body.clear()

    def onUpdate(self):
        self.pe.body.hideControls()

    def onListChange(self, event):
        self.pe.body.hideControls()
        items = self.slist.list.curselection()
        name = self.slist.list.get(int(items[0]))
        filt = self.config.getFilter(name)
        self.pe.setPropertyHolder(filt)

class ConfigPanel(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.load = Button(self, text="Load...", command=parent.onLoad)
        self.load.pack(side=LEFT)
        self.save = Button(self, text="Save", command=parent.onSave)
        self.save.pack(side=LEFT)
        self.save = Button(self, text="Save as...", command=parent.onSaveAs)
        self.save.pack(side=LEFT)
        self.reset = Button(self, text="Reset", command=parent.onReset)
        self.reset.pack(side=RIGHT)

class Configurator(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.llist = LoggerPanel(self)
        self.llist.grid(row=0, column=0, rowspan=2, sticky='nsew')
        spacer = Canvas(self, width=2, highlightthickness=0)
        spacer.grid(row=0, column=1, rowspan=2, sticky='ns')
        self.hlist = HandlerPanel(self)
        self.hlist.grid(row=0, column=2, sticky='nsew')
        self.flist = FormatterPanel(self)
        self.flist.grid(row=1, column=2, sticky='nsew')
        self.cfg = ConfigPanel(self)
        self.cfg.grid(row=2, column=0, columnspan=2, sticky='w')
        self.filename = None

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        label = Label(self, text="Copyright (C) 2002 Vinay Sajip. All rights reserved.", foreground='brown')
        label.grid(row=3, column=0, columnspan=2, sticky='w')

        if len(sys.argv) > 1:
            fn = sys.argv[1]
            try:
                self.loadFile(fn)
            except Exception, e:
                print e
                raise
        else:
            self.onReset(0)
        self.setTitle()
        self.focus_set()

    def setTitle(self):
        if self.filename:
            s = os.path.split(self.filename)[1]
        else:
            s = "untitled"
        self.winfo_toplevel().title("%s - Python Logging Configurator V%s" % (s, __version__))

    def loadFile(self, fn):
        self.config = LoggingConfig()
        self.config.read(fn)
        self.filename = fn
        self.llist.setConfig(self.config)
        self.hlist.setConfig(self.config)
        self.flist.setConfig(self.config)
        self.setTitle()

    def onLoad(self):
        fn = askopenfilename(title="Choose configuration file", filetypes=[("Logging configurations", "*.ini"), ("All files", "*.*")])
        if fn:
            self.loadFile(fn)

    def onSaveAs(self):
        if self.filename:
            fn = os.path.split(self.filename)[1]
        else:
            fn = DEFAULT_FILENAME
        fn = asksaveasfilename(title="Save configuration as", initialfile=fn, filetypes=[("Logging configurations", "*.ini"), ("All files", "*.*")])
        if fn:
            self.config.save(fn)
            self.filename = fn
            self.setTitle()

    def onSave(self):
        if not self.filename:
            self.onSaveAs()
        else:
            self.config.save(self.filename)

    def onReset(self, confirm=1):
        if not confirm:
            doit = 1
        else:
            doit = askyesno("Reset", "Are you sure you want to reset?")
        if doit:
            self.config = LoggingConfig()
            self.llist.setConfig(self.config)
            self.hlist.setConfig(self.config)
            self.flist.setConfig(self.config)
            self.setTitle()

# -- general properties

class NameProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "name", "Name", value)

class LevelProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "level", "Level", value)

    def getChoices(self):
        return LOGGING_LEVELS

# -- formatter properties

class FormatProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "format", "Format", value)

class DateFormatProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "datefmt", "Date Format", value)

class FormatterProxy(PropertyHolder):
    def __init__(self, config, dict):
        self.config = config
        PropertyHolder.__init__(self, dict)
        prop = NameProperty(dict.get("name", ""))
        self.dict["name"] = prop
        prop = FormatProperty(dict.get("format", "%(asctime)s %(levelname)s %(message)s"))
        self.dict["format"] = prop
        prop = DateFormatProperty(dict.get("datefmt", ""))
        self.dict["datefmt"] = prop
        self.propnames = ["name", "format", "datefmt"]

    def isReadonly(self, name):
        return name == "name"

    def writeConfig(self, file):
        file.write("[formatter_%s]\n" % self.getPropValue("name"))
        file.write("format=%s\n" % self.getPropValue("format"))
        file.write("datefmt=%s\n\n" % self.getPropValue("datefmt"))

# -- filter properties

class LoggerNameProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "lname", "Name", value)

class FilterProxy(PropertyHolder):
    def __init__(self, config, dict):
        self.config = config
        PropertyHolder.__init__(self, dict)
        prop = NameProperty(dict.get("name", ""))
        self.dict["name"] = prop
        prop = LoggerNameProperty(dict.get("lname", ""))
        self.dict["lname"] = prop
        self.propnames = ["name", "lname"]

    def isReadonly(self, name):
        return name == "name"

    def writeConfig(self, file):
        file.write("[filter_%s]\n" % self.getPropValue("name"))
        file.write("lname=%s\n" % self.getPropValue("lname"))

# -- handler properties and proxies

class HandlerTypeProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "class", "Type", value)

    def getChoices(self):
        return HANDLER_TYPES

class FormatterProperty(Property):
    def __init__(self, config, value=None):
        self.config = config
        Property.__init__(self, "formatter", "Formatter", value)

    def getChoices(self):
        return self.config.getFormatterChoice()

class HandlerProxy(PropertyHolder):
    def __init__(self, config, dict):
        self.config = config
        PropertyHolder.__init__(self, dict)
        prop = NameProperty(dict.get("name", ""))
        self.dict["name"] = prop
        prop = HandlerTypeProperty(dict.get("class", "StreamHandlerProxy"))
        self.dict["class"] = prop
        prop = FormatterProperty(self.config, dict.get("formatter", ""))
        self.dict["formatter"] = prop
        prop = LevelProperty(dict.get("level", "NOTSET"))
        self.dict["level"] = prop
        self.propnames = ["name", "class", "level", "formatter"]

    def isReadonly(self, name):
        return (name == "name")

    def setPropValue(self, name, value):
        PropertyHolder.setPropValue(self, name, value)
        if (name == "class"):   #morph type of handler
            #print "try morph -> %s" % value
            try:
                klass = eval(value)
            except Exception, e:
                print e
                klass = None
            if klass:
                n = self.getPropValue("name")
                d = {
                        "name": n,
                        "class": value,
                        "formatter": self.getPropValue("formatter"),
                        "level": self.getPropValue("level"),
                        }
                newhand = klass(self.config, d)
                self.config.handlers[n] = newhand   #FIXME encapsulation
                if self.onPropListChanged:
                    self.onPropListChanged(newhand)

    def writeConfig(self, file):
        file.write("[handler_%s]\n" % self.getPropValue("name"))
        s = self.getProp("class").getValueText()
        if not s in ["StreamHandler", "FileHandler"]:
            s = "handlers." + s
        file.write("class=%s\n" % s)
        file.write("level=%s\n" % self.getPropValue("level"))
        file.write("formatter=%s\n" % self.getPropValue("formatter"))

class StreamProperty(Property):
    def __init__(self, config, value=None):
        self.config = config
        Property.__init__(self, "stream", "Stream", value)

    def getChoices(self):
        return OUTPUT_STREAMS

class StreamHandlerProxy(HandlerProxy):
    def __init__(self, config, dict):
        HandlerProxy.__init__(self, config, dict)
        prop = StreamProperty(self.config, dict.get("stream", "sys.stderr"))
        self.dict["stream"] = prop
        self.propnames.append("stream")

    def writeConfig(self, file):
        HandlerProxy.writeConfig(self, file)
        file.write("stream=%s\n" % self.getPropValue("stream"))
        file.write("args=(%s,)\n\n" % self.getPropValue("stream"))

    def readConfig(self, sectname):
        prop = StreamProperty(self.config, self.config.get(sectname, "stream"))
        self.dict["stream"] = prop
        self.propnames.append("stream")

class FilenameProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "filename", "File name", value)

class ModeProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "mode", "Mode", value)

    def getChoices(self):
        return FILE_MODES

class MaxSizeProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "maxsize", "Maximum Size (bytes)", value)

class BackupCountProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "backcount", "Backup Count", value)

class FileHandlerProxy(HandlerProxy):
    def __init__(self, config, dict):
        HandlerProxy.__init__(self, config, dict)
        prop = FilenameProperty(dict.get("filename", "python.log"))
        self.dict["filename"] = prop
        prop = ModeProperty(dict.get("mode", "a"))
        self.dict["mode"] = prop
        self.propnames.extend(["filename", "mode"])

    def writeConfig(self, file):
        HandlerProxy.writeConfig(self, file)
        fn = self.getPropValue("filename")
        file.write("filename=%s\n" % fn)
        mode = self.getPropValue("mode")
        file.write("mode=%s\n" % mode)
        file.write("args=('%s', '%s')\n\n" % (fn, mode))

    def readConfig(self, sectname):
        prop = FilenameProperty(self.config.get(sectname, "filename"))
        self.dict["filename"] = prop
        prop = ModeProperty(self.config.get(sectname, "mode"))
        self.dict["mode"] = prop
        self.propnames.extend(["filename", "mode"])

class RotatingFileHandlerProxy(FileHandlerProxy):
    def __init__(self, config, dict):
        FileHandlerProxy.__init__(self, config, dict)
        prop = MaxSizeProperty(dict.get("maxsize", "0"))
        self.dict["maxsize"] = prop
        prop = BackupCountProperty(dict.get("backcount", "1"))
        self.dict["backcount"] = prop
        self.propnames.extend(["maxsize", "backcount"])

    def writeConfig(self, file):
        HandlerProxy.writeConfig(self, file)
        fn = self.getPropValue("filename")
        file.write("filename=%s\n" % fn)
        mode = self.getPropValue("mode")
        file.write("mode=%s\n" % mode)
        ms = self.getPropValue("maxsize")
        file.write("maxsize=%s\n" % ms)
        bc = self.getPropValue("backcount")
        file.write("backcount=%s\n" % bc)
        file.write("args=('%s', '%s', %s, %s)\n\n" % (fn, mode, ms, bc))

    def readConfig(self, sectname):
        FileHandlerProxy.readConfig(self, sectname)
        prop = MaxSizeProperty(self.config.get(sectname, "maxsize"))
        self.dict["maxsize"] = prop
        prop = BackupCountProperty(self.config.get(sectname, "backcount"))
        self.dict["backcount"] = prop
        self.propnames.extend(["maxsize", "backcount"])


class HostProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "host", "Host", value)

class PortProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "port", "Port", value)

class SocketHandlerProxy(HandlerProxy):
    def __init__(self, config, dict):
        HandlerProxy.__init__(self, config, dict)
        prop = HostProperty(dict.get("host", "localhost"))
        self.dict["host"] = prop
        prop = PortProperty(dict.get("port", "handlers.DEFAULT_TCP_LOGGING_PORT"))
        self.dict["port"] = prop
        self.propnames.extend(["host", "port"])

    def writeConfig(self, file):
        HandlerProxy.writeConfig(self, file)
        host = self.getPropValue("host")
        file.write("host=%s\n" % host)
        port = self.getPropValue("port")
        file.write("port=%s\n" % port)
        file.write("args=('%s', %s)\n\n" % (host, port))

    def readConfig(self, sectname):
        prop = HostProperty(self.config.get(sectname, "host"))
        self.dict["host"] = prop
        prop = PortProperty(self.config.get(sectname, "port"))
        self.dict["port"] = prop
        self.propnames.extend(["host", "port"])

class DatagramHandlerProxy(HandlerProxy):
    def __init__(self, config, dict):
        HandlerProxy.__init__(self, config, dict)
        prop = HostProperty(dict.get("host", "localhost"))
        self.dict["host"] = prop
        prop = PortProperty(dict.get("port", "handlers.DEFAULT_UDP_LOGGING_PORT"))
        self.dict["port"] = prop
        self.propnames.extend(["host", "port"])

    def writeConfig(self, file):
        HandlerProxy.writeConfig(self, file)
        host = self.getPropValue("host")
        file.write("host=%s\n" % host)
        port = self.getPropValue("port")
        file.write("port=%s\n" % port)
        file.write("args=('%s', %s)\n\n" % (host, port))

    def readConfig(self, sectname):
        prop = HostProperty(self.config.get(sectname, "host"))
        self.dict["host"] = prop
        prop = PortProperty(self.config.get(sectname, "port"))
        self.dict["port"] = prop
        self.propnames.extend(["host", "port"])

class URLProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "url", "URL", value)

class MethodProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "method", "HTTP Method", value)

    def getChoices(self):
        return HTTP_METHODS

class HTTPHandlerProxy(HandlerProxy):
    def __init__(self, config, dict):
        HandlerProxy.__init__(self, config, dict)
        prop = HostProperty(dict.get("host", "localhost"))
        self.dict["host"] = prop
        prop = PortProperty(dict.get("port", "80"))
        self.dict["port"] = prop
        prop = URLProperty(dict.get("url", ""))
        self.dict["url"] = prop
        prop = MethodProperty(dict.get("method", "GET"))
        self.dict["method"] = prop
        self.propnames.extend(["host", "port", "url", "method"])

    def writeConfig(self, file):
        HandlerProxy.writeConfig(self, file)
        host = self.getPropValue("host")
        file.write("host=%s\n" % host)
        port = self.getPropValue("port")
        file.write("port=%s\n" % port)
        url = self.getPropValue("url")
        file.write("url=%s\n" % url)
        meth = self.getPropValue("method")
        file.write("method=%s\n" % meth)
        file.write("args=('%s:%s', '%s', '%s')\n\n" % (host, port, url, meth))

    def readConfig(self, sectname):
        prop = HostProperty(self.config.get(sectname, "host"))
        self.dict["host"] = prop
        prop = PortProperty(self.config.get(sectname, "port"))
        self.dict["port"] = prop
        prop = URLProperty(self.config.get(sectname, "url"))
        self.dict["url"] = prop
        prop = MethodProperty(self.config.get(sectname, "method"))
        self.dict["method"] = prop
        self.propnames.extend(["host", "port", "url", "method"])

class SOAPHandlerProxy(HandlerProxy):
    def __init__(self, config, dict):
        HandlerProxy.__init__(self, config, dict)
        prop = HostProperty(dict.get("host", "localhost"))
        self.dict["host"] = prop
        prop = PortProperty(dict.get("port", "80"))
        self.dict["port"] = prop
        prop = URLProperty(dict.get("url", ""))
        self.dict["url"] = prop
        self.propnames.extend(["host", "port", "url"])

    def writeConfig(self, file):
        HandlerProxy.writeConfig(self, file)
        host = self.getPropValue("host")
        file.write("host=%s\n" % host)
        port = self.getPropValue("port")
        file.write("port=%s\n" % port)
        url = self.getPropValue("url")
        file.write("url=%s\n" % url)
        file.write("args=('%s:%s', '%s')\n\n" % (host, port, url))

    def readConfig(self, sectname):
        prop = HostProperty(self.config.get(sectname, "host"))
        self.dict["host"] = prop
        prop = PortProperty(self.config.get(sectname, "port"))
        self.dict["port"] = prop
        prop = URLProperty(self.config.get(sectname, "url"))
        self.dict["url"] = prop
        self.propnames.extend(["host", "port", "url"])

class FacilityProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "facility", "Facility", value)

    def getChoices(self):
        return SYSLOG_FACILITIES

class SysLogHandlerProxy(HandlerProxy):
    def __init__(self, config, dict):
        HandlerProxy.__init__(self, config, dict)
        prop = HostProperty(dict.get("host", "localhost"))
        self.dict["host"] = prop
        prop = PortProperty(dict.get("port", "handlers.SYSLOG_UDP_PORT"))
        self.dict["port"] = prop
        prop = FacilityProperty(dict.get("facility", "handlers.SysLogHandler.LOG_USER"))
        self.dict["facility"] = prop
        self.propnames.extend(["host", "port", "facility"])

    def writeConfig(self, file):
        HandlerProxy.writeConfig(self, file)
        host = self.getPropValue("host")
        file.write("host=%s\n" % host)
        port = self.getPropValue("port")
        file.write("port=%s\n" % port)
        fac = self.getPropValue("facility")
        file.write("facility=%s\n" % fac)
        file.write("args=(('%s', %s), handlers.SysLogHandler.%s)\n\n" % (host, port, fac))

    def readConfig(self, sectname):
        prop = HostProperty(self.config.get(sectname, "host"))
        self.dict["host"] = prop
        prop = PortProperty(self.config.get(sectname, "port"))
        self.dict["port"] = prop
        prop = FacilityProperty(self.config.get(sectname, "facility"))
        self.dict["facility"] = prop
        self.propnames.extend(["host", "port", "facility"])

class FromProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "from", "From", value)

class ToProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "to", "To", value)

class SubjectProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "subject", "Subject", value)

class SMTPHandlerProxy(HandlerProxy):
    def __init__(self, config, dict):
        HandlerProxy.__init__(self, config, dict)
        prop = HostProperty(dict.get("host", "localhost"))
        self.dict["host"] = prop
        prop = PortProperty(dict.get("port", "25"))
        self.dict["port"] = prop
        prop = FromProperty(dict.get("from", ""))
        self.dict["from"] = prop
        prop = ToProperty(dict.get("to", ""))
        self.dict["to"] = prop
        prop = SubjectProperty(dict.get("subject", ""))
        self.dict["subject"] = prop
        self.propnames.extend(["host", "port", "from", "to", "subject"])

    def writeConfig(self, file):
        HandlerProxy.writeConfig(self, file)
        host = self.getPropValue("host")
        file.write("host=%s\n" % host)
        port = self.getPropValue("port")
        file.write("port=%s\n" % port)
        frm = self.getPropValue("from")
        file.write("from=%s\n" % frm)
        to = self.getPropValue("to")
        file.write("to=%s\n" % to)
        subj = self.getPropValue("subject")
        file.write("subject=%s\n" % subj)
        to = string.split(to, ",")
        file.write("args=('%s', '%s', %s, '%s')\n\n" % (host, frm, repr(to), subj))

    def readConfig(self, sectname):
        prop = HostProperty(self.config.get(sectname, "host"))
        self.dict["host"] = prop
        prop = PortProperty(self.config.get(sectname, "port"))
        self.dict["port"] = prop
        prop = FromProperty(self.config.get(sectname, "from"))
        self.dict["from"] = prop
        prop = ToProperty(self.config.get(sectname, "to"))
        self.dict["to"] = prop
        prop = SubjectProperty(self.config.get(sectname, "subject"))
        self.dict["subject"] = prop
        self.propnames.extend(["host", "port", "from", "to", "subject"])

class CapacityProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "capacity", "Capacity", value)

class FlushLevelProperty(LevelProperty):
    def __init__(self, value=None):
        Property.__init__(self, "flushlevel", "Flush Level", value)

class TargetProperty(Property):
    def __init__(self, config, value=None):
        self.config = config
        Property.__init__(self, "target", "Target", value)

    def getChoices(self):
        handlers = self.config.getHandlerChoice()
        nm = self.dict["name"].getValueText()
        #can't be own target...
        return filter(lambda x,nm=nm: x[0] != nm, handlers)

class MemoryHandlerProxy(HandlerProxy):
    def __init__(self, config, dict):
        HandlerProxy.__init__(self, config, dict)
        prop = CapacityProperty(dict.get("capacity", "10"))
        self.dict["capacity"] = prop
        prop = FlushLevelProperty(dict.get("flushlevel", "ERROR"))
        self.dict["flushlevel"] = prop
        prop = TargetProperty(config, dict.get("target", ""))
        prop.dict = self.dict
        self.dict["target"] = prop
        self.propnames.extend(["capacity", "flushlevel", "target"])

    def writeConfig(self, file):
        HandlerProxy.writeConfig(self, file)
        cap = self.getPropValue("capacity")
        file.write("capacity=%s\n" % cap)
        flvl = self.getPropValue("flushlevel")
        file.write("flushlevel=%s\n" % flvl)
        file.write("target=%s\n" % self.getPropValue("target"))
        file.write("args=(%s, %s)\n\n" % (cap, flvl))

    def readConfig(self, sectname):
        prop = CapacityProperty(self.config.get(sectname, "capacity"))
        self.dict["capacity"] = prop
        prop = FlushLevelProperty(self.config.get(sectname, "flushlevel"))
        self.dict["flushlevel"] = prop
        prop = TargetProperty(self.config, self.config.get(sectname, "target"))
        prop.dict = self.dict
        self.dict["target"] = prop
        self.propnames.extend(["capacity", "flushlevel", "target"])

class AppNameProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "appname", "Application Name", value)

class DLLNameProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "dllname", "Message DLL name", value)

class LogTypeProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "logtype", "Log Type", value)

    def getChoices(self):
        return LOG_TYPES

class NTEventLogHandlerProxy(HandlerProxy):
    def __init__(self, config, dict):
        HandlerProxy.__init__(self, config, dict)
        prop = AppNameProperty(dict.get("appname", "Python Application"))
        self.dict["appname"] = prop
        prop = DLLNameProperty(dict.get("dllname", ""))
        self.dict["dllname"] = prop
        prop = LogTypeProperty(dict.get("logtype", "Application"))
        self.dict["logtype"] = prop
        self.propnames.extend(["appname", "dllname", "logtype"])

    def writeConfig(self, file):
        HandlerProxy.writeConfig(self, file)
        app = self.getPropValue("appname")
        file.write("appname=%s\n" % app)
        dll = self.getPropValue("dllname")
        file.write("dllname=%s\n" % dll)
        ltype = self.getPropValue("logtype")
        file.write("logtype=%s\n" % ltype)
        file.write("args=('%s', '%s', '%s')\n\n" % (app, dll, ltype))

    def readConfig(self, sectname):
        prop = AppNameProperty(self.config.get(sectname, "appname"))
        self.dict["appname"] = prop
        prop = DLLNameProperty(self.config.get(sectname, "dllname"))
        self.dict["dllname"] = prop
        prop = LogTypeProperty(self.config.get(sectname, "logtype"))
        self.dict["logtype"] = prop
        self.propnames.extend(["appname", "dllname", "logtype"])

# -- logger properties and proxies

class ChannelProperty(Property):
    def __init__(self, value=None):
        Property.__init__(self, "channel", "Name", value)

class HandlerProperty(Property):
    def __init__(self, config, value=None):
        self.config = config
        Property.__init__(self, "handler", "Handlers", value)

    def getChoices(self):
        return self.config.getHandlerChoice()

class FilterProperty(Property):
    def __init__(self, config, value=None):
        self.config = config
        Property.__init__(self, "filter", "Filters", value)

    def getChoices(self):
        return self.config.getFilterChoice()

class ParentProperty(Property):
    def __init__(self, config, value=None):
        self.config = config
        Property.__init__(self, "parent", "Parent", value)

    def getChoices(self):
        loggers = self.config.getLoggerChoice()
        nm = self.dict["name"].getValueText()
        #can't be own parent...
        return filter(lambda x,nm=nm: x[0] != nm, loggers)

    def getValueText(self):
        if self.dict.has_key("root"):
            return ""
        pn = Property.getValueText(self)
        rv = ""
        while pn != "(root)":
            parent = self.config.getLogger(pn)
            rv = parent.getPropValue("channel") + "." + rv
            pn = parent.getProp("parent").value
        return rv[:-1]

class PropagateProperty(Property):
    def __init__(self, config, value=None):
        self.config = config
        Property.__init__(self, "propagate", "Propagate", value)

    def getChoices(self):
        return BOOLEAN_VALUES

class LoggerProxy(PropertyHolder):
    def __init__(self, config, dict):
        self.config = config
        PropertyHolder.__init__(self, dict)
        prop = ChannelProperty(dict.get("channel", ""))
        self.dict["channel"] = prop
        prop = NameProperty(dict.get("name", ""))
        self.dict["name"] = prop
        prop = HandlerProperty(config, dict.get("handler", []))
        self.dict["handler"] = prop
        prop = LevelProperty(dict.get("level", "NOTSET"))
        self.dict["level"] = prop
        prop = PropagateProperty(self.config, dict.get("propagate", "1"))
        self.dict["propagate"] = prop
        prop = ParentProperty(config, dict.get("parent", "(root)"))
        prop.dict = self.dict
        self.dict["parent"] = prop
        self.propnames = ["parent", "channel", "level", "propagate", "handler"]
        self.onChannelChanged = None
        self.deleted = 0

    def isReadonly(self, name):
        return (name in ["channel", "parent", "propagate"]) and self.dict.has_key("root")

    def getQualifiedName(self):
        pt = self.getProp("parent").getValueText()
        nm = self.getPropValue("channel")
        if pt:
            pn =  pt + "." + nm
        else:
            pn = nm
            if pn == "":
                pn = "(root)"
        return pn

    def setPropValue(self, name, value):
        PropertyHolder.setPropValue(self, name, value)
        if (name == "channel"):
            nm = self.getPropValue("name")
            if self.onChannelChanged:
                self.onChannelChanged(nm, value)

    def writeConfig(self, file):
        if self.dict.has_key("root"):
            name = "root"
        else:
            name = self.getPropValue("name")
        file.write("[logger_%s]\n" % name)
        file.write("level=%s\n" % self.getPropValue("level"))
        file.write("propagate=%s\n" % self.getPropValue("propagate"))
        file.write("channel=%s\n" % self.getPropValue("channel"))
        file.write("parent=%s\n" % self.getPropValue("parent"))
        file.write("qualname=%s\n" % self.getQualifiedName())
        file.write("handlers=%s\n\n" %  string.join(self.getPropValue("handler"), ","))

# -- logging configuration

class LoggingConfig(ConfigParser.ConfigParser):
    def __init__(self, defaults=None):
        ConfigParser.ConfigParser.__init__(self, defaults)
        self.formatters = {}
        self.handlers = {}
        self.loggers = {}
#        self.filters = {}
        #create root logger
        d = { "name": "(root)", "root": 1, "parent": "" }
        self.loggers["(root)"] = LoggerProxy(self, d)

    def read(self, fn):
        ConfigParser.ConfigParser.read(self, fn)
        llist = self.get("loggers", "keys")
        llist = string.split(llist, ",")
        llist.remove("root")
        sectname = "logger_root"
        log = self.loggers["(root)"]
        log.setPropValue("level", self.get(sectname, "level"))
        hlist = self.get(sectname, "handlers")
        hlist = string.split(hlist, ",")
        log.setPropValue("handler", hlist)
        for log in llist:
            sectname = "logger_%s" % log
            hlist = self.get(sectname, "handlers")
            hlist = string.split(hlist, ",")
            d = {
                "name"      : log,
                "level"     : self.get(sectname, "level"),
                "channel"   : self.get(sectname, "channel"),
                "parent"    : self.get(sectname, "parent"),
                "propagate" : self.get(sectname, "propagate"),
                "handler"   : hlist,
            }
            self.loggers[log] = LoggerProxy(self, d)
        hlist = self.get("handlers", "keys")
        if len(hlist):
            hlist = string.split(hlist, ",")
            for hand in hlist:
                sectname = "handler_%s" % hand
                klass = self.get(sectname, "class")
                if klass[:9] == "handlers.":
                    klass = klass[9:]
                d = {
                    "name"      : hand,
                    "class"     : "%sProxy" % klass,
                    "level"     : self.get(sectname, "level"),
                    "formatter" : self.get(sectname, "formatter"),
                }
                hobj = HandlerProxy(self, d)
                hobj.__class__ = eval("%sProxy" % klass)
                hobj.readConfig(sectname)
                self.handlers[hand] = hobj

        flist = self.get("formatters", "keys")
        if len(flist):
            flist = string.split(flist, ",")
            for form in flist:
                sectname = "formatter_%s" % form
                d = {
                    "name"   : form,
                    "format" : self.get(sectname, "format", 1),
                    "datefmt" : self.get(sectname, "datefmt", 1),
                }
                self.formatters[form] = FormatterProxy(self, d)

#        flist = self.get("filters", "keys")
#        if len(flist):
#            flist = string.split(flist, ",")
#            for filt in flist:
#                sectname = "filter_%s" % filt
#                d = {
#                    "name"   : filt,
#                    "lname"  : self.get(sectname, "lname", 1),
#                }
#                self.filters[filt] = FilterProxy(self, d)

    def getFormatter(self, name):
        if name:
            fmt = self.formatters[name]
        else:
            n = len(self.formatters.keys()) + 1
            name = "form%02d" % n
            fmt = FormatterProxy(self, {"name": name})
            self.formatters[name] = fmt
        return fmt

    def getHandler(self, name):
        if name:
            hand = self.handlers[name]
        else:
            n = len(self.handlers.keys()) + 1
            name = "hand%02d" % n
            hand = StreamHandlerProxy(self, {"name": name})
            self.handlers[name] = hand
        return hand

    def getLogger(self, name):
        if name:
            log = self.loggers[name]
        else:
            n = len(self.loggers.keys()) + 1
            name = "log%02d" % n
            log = LoggerProxy(self, {"name": name, "channel": name})
            self.loggers[name] = log
        return log

    def getFormatterChoice(self):
        values = []
        keys = self.formatters.keys()
        keys.sort()
        for f in keys:
            values.append((f, f))
        return tuple(values)

    def getHandlerChoice(self):
        values = []
        keys = self.handlers.keys()
        keys.sort()
        for f in keys:
            values.append((f, f))
        return tuple(values)

    def getFilterChoice(self):
        values = []
        keys = self.filters.keys()
        keys.sort()
        for f in keys:
            values.append((f, f))
        return tuple(values)

    def getLoggerChoice(self):
        values = []
        keys = self.loggers.keys()
        keys.sort()
        for f in keys:
            values.append((f, f))
        return tuple(values)

    def getLoggers(self):
        return self.loggers.values()

    def getHandlers(self):
        return self.handlers.values()

    def getFormatters(self):
        return self.formatters.values()

    def formatterIsUsed(self, name):
        rv = None
        for h in self.handlers.keys():
            if self.handlers[h].getPropValue("formatter") == name:
                rv = h
                break
        return rv

    def handlerIsUsed(self, name):
        rv = None
        for log in self.loggers.keys():
            if name in self.loggers[log].getPropValue("handler"):
                rv = log
                break
        return rv

    def removeFormatter(self, name):
        del self.formatters[name]

    def removeHandler(self, name):
        del self.handlers[name]

    def removeLogger(self, name):
        del self.loggers[name]

    def save(self, fn):
        #needed because 1.5.2 ConfigParser should be supported
        file = open(fn, "w")
        #Write out the keys
        loggers = self.loggers.keys()
        loggers.remove("(root)")
        loggers = filter(lambda x, d=self.loggers: not d[x].deleted, loggers)
        loggers.sort()
        list = ["root"]
        list.extend(loggers)
        file.write("[loggers]\nkeys=%s\n\n" % string.join(list, ","))
        handlers = self.handlers.keys()
        handlers.sort()
        file.write("[handlers]\nkeys=%s\n\n" % string.join(handlers, ","))
        formatters = self.formatters.keys()
        formatters.sort()
        file.write("[formatters]\nkeys=%s\n\n" % string.join(formatters, ","))
        #write out the root logger properties
        log = self.loggers["(root)"]
        log.writeConfig(file)
        #write out other logger properties
        for log in loggers:
            log = self.loggers[log]
            log.writeConfig(file)
        #write out handler properties
        for hand in handlers:
            hand = self.handlers[hand]
            hand.writeConfig(file)
        #write out formatter properties
        for form in formatters:
            form = self.formatters[form]
            form.writeConfig(file)
        file.close()

root = None

def onClose():
    if _popup:
        _popup.withdraw()
    root.destroy()

def main():
    global root
    root=Tk()
    cfg = Configurator(root)
    cfg.pack(side=LEFT, fill=BOTH, expand=1)
    root.protocol("WM_DELETE_WINDOW", onClose)
    root.mainloop()

if __name__ == "__main__":
    main()