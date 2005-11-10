import mod_python.util

class Request:
  """Request object used by widgets to interact with server

  This request object is used for Mod_Python. It shouldn't be too hard to write
  similar objects for other environments like CGI or ASP."""

  def __init__(self, req):
    """Initialize request object by wrapping around mp_request instance

    If the mp_request object has a "form" member, it will be used to read form
    variables, otherwise a new FieldStorage instance will be created. This is
    for compatibility with the Publisher handler which sets the "form" member.
    """
    self._req = req

    if hasattr(req, 'form'):
      self.form = req.form
    else:
      self.form = mod_python.util.FieldStorage(req, 0)

    if not hasattr(self.form, 'get') and not hasattr(self.form, 'put'):
      # FieldStorage object doesn't have "get" and "put" members, use a hack
      # to add them for compatibility with older versions of mod_python
      class PartFieldStorage(util.FieldStorage):
        def __init__(self, other, start, end):
          self.list = other.list[start:end]

        get_params = util.parse_qsl(req)

        # hack assumes GET params listed before POST params and in same
        # order as returned by parse_qsl
        for (name, value), field in zip(get_params, self.form.list):
          assert name == field.name

        self.form.get = PartFieldStorage(self.form, None, len(get_params))
        self.form.post = PartFieldStorage(self.form, len(get_params), None)

  def write(self, text):
    self._req.write(text, False)

  def flush(self, text):
    self._req.flush()
