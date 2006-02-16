import ezt

class Template:
  """Template object wrapping EZT template interface

  See widgets.Template docstring for information about the Template class
  interface. See ezt.py module for information about EZT."""

  def __init__(self, string=None, file=None):
    if string is not None:
      assert file is None
      self._ezt = ezt.Template()
      self._ezt.parse(string)
    else:
      assert file is not None
      self._ezt = ezt.Template(file)

  def execute(self, req, dataobj):
    self._ezt.generate(req, dataobj)

  def bind_write(self, write_method, *args, **kwargs):
    """Returns write method bound with arguments as an EZT callback

    Arguments passed to the callback within the template are simply appended
    to the the bound arguments."""
    return lambda ctx, *cargs: write_method(ctx.fp, *(args+cargs), **kwargs)
