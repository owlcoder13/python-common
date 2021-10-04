from urllib.request import Request, urlopen, ssl, socket
from urllib.error import URLError, HTTPError
import datetime
from dateutil import parser
import OpenSSL

ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

"""
For this library you must exec
    pip install python-dateutil pyOpenSSL 
"""


def get_expire_from_file(file_name):
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, open(file_name).read())
    datetime_struct = parser.parse(cert.get_notAfter().decode("UTF-8"), ignoretz=True)
    return datetime_struct


def ssl_expiry_datetime(host, port=443):
    try:
        context = ssl.create_default_context()
        conn = context.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=host,
        )
        # 3 second timeout because Lambda has runtime limitations
        conn.settimeout(3.0)
        conn.connect((host, port))
        ssl_info = conn.getpeercert()

        # parse the string from the certificate into a Python datetime object
        res = datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
        return res
    except ssl.SSLCertVerificationError:
        return None
