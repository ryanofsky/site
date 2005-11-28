import mod_python.util

class Request:
  """Request object wrapping Mod_Python server interface

  See widgets.Request docstring for information about the Request class
  interface"""

  def __init__(self, req):
    """Initialize request object by wrapping around mp_request object

    If the mp_request object has a "form" member, it will be used to read form
    variables, otherwise a new FieldStorage instance will be created. This is
    for compatibility with the Publisher handler which sets the "form" member.
    """
    self._req = req

    if hasattr(req, 'form'):
      self.form = req.form
    else:
      self.form = mod_python.util.FieldStorage(req, 0)

    if hasattr(self.form, 'get') and hasattr(self.form, 'put'):
      self.get = self.form.get
      self.put = self.form.put

    else:
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

        self.get = PartFieldStorage(self.form, None, len(get_params))
        self.post = PartFieldStorage(self.form, len(get_params), None)

  def write(self, text):
    self._req.write(text, False)

  def flush(self, text):
    self._req.flush()

  def server_name(self):
    return self._req.hostname

  def server_port(self):
    return self._req.connection.local_addr[1]

  def is_https(self):
    ### need to find correct value
    return False

  def request_uri(self):
    return self._req.unparsed_uri

  def script_name(self):
    return self._req.uri

  def path_info(self):
    return self._req.path_info

  def query_string(self):
    return self._req.args
