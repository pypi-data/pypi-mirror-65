"""SDK classes"""
import json
import requests

class WialonSdk:
  """Sdk handler"""

  def __init__(self, is_development=False, scheme='https', host='hst-api.wialon.com', port=0,
                     session_id='', extra_params=None):
    """Method missing handler"""
    self.is_development = is_development
    self.session_id = session_id
    self.scheme = scheme
    self.default_params = {}

    if extra_params is not None:
      self.default_params.update(extra_params)

    self.host = host

    parsed_port = ""

    port = int(port)

    if port < 0:
      raise SdkException(message='Invalid port, must be greater than 0')

    if port > 0:
      self.base_url = f'{scheme}://{host}:{port}'
    else:
      self.base_url = f'{scheme}://{host}'

    self.base_url += '/wialon/ajax.html?'

    self.user_id = ''

  def call(self, method, args):
    """Call method"""
    svc = None

    if method == 'unit_group_update_units':
      svc = 'unit_group/update_units'
    else:
      svc = str(method).replace("_", "/", 1)

    arguments = {}
    arguments.update(self.default_params)

    if isinstance(args, list):
      arguments = args
    else:
      arguments.update(args)

    try:
      parameters = json.dumps(arguments)
    except Exception as e:
      raise SdkException(f'Internal error: {e}')

    parameters = {
      'svc': svc,
      'params': parameters,
      'sid': self.session_id
    }

    if self.is_development:
      self._debug_printer(content=f'Method: {parameters["svc"]}\nParameters: {parameters}\n'\
                          + f'URL: {self.base_url}svc={parameters["svc"]}'\
                          + f'&params={parameters["params"]}&sid={parameters["sid"]}')

    try:
      request = requests.post(url=self.base_url, params=parameters)
    except Exception as e:
      raise SdkException(f'Internal error: {e}')

    try:
      response = request.json()
    except Exception as e:
      raise SdkException(f'Internal error: {e}')

    if 'error' in response and response['error'] != 0:
      reason = ''
      if 'reason' in response:
        reason = response["reason"]

      raise WialonError(code=response['error'], reason=reason)

    return response

  def login(self, token):
    """Login shortcut method"""
    result = self.token_login({'token': token})

    self.user_id = result['user']['id']
    self.session_id = result['eid']

    return result

  def logout(self):
    """Logout shortcut method"""
    self.core_logout()

  def reverse_geocoding(self, latitude, longitude, flags=1255211008):
    """Reverse geocoding service"""

    coordinates = json.dumps({
      'lon': longitude,
      'lat': latitude
    })

    url = f'https://geocode-maps.wialon.com/{self.host}/gis_geocode?'\
        + f'coords=[{coordinates}]&flags={flags}&uid={self.user_id}'

    if self.is_development:
      self._debug_printer(content=f'Method: Reverse geocoding service\nURL: {url}')

    try:
      request = requests.post(url=url)
      response = request.json()

      return response[0]
    except Exception as e: #pylint: disable=W0706
      raise SdkException(message=f'Internal error: {e}')

  def _debug_printer(self, content):
    """Debug printer"""
    print('*******' * 10)
    print(content)
    print('*******' * 10)

  def __getattr__(self, name):
    """Method missing handler"""

    def method(*args):
      """Handler"""
      arguments = {}

      if len(args) > 0:
        arguments = args[0]

      return self.call(name, arguments)

    return method

class SdkException(Exception):
  """Sdk general exceptions"""
  _message = ''

  def __init__(self, message='Exception'):
    """Constructor"""
    self._message = message
    super().__init__()

  def _readable(self):
    """Readable property"""
    return f'SdkException(message: {self._message})'

  def __str__(self):
    """Readable property"""
    return self._readable()

  def __repr__(self):
    """Readable property"""
    return self._readable()

class WialonError(Exception):
  """Error handler class"""

  _errors = {
    '-1': 'Unhandled error code',
    '1': 'Invalid session',
    '2': 'Invalid service name',
    '3': 'Invalid result',
    '4': 'Invalid input',
    '5': 'Error performing request',
    '6': 'Unknown error',
    '7': 'Access denied',
    '8': 'Invalid user name or password',
    '9': 'Authorization server is unavailable',
    '10': 'Reached limit of concurrent requests',
    '11': 'Password reset error',
    '14': 'Billing error',
    '1001': 'No messages for selected interval',
    '1002': 'Item with such unique property already exists or Item'\
          + 'cannot be created according to billing restrictions',
    '1003': 'Only one request is allowed at the moment',
    '1004': 'Limit of messages has been exceeded',
    '1005': 'Execution time has exceeded the limit',
    '1006': 'Exceeding the limit of attempts to enter a two-factor authorization code',
    '1011': 'Your IP has changed or session has expired',
    '2014': 'Selected user is a creator for some system objects, thus this user cannot'\
          + 'be bound to a new account',
    '2015': 'Sensor deleting is forbidden because of using in another sensor or advanced'\
          + 'properties of the unit'
  }

  _reason = ''

  def __init__(self, code, reason):
    """Constructor"""
    print('Error code: ', code)
    if str(code) not in self._errors:
      self._reason = self._errors['-1']
    else:
      self._reason = self._errors[str(code)]

    if len(reason) > 0:
      self._reason += f' - {reason}'

    super().__init__()

  def _readable(self):
    """Readable property"""
    return f'WialonError(code: {self._code}, reason: {self._reason})'

  def __str__(self):
    """Readable property"""
    return self._readable()

  def __repr__(self):
    """Readable property"""
    return self._readable()
