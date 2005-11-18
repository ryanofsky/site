import cgi
import sys

class Request:
  """Request object used by widgets to interact with server

  This request object is used in a CGI environent."""

  def __init__(self):
    self.form = cgi.FieldStorage()

    # FieldStorage object can't distinguish between get and put variables
    # just add "get" and "put" members pointing to parent object
    self.form.get = self.form
    self.form.put = self.form

  def write(self, text):
    sys.stdout.write(text)

  def flush(self, text):
    sys.stdout.flush()
