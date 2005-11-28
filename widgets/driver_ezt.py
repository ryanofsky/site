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

  def callback(self, callback):
    return callback
