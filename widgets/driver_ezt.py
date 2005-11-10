import ezt

class Template:
  """Template object wrapping up EZT template interface"""
  def __init__(self, template):
    self._ezt = ezt.Template()
    self._ezt.parse(template)

  def write(self, req, data):
    self._ezt.generate(req, data)

  def var(self, data):
    def callback(req):
      self._ezt.generate(req, data)
    return callback
