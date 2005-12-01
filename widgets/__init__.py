import cgi
import re
import urllib

"""widgets module -- a framework for generating dynamic web pages

Widgets are a way of organizing python code which generates web pages. The idea
behind them is simple: take various components of web pages, like forms, form
elements, navigation areas, even entire web applications, and implement them as
python classes, with the more complex classes containing and reusing the
simpler ones, and each class instance responsible for outputting a chunk of the
page's HTML.

A Widget class implements two methods: First, an __init__ method where it
initializes its state, assigns members, creates child widgets, reads form
variables, and does anything else that needs to be done before page output is
generated. Second, a write method where it produces whatever HTML output
it's responsible for. Both methods take Request objects as arguments, which
provide a simple server-independent interface for accessing form variables and
HTTP headers, and sending output.

And that's basically all there is to Widgets. This framework provides a
number of widget classes useful for implementing form-driven applications,
some Request classes for server environments like CGI and Mod_Python, and
some helper classes which make it easy to use Template engines like Cheetah,
PSP, or EZT to generate widget output. The sole concern of this framework is
organizing the complex logic used to generate web pages by breaking those
pages down into independent components. Unlike other web frameworks it is not
concerned with things like URL schemes, database access, authentication,
MVC separation, and so on, except in being flexible enough to work with
software and design schemes that do provide these things."""


class Widget:
  """Abstract base for Widget classes

  Subclasses implement two methods (not defined in the class body to avoid
  masking other definitions when multiple inheritance is used):

    __init__(self, req, ...)
      implementations of this method should initialize members and load
      widget state. In a well-behaved application, this method will be
      called before any page output is written, making it possible for widgets
      to do things like set cookies, issue redirects, and modify the states
      of other widgets here.

    write(self, req, ...)
      implementations of this method should mostly just write HTML output
      to the page.

    Both methods take a Request object as an argument, and sometimes other
    arguments as well, depending on what a widget does."""


class Request:
  """Abstract base for Request classes

  Request objects are used by widgets to interact with the web server. They
  provide a means of reading and writing request data.

  They define the following members:

    form
      an object, such as cgi.FieldStorage, which provides getfirst(),
      getlist(),and keys() methods for retrieving values of GET and
      POST variables. These methods are described in cgi.FieldStorage
      docstring and in the Python Standard Library Reference

    get
      an object exactly like "form" but only returns the values of GET
      variables

    post
      an object exactly like "form" but only returns the values of POST
      variables

    Some web server interfaces make it difficult to separate GET and POST
    variables. Request objects for these servers may make "get" and "post"
    members aliases to the "form" object as incorrect, but probably harmless
    expedients."""

  def write(self, data):
    """Write data to client

    This should be implemented as a buffered write because widgets and
    templates typically output small amounts of data at a time"""
    raise NotImplementedError

  def flush(self, data):
    """Flush write buffer, if any"""
    raise NotImplementedError

  def server_name(self):
    """Return server name
    Example: Returns "hello.com" for http://hello.com:88/page.py/path?1=2"""
    raise NotImplementedError

  def server_port(self):
    """Return server port number as integer
    Example: Returns 88 for http://hello.com:88/page.py/path?1=2"""
    raise NotImplementedError

  def is_https(self):
    """Return True if this is an HTTPS request, False for HTTP"""
    raise NotImplementedError

  def request_uri(self):
    """Return raw requested URI from first line of HTTP request
    Example: Returns "/page.py/path?1=2" for
    http://hello.com:88/page.py/path?1=2"""
    raise NotImplementedError

  def script_name(self):
    """Return script name
    Example: Returns "page.py" for http://hello.com:88/page.py/path?1=2"""
    raise NotImplementedError

  def path_info(self):
    """Return extended path
    Example: Returns "/path" for http://hello.com:88/page.py/path?1=2"""
    raise NotImplementedError

  def query_string(self):
    """Return query string
    Example: Returns "1=2" for http://hello.com:88/page.py/path?1=2"""
    raise NotImplementedError


class Template:
  """Abstract base for Template classes

  Template objects provide a common interface for a variety of template
  engines."""

  def __init__(self, string=None, file=None):
    """Load a template from a string or file

    string can be a string containing template code

    file can be the path to a file containing template code

    The template can specified as either a string or file, but not both.
    Subclasses should attempt to do as much initialization as possible here,
    including parsing and compiling template code, so there's less work to be
    done when execute() is called."""
    raise NotImplementedError

  def execute(self, req, dataobj):
    """Execute template, writing to req and using data from dataobj

    req is a request object

    dataobj is an object whose members will be exposed as template variables"""
    raise NotImplementedError

  def callback(self, cb):
    ### Need to implement Template classes for templates other than EZT
    ### to see if this interface is at all workable...
    """Adapt a callback for use in a template

    cb should be a callable object that takes a request object as its
    first argument, for example a bound Widget.write method. It may take
    additional arguments as well if the template engine allows passing
    arguments to callbacks."""
    raise NotImplementedError


class TemplateWidget(Widget):
  """Base class for Widgets that output templates populated with member data

  Base classes set a member called "template" member to a Template object.
  When the write method is called it executes the template, making other
  members available as template variables.

  The point of this class is to make it possible to make simple widgets
  wholly out of templates and python class declarations, with little or
  no supporting python code. It is not intended to be subclassed by widgets
  that implement __init__ and write methods, or have members of their
  own which don't need to be exposed to templates. These classes should the
  use the Template interface directly."""

  def __init__(self, req, **args):
    """Default constructor that saves any keyword arguments as members"""
    vars(self).update(args)

  def write(self, req):
    """Execute self.template passing self as input and writing output to req"""
    self.template.execute(req, self)

  def embed(self):
    """Return Widget as a template variable that can be included in other
    templates"""
    return self.template.callback(lambda req: self.template.execute(req, self))


class Form:
  """Class holding common data for all widgets on a form

  Form instances have the following public members:

    name
      string holding value of the form's "name=" attribute. It is used by
      widgets that output javascript accessing form elements.

    url
      string holding a link to the current page without any query parameters.
      If not overridden, this member is automatically initialized in the
      constructor, Typicaly it is a server-relative URL (i.e. "/dir/page.py")
      or a location-relative URL (i.e. "page.py") meant to go in a form's
      "action=" attribute. It is also used as the base URL for links returned
      by the Form.get_url() method.

    Applications may set additional members on Form objects to share
    information (like session data) or resources (like database connections)
    between widgets."""

  def __init__(self, req, name=None, url=None):
    """Create Form object, see class docstring for argument meanings

    req is the Request object

    name can be set to None on forms with no javascript widgets, but it's a
    good idea to set it whenever you have any widgets in a <form> element, in
    case you decide to add javascript in the future.

    url is usually just None so the member will be automatically initialized"""

    self.name = name
    if url is None:
      self.url = _url(req)
    else:
      self.url = url
    self._url_vars = []

  def get_url(self, extra_vars, remove_vars):
    """Return URL to current page with state preserved in URL params

      extra_vars is a list of (name, value) tuples to add the URL query string

      remove_vars is a list of state-containing variable names to omit from
      the outputted URL

    Most widgets do not ever call this function because they store their state
    in form elements that get passed back when the user submits the form.
    However, on pages that don't display editable form elements, it's nice to
    be able to provide an interface made of simple html hyperlinks rather than
    submit buttons. This function can be used to generate hyperlinks with
    widget state information and extra parameters stored in the query string
    for that purpose.

    Note that to prevent URL bloat, most widgets will not include their state
    in the generated URLs, unless you first call their write_hidden method with
    the WRITE_URL flag."""
    params = []

    for name, value in extra_vars:
      params.append("%s=%s" % (_escape_url(name), _escape_url(value, True)))

    for name, value in self._url_vars:
      if name not in remove_vars:
        params.append("%s=%s" % (_escape_url(name), _escape_url(value, True)))

    return "?".join((self.url, "&".join(params)))

  def add_url_var(self, name, value):
    """Add name, value pair to include in get_url generated URLs."""
    self._url_vars.append((name, value))

  def short_name(self, name):
    """Hook for mapping dot-separated widget identifiers to shorter names

    To allow multiple instances of widgets to coexist on the same page without
    name clashes, form widgets use identifiers like "widget.childwidget.param"
    in HTML output to guarantee that each widget's identifiers are unique. But
    sometimes you can guarantee that there will only be one instance of a widget
    on a page. In this case you can override the short_name method to map widget
    identifiers to shorter names. The widget loading and writing code will
    automatically perform the substitutions, resulting in cleaner html output
    and more user-friendly urls without any further changes to the code."""
    return name


# flags for FormWidget.__init__ and FormWidget.read_value
# (see FormWidget.read_value docstring for descriptions)
READ_DEFAULT = 1 << 0
READ_URL     = 1 << 1
READ_POST    = 1 << 2
READ_FORM    = READ_URL | READ_POST


# flags for FormWidget.write_hidden and FormWidget.write_value
# (see FormWidget.write_value docstring for descriptions)
WRITE_FORM = 1 << 0
WRITE_URL  = 1 << 1


class FormWidget(Widget):
  """Abstract base for Form Widgets

  Subclasses implement two methods (not defined in the class body to avoid
  masking other definitions when multiple inheritance is used):

    write(self, req, ...)
      implementations of this method write the HTML contents of widget to the
      the page. The first argument is a Request object. Typically only
      primitive widgets (like buttons and checkboxes) accept additional
      arguments, usually for things like labels, captions, and HTML attributes
      which affect widget appearance without affecting behavior. They provide
      these arguments for maximum flexibility and to restrict their
      implementations to application logic, leaving callers to work out
      presentation logic. More complex widgets are usually less flexible about
      how they are displayed and separate their presentation logic from
      application logic by other means, such as templates.

    write_hidden(self, req, flags=WRITE_FORM)
      implementations of this method write widget state without outputting any
      user-visible HTML, typically by making calls to FormWidget.write_value()
      which emit <input type="hidden"> elements. The first argument, req, is
      a Request object. The second argument, flags, is a set of WRITE_* flags
      described in the FormWidget.write_value() docstring. The flags are
      usually just passed along unaltered to calls of that function.

  FormWidget instances have 2 public members:

    form
      instance of Form class the FormWidget is associated with

    full_id
      a base string used by the FormWidget.id() method to generate unique
      names for page elements associated with the widget."""

  def __init__(self, req, parent, id, flags=READ_FORM):
    """Construct form widget

    req is the Request object

    parent is a Form object if this is a top level widget, or another widget
    if this is a child widget.

    id is a base string which is prepended with the parent widget's full id
    and used to initialize the the FormWidget.full_id member

    flags is a set of READ_* flags described in the FormWidget.read_value
    docstring. Typically it will just be forwarded to calls to that function.

    FormWidget classes which override this method should be sure to call it
    internally. Almost all subclasses will extend this method and use it to
    load widget state."""

    if isinstance(parent, Form):
      self.full_id = id
      self.form = parent
    else:
      self.full_id = _join_ids(parent.full_id, id)
      self.form = parent.form

  def id(self, id=None):
    """Return Widget identifer or another identifier prefixed with it"""
    full_id =  _join_ids(self.full_id, id)
    return self.form.short_name(full_id)

  def read_value(self, req, id, flags):
    """read value from URL or POST request variables

    req is the request object

    id is a string specifying what value to read. This string prefixed with
    the FormWidget.full_id is the name of the variable that will be looked up

    flags can be a bitwise combination of the following values

      READ_DEFAULT
        if this flag is set, all other flags are ignored and the function
        returns None. The flag indicates that the widget is newly created
        (did not exist in previous page loads) and should initialize itself
        to a default state.

      READ_URL
        looks up variable in URL query string (i.e. the part after the question
        mark in "page.py?widget.var=value")

      READ_POST
        looks up variable in POST data (i.e. a form field submitted in a
        <form "method=post" ...> form)

      READ_FORM
        bitwise combination of READ_URL and READ_POST that finds form field
        values regardless of whether they were submitted in a method="get" or
        a method="post" form.

    If multiple values are found, this function only returns the first one.
    The FormWidget.read_values method can be used instead of this one to
    retrieve multiple values.

    If no values are found this function returns None"""

    fs = _get_storage(req, flags)
    if fs is not None:
      full_id = self.id(id)
      value = fs.getfirst(full_id)
      if value is not None:
        return value
    return None

  def read_values(self, req, id, flags):
    """Read values from URL or POST variables

    This function takes the same arguments as FormWidget.read_value. The only
    difference is that it is a generator that yields ALL the values
    corresponding to an identifer instead of just returning the first value."""
    fs = _get_storage(req, flags)
    if fs is not None:
      full_id = self.id(id)
      for value in fs.getlist(full_id):
        yield value

  def enum_values(self, req, flags):
    """Enumerate URL or POST variables associated with this widget

      req is the current request object
      flags are described in FormWidget.read_value docstring

    The return value is the sequence of all the id strings that can be
    passed to FormWidget.read_value and not return None"""

    # This function currently works by doing a linear search through all the
    # request variables, which might not be the most efficient thing to do
    # on pages with a lot of widgets. Multiple calls could be optimized by
    # splitting variable names on the dots and putting them in nested
    # dictionaries organized as a trie. Or a normal character based trie
    # could be used, if such a thing exists for python. But really, this
    # function should never need to be optimized. The only widget that
    # relies on it is DataButton, and there is typically only one
    # DataButton doing the search per page request.

    fs = _get_storage(req, flags)
    if fs is not None:
      prefix = self.id("")
      for field in fs.keys():
        if field.startswith(prefix):
          yield field[len(prefix):]

  def write_value(self, req, id, value, flags):
    """Store value so it can be read by the widget on future page loads

    req is the current request object

    id is a string that identifies the value, and can be passed
    to FormWidget.read_value() in future page loads.

    value is the string value to be written

    flags determines what this function does with the value, it can be a
    bitwise combination of the following flags

      WRITE_FORM
        store value by writing an <input type=hidden...> form field to the
        HTML output

      WRITE_URL
        store value by calling Form.add_url_var for inclusion in hyperlinks
        generated by Form.get_url()

    In the future, more flags could be added to store state in other places
    like session objects or cookies."""

    if value is None:
      return

    full_id = self.id(id)
    if flags & WRITE_FORM:
      _tag(req, "input", ("type", "hidden"),
           ("name", full_id), ("value", value))

    if flags & WRITE_URL:
      self.form.add_url_var(full_id, value)


class TextBox(FormWidget):
  """Text input widget

  Members:

    text
      string containing widget text"""

  def __init__(self, req, parent, id, flags):
    FormWidget.__init__(self, req, parent, id, flags)
    self.text = self.read_value(req, None, flags)

  def write_hidden(self, req, flags):
    self.write_value(req, None, self.text, flags)

  def write(self, req, cols=0, rows=0, *attribs):
    """Write input box

    cols
      width of field, passed as textarea "cols" attribute or text input "size"
      attribute (only if nonzero)

    rows
      If nonzero, writes a <textarea> field with the specified number of rows.
      If zero, writes an <input type=text> field

    attribs
      extra attributes to add to html tag in (name, value) tuples"""
    id = self.id()
    if rows:
      _tag(req, "textarea", ("name", id), ("rows", rows), ("cols", cols),
           open=True)
      req.write(_escape_html(self.text or ""))
      _ctag(req, "textarea")
    else:
      _tag(req, "input", ("name", id),
           self.text is not None and ("value", self.text) or None,
           cols and ("size", cols) or None, *attribs)


# The CheckBox, RadioButton, SelectBox, and MSelectBox classes have a lot
# of methods in common, so they share implementations through the
# _SingleSelect, _MultipleSelect, and _ClickBox and _SelectBox mixin classes
# below

class _SingleSelect(FormWidget):
  """Mixin class providing common methods for RadioButton and SelectBox"""

  def __init__(self, req, parent, id, flags):
    FormWidget.__init__(self, req, parent, id, flags)
    self.selected = self.read_value(req, None, flags)

  def write_hidden(self, req, flags):
    self.write_value(req, None, self.selected, flags)

  def is_selected(self, value):
    """Return True if the specified value is currently selected"""
    return self.selected == value

  select_multiple = False


class _MultipleSelect(FormWidget):
  """Mixin class providing common methods for CheckBox and MSelectBox"""

  def __init__(self, req, parent, id, flags):
    FormWidget.__init__(self, req, parent, id, flags)
    self.selected = list(self.read_values(req, None, flags))

  def write_hidden(self, req, flags):
    for item in self.selected:
      self.write_value(req, None, item, flags)

  def is_selected(self, value):
    """Return True if the specified value is currently selected"""
    return value in self.selected

  select_multiple = True


class _SelectBox:
  """Mixin class providing common methods for SelectBox and MSelectBox"""

  def write(self, req, items, *attribs):
    """Write select box with specified items

    req is a Request object

    items is a sequence of (value, name) tuples to include in the list.

    attribs are extra attributes to add to the html tag in (name, value) tuples

    On the next page load, the "selected" member and is_selected method can
    be used to see which item(s) have been selected.

    The write_open(), write_item(), and write_close() methods can be called as
    an alternative to write(). It may be neccessary to use these in template
    languages where it's not possible to create sequences of tuples for the
    "items" argument, or when you need to write things like <optgroup> tags
    or javascript within the select block."""

    self.write_open(req, *attribs)

    for item in items:
      if isinstance(item, tuple):
        value, name = item
      else:
        value = None
        name = item
      self.write_item(req, value, name)

    self.write_close(req)

  def write_open(self, req, *attribs):
    """Output widget's opening <select> tag"""
    id = self.id()
    _tag(req, "select", ("name", id),
         self.multiple_select and ("multiple", None) or None,
         open=True, *attribs)

  def write_item(self, req, value, name, *attribs):
    """Output an <option> block"""
    _tag(req, "option", value is not None and ("value", value) or None,
         self.is_selected(value) and ("selected", None) or None,
         open=True, *attribs)
    req.write(_html_escape(name))
    _ctag(req, "option")

  def write_close(self, req):
    """Output widget's closing </select> tag"""
    _ctag(req, "select")


class _ClickBox:
  """Mixin class providing common methods for RadioButton and CheckBox"""

  def write(self, req, value, identifer=None, *attribs):
    """Write check box or radio button with the specified value

    In a group of check boxes or radio buttons, this method is meant to be
    called once for each box or button. On the next page load, the "selected"
    member and is_selected() method can be used to see which boxes have been
    selected.

    req is a Request object

    value is the input element's "value=" attribute

    identifier, if not None, is set as the input element's "id=" attribute,
    prefixed with the widget's full_id. This argument is useful when you
    want to make labels for the boxes with <label for="id"> tags.

    attribs are extra attributes to add to <input> tag in (name, value) tuples
    """

    id = self.id()
    _tag(req, "input", ("type", self.input_type), ("name", id),
         identifier is not None and ("id", self.id(identifer)) or None,
         self.is_selected(value) and ("checked", None) or None, *attribs)

  def label_id(self, req, id):
    """Return escaped id for use in a <label for=""> tag"""
    return _escape_html(self.id(id), True)


class RadioButton(_ClickBox, _SingleSelect):
  """Widget for a group of radio buttons

  Members:
    selected
      string value of the current selected button, or None"""
  input_type = "radio"


class CheckBox(_ClickBox, _MultipleSelect):
  """Widget for a group of check boxes

  Members:

    selected
      list of currently checked values"""
  input_type = "checkbox"


class SelectBox(_SelectBox, _SingleSelect):
  """Select Box Widget

  Members:

    selected
       string value of current selected item, or None"""


class MSelectBox(_SelectBox, _MultipleSelect):
  """Select Box Widget allowing multiple select

  Members:

    selected
      list of currently selected values"""


class SubmitButton(FormWidget):
  """Submit Button Widget

  Members:

    clicked
      boolean, True if button was clicked on current page load"""

  def __init__(self, req, parent, id, flags):
    FormWidget.__init__(self, req, parent, id, flags)
    self.clicked = self.read_value(req, None, flags) is not None

  def write_hidden(self, req):
    pass

  def write(self, req, label, *attribs):
    """Write submit button with specified label and attributes

    label is a string specifying button text

    attribs are extra attributes to add to <input> tag in (name, value) tuples
    """
    id = self.id()
    _tag(req, "input", ("type", "submit"), ("name", id), ("value", label),
         *attribs)


class DataButton(FormWidget):
  """Submit button widget that passes data strings with button clicks

  This class is similar to SubmitButton, except that it attaches non-visible
  data strings to buttons that are submitted when they are clicked. This is
  convenient for pages with a lot of buttons because you can see which button
  was clicked by looking at a single data string instead of running over all
  the buttons that might have existed on the previous page and testing each for
  clicks.

  Implementation note: HTML forms submit their elements as pairs of name/value
  strings. For the most part they allow applications to choose arbitrary
  values for those strings which are invisible to users and not displayed
  on pages. Submit buttons are the only exception, they use the value string as
  the label that appears on the button. As a result, the only way to associate
  application data with a button click is to store it in the name. That is what
  this class does. It writes buttons with data strings appended to the widget
  name and at page loading time looks for a GET and POST variables beginning
  with the widget name, setting the "data" member if it finds one

  Members:

    clicked, string with data from last button click, or None if no buttons
    were clicked"""

  def __init__(self, req, parent, id, flags):
    FormWidget.__init__(self, req, parent, id, flags)
    self.clicked = None
    for data in self.enum_values(req, flags):
      self.clicked = data
      break # shouldn't be more than one value, but if there is, keep first

  def write_hidden(self, req):
    pass

  def write(self, req, caption, data, *attribs):
    _tag(req, "input", ("type", "submit"), ("name", self.id(data)),
         ("value", caption), *attribs)

  def write_cb(self, data):
    """Return callable object that performs write with specified data argument
    Useful for passing buttons writes to templates without exposing data"""
    return lambda req, caption, *attrib: \
      self.write(req, caption, data, *attrib)

class ModalWidget(FormWidget):
  """Base class for widgets that show child widgets depending on mode

  Lots of times the functionality you want to implement in a widget, like a
  wizard interface or message editor, can be broken down into several modes
  (or states), making it logical to implement the logic behind the individual
  modes in seperate child widgets which are displayed, one at a time, by the
  main widget. For example, in the case of the wizard interface you might want
  to make the forms displayed on each step of the wizard into seperate widgets.
  A message editor widget might implement a text editor in one child widget, a
  spell checking interface in another child widget, and a file uploading
  interface in a third. The ModalWidget class exists to make it possible to
  write widgets like these with less boilerplate code and with common naming
  conventions. As it coordinates loading and display of form elements over time
  (on different page loads) it's  sort of a logical extension to Form Widgets,
  which coordinate creation of widgets in space (alongside each other on the
  same pages).

  To use ModalWidget functionality, the main, parent widget and the separate
  child widgets which comprise its interface should all inherit from the
  ModalWidget base class. (This symmetry means you can nest modal widgets as
  modes in other modal widgets, so you could make a wizard a mode of a
  message editing interface or vice versa.)

  A ModalWidget parent will create and display ModalWidget children depending
  on what mode or state it's in. For any given mode of the parent, at most one
  child will be displayed (it's write method called). This is called the
  "active" child and each ModalWidget instance has an "active" boolean member
  that indicates whether or not a parent widget should display it on the
  current page load.

  The ModalWidget class doesn't impose much structure on subclasses. In
  particular, it doesn't have any abstract methods for subclasses to implement.
  Instead, it provides methods implementing reasonable-default logic for
  modal widgets that some subclasses will use directly, some will override,
  and some will just completely ignore. The init_children(), write_children(),
  and write_hidden_children() methods it provides implement most of the logic a
  parent needs to manage it's children. And the write_mode(), read_mode(),
  parse_mode(), and mode_str() methods it provides help deal with modes
  represented as lists of strings.

  ModalWidget classes provide the following members:

  "modal_children" - a list of ModalWidget child instances that is
    automatically populated as each instance is constructed

  "active" - boolean, default True. If this is a child widget, indicates
    whether it should be displayed (whether its write method should be called
    instead of write_hidden). At most one child widget should be marked active
    per parent, depending on the mode of the parent.

  "mode" - list of strings, or None. Only present if the read_mode() method
    has been called (and not overridden to do something different). May also
    be something other than a list of strings if the parse_mode() and
    mode_str() methods have been overridden. In any case, it represents the
    mode of a parent widget and determines whether its children will be
    displayed (or created)."""

  def __init__(self, req, parent, id, flags, *args, **kwargs):
    """Initialize modal widget, setting default values for members"""
    FormWidget.__init__(self, req, parent, id, flags)
    self.active = True
    self.modal_children = []
    if isinstance(parent, ModalWidget):
      parent.modal_children.append(self)

  def init_children(self, req, flags):
    """Set up child widgets depending on mode, return True if one is active

    A parent widget should call this method in its __init__ constructor to
    initialize the current mode. It can use a True return value to avoid doing
    unneccessary processing like handling button clicks when a child is active.

    A parent widget can override this method to create child widgets on the fly
    depending on the current mode, calling it wherever it changes the mode, to
    create the corresponding child widget."""
    any_active = False
    for child in self.modal_children:
      if child.active:
        any_active = True
    return any_active

  def write_children(self, req):
    """Write output from child widgets, return True if any is active.

    A parent widget should call this method in its write() method. If there
    is an active child widget, this calls that child's write() method.
    Otherwise this calls childrens' write_hidden() methods."""
    any_active = False
    for child in self.modal_children:
      if child.active:
        child.write(req)
        any_active = True
      else:
        child.write_hidden(req)
    return any_active

  def write_hidden_children(req):
    """Write hidden output from child widgets"""
    for child in self.modal_children:
      self.child.write_hidden(req)

  def write_mode(self, req):
    """Preserve "mode" member using mode_str() to format as a string"""
    self.write_value(req, "mode", self.mode_str(self.mode), WRITE_FORM)

  def read_mode(self, req, flags):
    """Read "mode" member using parse_mode() to parse stored string"""
    self.mode = self.parse_mode(self.read_value(req, "mode", flags))

  def mode_str(self, mode):
    """Format a list of strings as a string

    The different elements of the lists are joined by dots. Dots are escaped
    by backslashes. Backslashes are escaped by backslashes."""
    if mode is not None:
      return ".".join([re.sub(r"([\\\.])", r"\\\1", str(p)) for p in mode])

  def parse_mode(self, str):
    """Parse dot separated mode string formatted by mode_str()

    Will return a list of strings identical to the one passed to mode_str.
    Should handle all lists correctly, including ones with empty members
    and members containing dots and backslashes."""
    if str is not None:
      return [re.sub(r"\\(.)", r"\1", p)
              for p in re.findall(r"((?:[^\\]|\\.)*?)\.", str + ".")]


# Helper functions

def _get_storage(req, flags):
  """Get FieldStorage object for a set LOAD_* flags"""
  if flags & READ_DEFAULT:
    return None
  elif flags & READ_FORM:
    return req.form
  elif flags & READ_URL:
    return req.get
  elif flags & READ_POST:
    return req.post
  else:
    return None

def _join_ids(parent, child=None):
  if child is None:
    return parent
  return "%s.%s" % (parent, child)

def _escape_url(text, space_plus=False):
  if space_plus:
    return urllib.quote_plus(text)
  else:
    return urllib.quote(text, ".")

_escape_html = cgi.escape

def _tag(req, tag, *attribs, **options):
  """Write html tag with attributes

  tag is a string holding the name of the tag

  attribs arguments are 2-tuples, strings or None elements.
  2-tuples are printed as escaped attribute=value pairs, strings are
  printed as is and None elements are ignored.

  options arguments are:

    open
      boolean which causes the tag to be written with closing slash
      (like "<tag />"), if False. Default is False"""

  req.write("<%s" % tag)
  for attrib in attribs:
    if isinstance(attrib, tuple):
      name, value = attrib
      if value is None:
        req.write(" %s" % (name))
      else:
        req.write(' %s="%s"' % (name, _escape_html(str(value), True)))
    elif attrib is not None:
      req.write(" ")
      req.write(attrib)

  if options.get("open"):
    req.write(">")
  else:
    req.write(" />")

def _ctag(req, tag):
  """Write closing tag"""
  req.write("</%s>" % tag)

def _url(req, server=False, info=True, query=False,
         relative=False, raw=False):
  """Return URL of current page in the specified format

  req is a Request object.

  The rest of the arguments are booleans:

  server includes server protocol, name, and port in URL if True.

  info includes extended path (part after script name) in URL if True.
    Ignored when raw=True.

  query includes query string in URL (part starting from ?) if True.
    Ignored when raw=True.

  relative returns a page-relative URL if True. Ignored if server=True
    or raw=True.

  raw uses unparsed URI from first line of HTTP request if True, instead
    of URL components parsed by web server. Implies info=True, query=True
    and relative=False"""

  server_str = path_str = query_str = ""
  if server:
    name = req.server_name()
    port = req.server_port()
    https = req.is_https()
    proto = https and "https" or "http"
    if (not https and port == 80) or (https and port == 443):
      server_str = "%s://%s" % (proto, name)
    else:
      server_str = "%s://%s:%i" % (proto, name, port)

  if raw:
    path_str = req.request_uri()
  else:
    path_str = req.script_name()
    if info:
      path_info = req.path_info()
      path_str = "%s%s" % (path_str, path_info)

    if relative and not server:
      p = path_str.rfind("/")
      if p >= 0:
        path_str = path_str[pos:]

    if query:
      args = req.query_string()
      query_str = "%s%s" % (args and "?", args)

  return "%s%s%s" % (server_str, path_str, query_str)
