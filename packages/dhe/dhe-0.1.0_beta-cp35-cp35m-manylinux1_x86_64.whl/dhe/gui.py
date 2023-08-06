from abc import ABC, abstractmethod
from typing import Union, Tuple, Sequence
from enum import Enum

from dataclasses import fields, dataclass, MISSING, \
    is_dataclass, make_dataclass

import wx  # pylint: disable=import-error
import wx.lib.masked  # pylint: disable=import-error
import wx.lib.intctrl  # pylint: disable=import-error

from .translations import __
from .model import DHEConfiguration, Path
from .core import save_result_csv, calc
from .classify import classify


class Control(ABC):
    @abstractmethod
    def fetch_data(self):
        pass

    @abstractmethod
    def set_data(self, x):
        pass


class IntegralControl(Control):
    def __init__(self, fetch_data, set_data):
        super().__init__()
        self._fetch_data = fetch_data
        self._set_data = set_data

    def fetch_data(self):
        return self._fetch_data()

    def set_data(self, x):
        self._set_data(x)


class ComposedControl(Control):
    def __init__(self, T):
        super().__init__()
        self.controls = []
        self.type = T

    def add_control(self, key, ctrl):
        self.controls.append((key, ctrl))

    def fetch_data(self):
        return self.type(**{key: ctrl.fetch_data()
                            for key, ctrl in self.controls})

    def set_data(self, x):
        for key, ctrl in self.controls:
            ctrl.set_data(getattr(x, key))


class MergedControl(Control):
    def __init__(self, T):
        super().__init__()
        self.controls = []
        self.type = T

    def grab(self, w):
        self.controls.append(w.ctrl)
        return w

    def grab_constructor(self, c):
        def _constructor(parent):
            return self.grab(c(parent))
        return _constructor

    def fetch_data(self):
        parts = (ctrl.fetch_data() for ctrl in self.controls)
        dct = {}
        for p in parts:
            dct.update(**{f.name: getattr(p, f.name) for f in fields(p)})
        return self.type(**dct)

    def set_data(self, x):
        for ctrl in self.controls:
            ctrl.set_data(ctrl.type(**{f.name: getattr(x, f.name)
                                       for f in fields(ctrl.type)}))


class PolymorphicControl(Control):
    def __init__(self, control_by_type, initial_type, on_set_type):
        super().__init__()
        self.control_by_type = control_by_type
        self._control = control_by_type[initial_type]
        self.on_set_type = on_set_type

    def fetch_data(self):
        return self._control.fetch_data()

    def set_data(self, x):
        self._control = self.control_by_type[type(x)]
        self._control.set_data(x)
        self.on_set_type(type(x))


class ArrayControl(Control):
    def __init__(self, set_n):
        super().__init__()
        self.item_controls = []
        self.set_n = set_n

    def fetch_data(self):
        return [w.fetch_data() for w in self.item_controls]

    def set_data(self, x):
        self.set_n(len(x))
        for _x, _c in zip(x, self.item_controls):
            _c.set_data(_x)


def unit_to_label(unit):
    if unit is None:
        return ""
    return "[{}]".format(str(unit))


def value_w_unit_to_label(value, unit):
    text = str(value)
    if unit is not None:
        text += " " + unit_to_label(unit)
    return text


def label_from_field(f):
    return f.metadata.get("help", f.name)


def constructor(f):
    def _decorator(*args, **kwargs):
        def _wrapped_f(parent):
            return f(parent, *args, **kwargs)
        return _wrapped_f
    return _decorator


def entangled_constructors(multi_constructor):
    widgets = None
    n = len(multi_constructor.__annotations__["return"].__args__)

    def _constructor_n(i):
        def _constructor(parent):
            nonlocal widgets
            if widgets is None:
                widgets = multi_constructor(parent)
            return widgets[i]
        return _constructor
    return (_constructor_n(i) for i in range(n))


# class NumEntry(wx.lib.masked.NumCtrl):
#     def __init__(self, parameter, parent, default=0.):
#         self.ctrl = IntegralControl(parameter,
#                                     fetch_data=self.GetValue,
#                                     set_data=self.SetValue)
#         if default is MISSING:
#             default = 0.
#         super().__init__(parent=parent, value=default,
#                          style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)

class Widget:
    def __init__(self, *args,
                 label=None,
                 unit=None,
                 ctrl,
                 default=MISSING,
                 **kwargs):
        self.label = label
        self.unit = unit
        self.ctrl = ctrl
        self.default = default
        super().__init__(*args, **kwargs)

    @abstractmethod
    def set_visible(self, visible=True):
        pass

    @abstractmethod
    def with_compagnons(self):
        pass


class WxWidget(Widget):
    def set_visible(self, visible=True):
        if visible:
            self.Show()  # pylint: disable=no-member
        else:
            self.Hide()  # pylint: disable=no-member

    def with_compagnons(self):
        return (Label(self.GetParent(), self.label or ""), self,  # pylint: disable=no-member
                Label(self.GetParent(), unit_to_label(self.unit)))  # pylint: disable=no-member


class NumEntry(WxWidget, wx.TextCtrl):
    def __init__(self, parent, default=0., **kwargs):
        ctrl = IntegralControl(fetch_data=self.GetValue,
                               set_data=self.SetValue)
        if default is MISSING:
            default = 0.
        super().__init__(parent=parent, value=str(default),
                         style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB,
                         default=default, ctrl=ctrl, **kwargs)

    def GetValue(self):
        return float(super().GetValue())

    def SetValue(self, x):
        super().SetValue(str(x))


class IntValidator(wx.lib.intctrl.IntValidator):
    def OnChar(self, event):
        key = event.GetKeyCode()
        ctrl = event.GetEventObject()
        pos = ctrl.GetInsertionPoint()
        sel_start, sel_to = ctrl.GetSelection()
        select_len = sel_to - sel_start
        value = ctrl.GetValue()
        textval = wx.TextCtrl.GetValue(ctrl)
        allow_none = ctrl.IsNoneAllowed()
        if key in (wx.WXK_DELETE, wx.WXK_BACK, wx.lib.intctrl.WXK_CTRL_X):
            if select_len:
                new_text = textval[:sel_start] + textval[sel_to:]
            elif key == wx.WXK_DELETE and pos < len(textval):
                new_text = textval[:pos] + textval[pos + 1:]
            elif key == wx.WXK_BACK and pos > 0:
                new_text = textval[:pos - 1] + textval[pos:]
            # (else value shouldn't change)
            if new_text == '' and not allow_none:
                # Deletion of last significant digit:
                wx.CallAfter(ctrl.SetValue, value)
                wx.CallAfter(ctrl.SetInsertionPoint, 0)
                wx.CallAfter(ctrl.SetSelection, 0, -1)
                return
        super().OnChar(event)


class IntEntry(WxWidget, wx.lib.intctrl.IntCtrl):
    def __init__(self, parent, default=0, **kwargs):
        ctrl = IntegralControl(fetch_data=self.GetValue,
                               set_data=self.SetValue)
        if default is MISSING:
            default = 0
        super().__init__(parent=parent, value=default,
                         default=default, ctrl=ctrl, **kwargs)
        # , validator=IntValidator())


class RadioBox(wx.RadioBox):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, pos=(80, 10),
                         majorDimension=1, style=wx.RA_SPECIFY_ROWS, **kwargs)


class RadioBoxWithCallbacks(RadioBox):
    def __init__(self, parent, callback_by_choice, default=None, **kwargs):
        choices, _ = zip(*callback_by_choice)
        super().__init__(parent, choices=choices, **kwargs)
        self.SetSelection(choices.index(default))
        self.callback_by_choice = dict(callback_by_choice)
        self.Bind(wx.EVT_RADIOBOX, self.on_select)

    def on_select(self, e):
        choice = e.GetEventObject().GetStringSelection()
        callback = self.callback_by_choice[choice]
        callback()


class EnumRadioBox(WxWidget, RadioBox):
    def __init__(self, parent, choices, default=MISSING, **kwargs):
        reverse_lookup = {val: key for key, val in choices.items()}

        def fetch_data():
            return choices[self.GetStringSelection()]

        def set_data(x):
            self.SetStringSelection(reverse_lookup[x])
        choice_keys = list(choices)
        ctrl = IntegralControl(fetch_data=fetch_data,
                               set_data=set_data)
        super().__init__(parent, choices=choice_keys, ctrl=ctrl, default=default,
                         **kwargs)
        if default is not MISSING:
            self.SetSelection(choice_keys.index(default))


class TextEntry(WxWidget, wx.TextCtrl):
    def __init__(self, parent, default="", **kwargs):
        ctrl = IntegralControl(fetch_data=self.GetValue,
                               set_data=self.SetValue)
        super().__init__(parent, value=default, ctrl=ctrl, default=default,
                         **kwargs)


class FilePicker(WxWidget, wx.FilePickerCtrl):
    def __init__(self, parent, default="", **kwargs):
        ctrl = IntegralControl(fetch_data=self.GetPath,
                               set_data=self.SetPath)
        super().__init__(parent, path=default, ctrl=ctrl, default=default,
                         style=wx.FLP_CHANGE_DIR,
                         **kwargs)


class Stack(wx.Panel):
    def __init__(self, parent, *constructors, orient=wx.VERTICAL):
        super().__init__(parent)
        layout = wx.BoxSizer(orient=orient)
        for _constructor in constructors:
            layout.Add(_constructor(self))
        self.layout = layout
        self.SetSizer(layout)

    def add(self, w):
        self.layout.Add(w)


class ScrolledWindow(wx.ScrolledWindow):
    def __init__(self, parent, child_constructor):
        super().__init__(parent)
        child = child_constructor(self)
        self.child = child
        layout = wx.BoxSizer()
        layout.Add(child)
        self.SetSizer(layout)
        self.SetScrollRate(0, 1)


class WrapStack(WxWidget, Stack):
    def __init__(self, *args, before=(), wrap, after=(), **kwargs):
        self.wrapped = None

        def wrap_constructor(*args):
            self.wrapped = wrap(*args)
            return self.wrapped
        constructors = before + (wrap_constructor,) + after
        super().__init__(*args, *constructors, ctrl=None, **kwargs)
        self.ctrl = self.wrapped.ctrl
        self.label = self.wrapped.label
        self.unit = self.wrapped.unit
        self.default = self.wrapped.default

    def with_compagnons(self):
        stack = Stack(self.GetParent(),
                      constructor(Heading)(self.label or ""),
                      lambda parent: self)
        self.Reparent(stack)
        return (stack,)


class PolymorphicWidget(WxWidget, Stack):
    def __init__(self, parent, *,
                 widget_constructor_by_type,
                 initial_type,
                 **kwargs):
        super().__init__(parent, ctrl=None, **kwargs)
        widgets_by_type = tuple((t, c(self))
                                for t, c in widget_constructor_by_type)
        self.widgets_by_type = widgets_by_type

        def on_set_type(t):
            return lambda: self.set_type(t)

        radio_box = RadioBoxWithCallbacks(
            self,
            callback_by_choice=tuple((w.label, on_set_type(t))
                                     for t, w in widgets_by_type),
            default=next(
                w.label for t, w in widgets_by_type if t is initial_type)
        )
        self.add(radio_box)
        for _, w in widgets_by_type:
            self.add(w)
        self.ctrl = PolymorphicControl(
            control_by_type={t: w.ctrl for t,
                             w in widgets_by_type},
            initial_type=initial_type,
            on_set_type=self.set_type)
        self.set_type(initial_type)

    def set_type(self, new_t):
        for t, w in self.widgets_by_type:
            w.set_visible(t is new_t)
        update_layout(self)


def polymorphic_widget_by_field(f, **kwargs):
    types = f.type.__args__
    return constructor(PolymorphicWidget)(
        widget_constructor_by_type=tuple((t, widget_by_field_tab(_field(t)))
                                         for t in types),
        initial_type=type(f.default),
        unit=f.metadata.get("unit"), **kwargs)


class ComposedWidget(WxWidget, wx.Panel):
    def __init__(self, parent, T, widget_constructors, **kwargs):
        super().__init__(parent, ctrl=ComposedControl(T), **kwargs)

        cols = 3
        layout = wx.GridBagSizer(vgap=5, hgap=5)
        for row, (key, _constructor) in enumerate(widget_constructors):
            widget = _constructor(self)
            widget_row = widget.with_compagnons()
            span = cols - len(widget_row) + 1
            for col, w in enumerate(widget_row):
                layout.Add(w, pos=(row, col), flag=wx.EXPAND, span=(1, span))
            if hasattr(widget, "ctrl"):
                self.ctrl.add_control(key, widget.ctrl)
        self.SetSizer(layout)

    def with_compagnons(self):
        stack = Stack(self.GetParent(),
                      constructor(Heading)(self.label or ""),
                      lambda parent: self)
        self.Reparent(stack)
        return (stack,)


def composed_widget_by_type(f, **kwargs):
    return constructor(ComposedWidget)(
        T=f,
        widget_constructors=tuple((_f.name, widget_by_field_tab(_f))
                                  for _f in fields(f)),
        **kwargs)


def composed_widget_by_field(f, **kwargs):
    return composed_widget_by_type(f.type, **kwargs)


class ArrayWidgetBase(WxWidget, wx.Panel):
    def header(self):
        pass

    @abstractmethod
    def control_from_item(self, item):
        pass

    @abstractmethod
    def item_destructor(self, item):
        pass

    @abstractmethod
    def update_layout(self):
        pass

    def __init__(self, parent, *,
                 n=0,
                 item_constructor,
                 default=MISSING,
                 **kwargs):
        self.items = []
        self.item_constructor = item_constructor
        super().__init__(parent,
                         ctrl=ArrayControl(self.set_n),
                         default=default, **kwargs)
        self.header()
        self.on_set_n = lambda n: None
        if n == 0:
            self.update_layout()
        else:
            self.set_n(n)
        if default is not MISSING:
            self.ctrl.set_data(default)

    def get_n(self):
        return len(self.items)

    def set_n(self, n):
        dn = n - self.get_n()
        if dn == 0:
            return
        if dn > 0:
            for _ in range(dn):
                item = self.item_constructor(self)
                self.ctrl.item_controls.append(
                    self.control_from_item(item))
                self.items.append(item)
        else:
            for row in self.items[n:]:
                self.item_destructor(row)
            del self.ctrl.item_controls[n:]
            del self.items[n:]
        self.update_layout()
        self.on_set_n(n)


class TabularArrayWidget(ArrayWidgetBase):
    def __init__(self, parent, *, item_type, header, **kwargs):
        self.header_strings = header
        self.item_type = item_type
        self.cols = len(self.header_strings)
        self.header_widgets = []
        super().__init__(parent, **kwargs)

    def header(self):
        self.header_widgets = tuple(Label(self, l)
                                    for l in self.header_strings)

    def control_from_item(self, item):
        ctrl = ComposedControl(self.item_type)
        for key, w in item:
            ctrl.add_control(key, w.ctrl)
        return ctrl

    def item_destructor(self, item):
        for _key, w in item:
            w.Destroy()

    def update_layout(self):
        rows = 1 + self.get_n()
        cols = self.cols
        layout = wx.GridSizer(rows, cols, 5, 5)
        for h in self.header_widgets:
            layout.Add(h, 0, wx.EXPAND)
        for widget_row in self.items:
            for _, widget in widget_row:
                layout.Add(widget, 0, wx.EXPAND)
        self.SetSizer(layout)
        update_layout(self)


def tabular_array_widget_by_type(T, **kwargs):
    _fields = fields(T) if is_dataclass(T) else (_field(T),)

    item_constructors = tuple((f.name, widget_by_field_tab(f))
                              for f in _fields)

    def item_constructor(parent):
        return tuple((key, c(parent)) for key, c in item_constructors)

    return constructor(TabularArrayWidget)(
        header=tuple(label_from_field(f) for f in _fields),
        item_constructor=item_constructor,
        item_type=T,
        **kwargs)


class ArrayWidget(ArrayWidgetBase):
    def update_layout(self):
        rows = self.get_n()
        cols = 1
        layout = wx.GridSizer(rows, cols, 5, 5)
        for widget in self.items:
            layout.Add(widget, flag=wx.EXPAND)
        self.SetSizer(layout)
        update_layout(self)

    def control_from_item(self, item):
        return item.ctrl

    def item_destructor(self, item):
        item.Destroy()


def array_widget_by_field(f, **kwargs):
    return constructor(ArrayWidget)(
        item_constructor=widget_by_field_tab(f),
        **kwargs)


class Field:
    def __init__(self, name, T):
        self.name = name
        self.type = T
        self.metadata = {}
        self.default = MISSING


def _field(T: type):
    return Field(T=T, name=T.__name__)


def tuple_widget_by_field(f, **kwargs):
    item_types = f.type.__args__
    kwargs["label"] = label_from_field(f)
    n = len(item_types)
    return array_widget_by_field(
        _field(item_types[0]), n=n, **kwargs)


def array_widget_auto_by_field(f, **kwargs):
    item_type = f.type.__args__[0]
    kwargs["label"] = label_from_field(f)
    n = f.metadata.get("n")
    if n is not None:
        return array_widget_by_field(
            _field(item_type), n=n, **kwargs)
    cls = classify(item_type)
    if cls is None \
       or (cls is dataclass and
           all(f.type in type_mapping
               for f in fields(item_type))):
        return with_n_control(
            tabular_array_widget_by_type(
                item_type, **kwargs))
    return with_n_control(array_widget_by_field(_field(item_type), **kwargs))


def update_layout(w):
    parent = w.GetParent()
    if parent is not None:
        parent.Fit()
        update_layout(parent)
    if hasattr(w, "Layout"):
        w.Layout()


def widget_by_field_tab(f, **kwargs):
    if f.default is not MISSING:
        kwargs["default"] = f.default
    return meta_type_mapping[classify(f.type)](
        f,
        label=label_from_field(f),
        **kwargs)


def widget_by_field(f, **kwargs):
    T = f.type
    if issubclass(T, Enum):
        return constructor(EnumRadioBox)(choices=T.__members__,
                                         unit=f.metadata.get("unit"))
    return type_mapping[T](unit=f.metadata.get("unit"), **kwargs)


type_mapping = {
    float: constructor(NumEntry),
    int: constructor(IntEntry),
    str: constructor(TextEntry),
    Path: constructor(FilePicker),
}


meta_type_mapping = {
    Union: polymorphic_widget_by_field,
    dataclass: composed_widget_by_field,
    None: widget_by_field,
    Sequence: array_widget_auto_by_field,
    Tuple: tuple_widget_by_field
}


def with_n_control(array_widget_constructor, **kwargs):
    def multi_constructor(parent) -> Tuple[Widget, Widget]:
        array_widget = array_widget_constructor(parent)
        n_control = wx.SpinCtrl(parent, value=str(array_widget.get_n()))
        n_control.Bind(wx.EVT_SPINCTRL,
                       lambda _: array_widget.set_n(n_control.GetValue()))
        array_widget.on_set_n = n_control.SetValue
        return array_widget, n_control

    def _constructor(parent):
        arr_constructor, n_ctrl_constructor = entangled_constructors(
            multi_constructor)
        return WrapStack(parent,
                         before=(n_ctrl_constructor,),
                         wrap=arr_constructor,
                         **kwargs)

    return _constructor


def Label(parent, text, font=None):
    label_ = wx.StaticText(parent, -1, label=text, style=wx.ALIGN_LEFT)
    if font is not None:
        label_.SetFont(font)
    return label_


def Heading(parent, text):
    return Label(parent,
                 text,
                 font=wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))  # pylint: disable=no-member


class MainFrame(wx.Frame):
    def __init__(self, *_args, **kwargs):
        super().__init__(None, title='DHE', **kwargs)
        self.InitUI()

    def InitUI(self):
        self.toolbar = self.CreateToolBar()

        def create_toolbutton(parent, toolbar, ico, callback):
            tool = toolbar.AddTool(wx.ID_ANY, '', wx.ArtProvider.GetBitmap(
                id=ico, client=wx.ART_MENU))
            parent.Bind(wx.EVT_MENU, callback, tool)
        create_toolbutton(self, self.toolbar, wx.ART_PRINT, self.calc_handler)
        create_toolbutton(self, self.toolbar,
                          wx.ART_FILE_SAVE, self.save_handler)
        create_toolbutton(self, self.toolbar,
                          wx.ART_FILE_OPEN, self.open_handler)
        self.toolbar.Realize()

        notebook = wx.Notebook(self)
        main_ctrl = MergedControl(DHEConfiguration)

        def sub_dataclass(name, base, sub_fields):
            base_fields = {f.name: f for f in fields(base)}
            return make_dataclass(
                name,
                fields=(
                    (f_name, base_fields[f_name].type, base_fields[f_name])
                    for f_name in sub_fields))

        def sub_ctrl(name, subfields):
            return constructor(ScrolledWindow)(
                main_ctrl.grab_constructor(
                    composed_widget_by_type(
                        sub_dataclass(name,
                                      DHEConfiguration,
                                      subfields))))

        notebook.AddPage(sub_ctrl("DHEPage",
                                  ("dhe",))(notebook),
                         __("DHE")
                         )
        notebook.AddPage(
            sub_ctrl("SoilPage",
                     ("soil_parameters",
                      "soil_layers")
                     )(notebook),
            __("Soil"))
        notebook.AddPage(sub_ctrl(
            "CalcPage",
            ("dim_ax",
             "dim_rad",
             "Gamma",
             "R",
             "opt_n_steps_multiplier",
             "adiabat",
             "n_steps_0",
             "dt_boundary_refresh",
             "dt",
             "t0",
             "T_brine_method",
             "calculation_mode"))(notebook),
            __("Calculation Parameters"))

        self.control = notebook
        self.main_ctrl = main_ctrl
        # main_ctrl.set_data(DHEConfiguration())
        self.Centre()

    def calc_handler(self, _e):
        cfg = self.main_ctrl.fetch_data()
        result = calc(cfg)
        pathname = self.show_save_dialog(
            __("Save csv result file"),
            wildcard="CSV {} (*.csv)|*.csv".format(__("files")))
        try:
            save_result_csv(result, pathname)
        except IOError:
            wx.LogError(
                __("Cannot save current data in file") +
                " '{}'.".format(pathname))

    def show_save_dialog(self, caption, wildcard):
        with wx.FileDialog(
                self, caption, wildcard=wildcard,
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return None    # the user changed their mind

            # save the current contents in the file
            return fileDialog.GetPath()

    def save_handler(self, _e):
        pathname = self.show_save_dialog(
            __("Save json file"),
            wildcard="JSON {} (*.json)|*.json".format(__("files")))
        cfg = self.main_ctrl.fetch_data()
        try:
            DHEConfiguration.save(cfg, pathname)
        except IOError:
            wx.LogError(
                __("Cannot save current data in file") +
                " '{}'.".format(pathname))

    def open_handler(self, _e):
        with wx.FileDialog(
                self, __("Open JSON file"),
                wildcard="JSON {} (*.json)|*.json".format(__("files")),
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            config_file = fileDialog.GetPath()
            try:
                cfg = DHEConfiguration.load(config_file)
                self.main_ctrl.set_data(cfg)
            except IOError:
                wx.LogError(__("Cannot open file '{}'.").format(config_file))


def main():
    app = wx.App()
    main_frame = MainFrame()
    main_frame.Show()
    app.MainLoop()
