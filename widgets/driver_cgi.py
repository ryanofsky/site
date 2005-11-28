import cgi
import os
import sys

class Request:
  """Request object wrapping CGI server interface

  See widgets.Request docstring for information about the Request class
  interface"""

  def __init__(self):
    self.form = cgi.FieldStorage()

    # FieldStorage object can't distinguish between get and put variables
    # just add "get" and "put" members pointing to parent object
    self.get = self.form
    self.put = self.form

  def write(self, text):
    sys.stdout.write(text)

  def flush(self, text):
    sys.stdout.flush()

  def server_name(self):
    return os.environ.get("SERVER_NAME")

  def server_port(self):
    return int(os.environ.get("SERVER_PORT", 0))

  def is_https(self):
    return os.environ.get("HTTPS") == "on"

  def request_uri(self):
    return os.environ.get("REQUEST_URI")

  def script_name(self):
    return os.environ.get("SCRIPT_NAME")

  def path_info(self):
    return os.environ.get("PATH_INFO", "")

  def query_string(self):
    return os.environ.get("QUERY_STRING")
