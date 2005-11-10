import cgi
import urllib


# flags for Widget.load_state and Widget.load_value
# (see Widget.load_value docstring for descriptions)
LOAD_URL = 1 << 0
LOAD_POST = 1 << 1
LOAD_FORM = LOAD_URL | LOAD_POST


# flags for Widget.write_state and Widget.write_value
# (see Widget.write_value docstring for descriptions)
WRITE_FORM = 1 << 0
WRITE_URL  = 1 << 1


class Form:
  """Class holding common data for all widgets on a form

  Form objects have the following public members:

    name
      string holding value of the form's "name=" attribute. It is used by
      widgets that output javascript accessing form elements.

    url
      string holding a link to the current page without any query parameters.
      It is usually specified as a server-relative URL (i.e. "/dir/page.py")
      or a location-relative URL (i.e. "page.py"). The value could go in a
      form's "action=" attribute. It is also used as the as the base URL
      for links returned by the Form.get_url() method.

    short_names
      dictionary mapping dot-separated widget identifiers to shorter names.
      To allow multiple instances of widgets to coexist on the same page
      without name clashes, the widget framework uses identifiers like
      "widget.childwidget.param" in HTML output to guarantee that each
      widget's identifiers are unique. But sometimes you can guarantee
      that there will only be one instance of a widget on a page. In this case
      you can add short names for the widget identifiers to the dictionary and
      the widget loading and writing code will automatically substitute them,
      resulting in cleaner html output and more user-friendly urls without
      any further changes in the code. The typical place to add to short_names
      is during widget construction where you'll do something like

        self.form.short_names[self.id('item_id')] = 'item_id'

    widgets
      list of top level Widget objects in this form, automatically populated
      by Widget constructors"""

  def __init__(self, name=None, url=None):
    """Create Form object, see class docstring for argument meanings

    name can be set to None on forms with no javascript widgets, but it's a
    good idea to set it whenever you have any widgets in a <form> element, in
    case you decide to add javascript in the future.

    url can be safely set to None when you know none of the widgets on your
    page will call Form.get_url(), but as with the form name it's a good
    idea to set it anyway in case your widgets change in the future."""
    self.name = name
    self.url = url
    self.widgets = []
    self._url_vars = []

  def load_state(self, req):
    """Call load_state on all widgets associated with this form"""
    for widget in self.widget():
      widget.load_state(req, None, LOAD_FORM)

  def get_url(self, url, extra_vars, remove_vars):
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
    in the generated URLs, unless you first call their write_state method with
    the WRITE_URL flag."""
    assert self.url is not None
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


class Widget:
  """Abstract base for Widgets

  Widget instances have the following members:

    identifer
      a base string used by the Widget.id() method to generate unique
      names for page elements associated with the widget.

    form
      instance of Form object this widget is associated with"""

  def __init__(self, identifier, parent):
    """Construct widget and associate with other widgets on the form

      identifer
        a base string which is prepended with the parent widget's identifer
        and used to set the Widget.identifer member

      parent
        parent widget, or Form object if this is a top-level widget

    Widget classes which override this method should be sure to call it
    internally. They should also avoid doing any heavyweight initialization
    such as accessing a database or reading request variables here. That type
    of thing is meant to be done in Widget.load_values."""

    if isinstance(parent, Form):
      self.identifier = identifier
      self.form = parent
    else:
      assert isinstance(parent, ParentWidget)
      self.identifier = _join_ids(parent.identifier, identifier)
      self.form = parent.form

    parent.widgets.append(self)

  def load_state(self, req, is_new, flags=LOAD_FORM):
    """Load widget state, possibly reading from request variables

    req is the request object

    is_new can be True, False, or None. If True it means that the Widget
    has been newly created, and this method should not attempt to read
    any state from request variables. If False, it means that the widget
    was displayed on a previous page load and should read state from the
    request. If None, it means that the caller does not know whether the
    widget is newly-created or not. Widgets with complex initial state
    (like widgets that need to load initial form values from a database) can
    require their callers to provide a True or False values and "assert
    is_new is not None"

    flags values are described in the Widget.load_value() docstring. The most
    common use of the flags argument here is just to forward it to that
    function."""

  def write_state(self, req, flags=WRITE_FORM):
    """Write widget state where it can be read on future page loads

    This function is called to preserve widget state when the widget is NOT
    being displayed on current page. When the widget is being displayed, the
    write method (or whatever other method is called to output the widget
    HTML) is responsible for writing any neccessary state.

    req is the request object

    flags values are described in the Widget.write_value() docstring. The most
    common use of the flags argument here is just to forward it to that
    function."""

  def write(self, req):
    """Write HTML contents of widget to page

      req is the request object

    Unlike other Widget methods meant to be overridden by subclasses
    (like load_state, write_state), this method is not a hook method,
    meaning that it will never be automatically called anywhere in the
    widget framework. Subclasses are therefore free to implement this
    function in varying ways (such as with extra arguments) or not at
    all."""
    raise NotImplementedError

  def id(self, identifer=None):
    """Return Widget identifer or another identifier prefixed with it"""
    long_identifier =  _join_ids(self.identifier, identifer)
    try:
      return self.form.short_ids[long_identifier]
    except KeyError:
      return long_identifier

  def load_value(self, req, identifier, flags):
    """Load value from URL or POST request variables

    req is the request object

    identifier
      string specifying what value to load. This string prefixed with the
      Widget.identifier is the name of the variable that will be looked up

    flags can be a bitwise combination of the following values

      LOAD_URL
        looks up variable in URL query string (i.e. the part after the question
        mark in "page.py?widget.var=value")

      LOAD_POST
        looks up variable in POST data (i.e. a form field submitted in a
        <form "method=post" ...> form)

      LOAD_FORM
        bitwise combination of LOAD_URL and LOAD_POST that finds form field
        values regardless of whether they were submitted in a method="get" or
        a method="post" form.

    If multiple values are found, this function only returns the first one.
    The Widget.load_values method can be used instead of this one to retrieve
    multiple values.

    If no values are found this function returns None"""
    fs = _get_storage(req, flags)
    if fs is not None:
      id = self.id(identifier)
      value = req.get.getfirst(id)
      if value is not None:
        return value
    return None

  def load_values(self, req, identifer, flags):
    """Load values from URL or POST variables

    This function takes the same arguments as Widget.load_value. The only
    difference is that it is a generator that yields ALL the values
    corresponding to an identifer instead of just returning the first value."""
    fs = _get_storage(req, flags)
    if fs is not None:
      id = self.id(identifier)
      for value in fs.getlist(id):
        yield value

  def enum_values(self, req, flags):
    """Enumerate URL or POST variables associated with this widget

      req is the current request object
      flags are described in Widget.load_value docstring

    The return value is the sequence of all the identifier strings that can be
    passed to Widget.load_value and not return None"""

    # This function currently works by doing a linear search through all the
    # request variables, which might not be the most efficient thing to do
    # on pages with a lot of widgets. Multiple calls could be optimized by
    # splitting variable names on the dots and putting them in nested
    # dictionaries organized as a trie. Or a normal character based trie
    # could be used, if such a thing exists for python. But really, this
    # function should never need to be optimized. The only widget that
    # relies on it is ActionButton, and there only ever needs to be one
    # ActionButton loading state per page request.

    fs = _get_storage(req, flags)
    if fs is not None:
      id = self.identifier
      prefix = _join_ids(id, "")
      for field in fs.list:
        if field.name.startswith(prefix):
          yield field.name[len(prefix):]
        elif field.name == id:
          yield None

  def write_value(self, req, identifier, value, flags):
    """Store value so it can be read by the widget on future page loads

    req is the current request object

    identifier is a string that identifies the value, and can be passed
    to Widget.load_value() in future page loads.

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

    id = self.id(identifier)
    if flags & WRITE_FORM:
      _tag(req, 'input', ('type', 'hidden'), ('name', id), ('value', value))

    if flags & WRITE_URL:
      self.form.add_url_var(id, value)


class TextBox(Widget):
  """Text input widget

  Members:

    text
      string containing widget text"""

  def load_state(self, req, is_new, flags):
    if is_new:
      self.text = None
    else:
      self.text = self.load_value(req, None, flags)

  def write_state(self, req, flags):
    if self.text is not None:
      self.write_value(req, None, self.text, flags)

  def write(self, req, rows=0, cols=0, attribs=()):
    """Write input box

    rows
      If nonzero, writes a <textarea> field with the specified number of rows.
      If zero, writes an <input type=text> field

    cols
      width of field, passed as textarea "rows" attribute or text input "size"
      attribute (only if nonzero)

    attribs
      list of extra attributes to add to html tag as (name, value) tuples"""
    id = self.id()
    if rows == 0:
      _tag(req, 'input', ('name', id),
           self.text is not None and ('value', self.text) or None,
           cols and ('size', cols) or None, *attribs)
    else:
      _tag(req, 'textarea', ('name', id), ('rows', rows), ('cols', cols),
           open=True)
      req.write(_escape_html(self.text or ""))
      _ctag(req, 'textarea')

# The CheckBoxes, RadioButtons, SelectBox, and MSelectBox classes have a lot
# of methods in common, so they share implementations through the
# _SingleSelect, _MultipleSelect, and _ClickBox and _SelectBox mixin classes
# below

class _SingleSelect:
  """Mixin class providing common methods for RadioButtons and SelectBox"""
  def load_state(self, req, is_new, flags):
    if is_new:
      self.selected = None
    else:
      self.selected = self.load_values(req, None, flags)

  def write_state(self, req, flags):
    if self.selected is not None:
      self.write_value(req, None, self.selected, flags)

  def is_selected(self, value):
    """Return True if the specified value is currently selected"""
    return self.selected == value

  select_multiple = False

class _MultipleSelect:
  """Mixin class providing common methods for CheckBoxes and MSelectBox"""
  def load_state(self, req, is_new, flags):
    if is_new:
      self.selected = []
    else:
      self.selected = self.load_values(req, None, flags)

  def write_state(self, req, flags):
    for item in self.selected:
      self.write_value(req, None, item, flags)

  def is_selected(self, value):
    """Return True if the specified value is currently selected"""
    return value in self.selected

  select_multiple = True

class _SelectBox:
  """Mixin class providing common methods for SelectBox and MSelectBox"""
  def write(self, req, items, attribs=()):
    """Write check box or radio button with the specified value

    If the box is selected, calls to is_selected(value) on future page
    loads will return true. In a group of check boxes or radio buttons,
    this method is meant to be called once for each box or button.

    req
      request object

    value
      input element's "value=" attribute

    identifier
      if specified this value is set as the input element's "id=" attribute,
      prefixed with the widget identifier. This argument is useful when you
      want to make labels for the boxes with <label for="id"> tags.

    attribs
      list of extra attributes to add to html tag as (name, value) tuples"""

    id = self.id()
    _tag(req, 'select', ('name', id),
         self.multiple_select and ('multiple', None) or None,
         open=True, *attribs)

    for item in items:
      if type(item) is tuple:
        value, name = item
      else:
        name = item
        value = None
      _tag(req, 'option', value is not None and ('value', value) or None,
           self.is_selected(value) and ('selected', None) or None, open=True)
      req.write(_html_escape(name))
      _ctag(req, 'option')
    _ctag(req, 'select')


class _ClickBox:
  """Mixin class providing common methods for RadioButtons and CheckBoxes"""

  def write(self, req, value, identifer=None, attribs=()):
    """Write check box or radio button with the specified value

    If the box is selected, calls to is_selected(value) on future page
    loads will return true. In a group of check boxes or radio buttons,
    this method is meant to be called once for each box or button.

    req
      request object

    value
      input element's "value=" attribute

    identifier
      if specified this value is set as the input element's "id=" attribute,
      prefixed with the widget identifier. This argument is useful when you
      want to make labels for the boxes with <label for="id"> tags.

    attribs
      list of extra attributes to add to html tag as (name, value) tuples"""
    id = self.id()
    _tag(req, 'input', ('type', self.input_type), ('name', id),
         identifier is not None and ('id', self.id(identifer)) or None,
         self.is_selected(value) and ('checked', None) or None, *attribs)


class RadioButtons(_ClickBox, _SingleSelect, Widget):
  """Widget for a group of radio buttons

  Members:
    selected
      string value of the current selected button, or None"""
  input_type = 'radio'


class CheckBoxes(_ClickBox, _MultipleSelect, Widget):
  """Widget for a group of check buttons

  Members:
    selected
      list of currently checked values"""
  input_type = 'checkbox'


class SelectBox(_SelectBox, _SingleSelect, Widget):
  """Select Box Widget

  Members:
    selected
       string value of current selected item, or None"""


class MSelectBox(_SelectBox, _MultipleSelect, Widget):
  """Select Box Widget allowing multiple select

  Members:
    selected
      list of currently selected values"""
  input_type = 'checkbox'


class SubmitButton(Widget):
  """Submit Button Widget

  Members:
    clicked
      boolean, True if button was clicked on current page load"""

  def load_state(self, req, is_new, flags):
    if is_new:
      self.clicked = False
    else:
      self.clicked = self.load_value(req, None, flags) is not None

  def write(self, req, caption, attribs=()):
    """Write submit button with specified caption and attributes

    caption
      string, button text

    attribs
      list of extra attributes to add to html tag as (name, value) tuples"""
    id = self.id()
    _tag(req, 'input', ('type', 'submit'), ('name', id), ('value', caption),
         *attribs)


class ParentWidget(Widget):
  """Abstract base for Widgets which hold other Widgets"""
  def __init__(self, identifier, parent):
    Widget.__init__(self, identifier, parent)
    self.widgets = []

  def load_state(self, req, is_new, flags=LOAD_FORM):
    """Call load_state on child widgets"""
    for widget in self.widgets:
      widget.load_state(req, is_new, flags)

  def write_state(self, req, flags=WRITE_FORM):
    """Call write_state on child widgets"""
    for widget in self.widgets:
      widget.write_state(req, flags)


class Block:
  """Abstract base for classes outputting blocks of HTML

  A Block is like a stripped down Widget. Blocks don't have any facilities
  for reading form data or constructing unique identifiers for page
  elements. The only method a Block class needs to have is a write method
  for outputting its contents to the page."""

  def write(req):
    """Write contents of block to page"""
    raise NotImplementedError


class TemplateBlock:
  """Base class for Blocks that output templates populated with member data"""
  def __init__(self, **args):
    """Default constructor that saves any keyword arguments as members"""
    vars(self).update(args)

  def write(self, req):
    """Write block to request output"""
    self.template.write(req, self)

  def var(self):
    """Return this Block as a variable can be inserted into other templates"""
    return self.template.var(self)

# Helper functions

def _get_storage(req, flags):
  """Get FieldStorage object for a set LOAD_* flags"""
  if flags & LOAD_FORM:
    return req.form
  elif flags & LOAD_URL:
    return req.form.get
  elif flags & LOAD_POST:
    return req.form.post
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

  attribs arguments are list 2-tuples or None elements. None elements are
  ignored and 2-tuples are printed as attribute=value pairs

  options arguents are:

    open
      boolean which causes the tag to be written with closing slash
      (like "<tag />"), if False. Default is False"""

  req.write("<%s" % tag)
  for attrib in attribs:
    if attrib is not None:
      name, value = attrib
      if value is None:
        req.write(' %s' % (name))
      else:
        req.write(' %s="%s"' % (name, _escape_html(str(value), True)))

  if options.get("open"):
    req.write(">")
  else:
    req.write(" />")

def _ctag(req, tag):
  """Write closing tag"""
  req.write("</%s>" % tag)

