_C='SHA256'
_B=False
_A=None
import base64,gzip,logging,ssl,uuid
from collections import namedtuple
from datetime import datetime
from typing import Optional
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request,urlopen
from cryptography.exceptions import InvalidSignature
from cryptography.utils import int_to_bytes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec,padding
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from cryptography.hazmat.backends.openssl.rsa import _RSAPrivateKey,_RSAPublicKey
from cryptography.hazmat.backends.openssl.ec import _EllipticCurvePrivateKey
def _params_to_pairs(params):A=params;return[(B.name,B.value)for B in A]if A else[]
_ApiParam=namedtuple('_ApiParam',('name','value'))
class SafeString(str):
	def title(A):return A
	def capitalize(A):return A
class Platform:
	def __init__(A,eb_core):A.eb_core=eb_core
	def makeRequest(K,request,callback):
		R='%d %r';Q='gzip';P='content-encoding';L=callback;J='utf-8';A=request;H=A.origin+A.path;M=urlencode(_params_to_pairs(A.query));N=A.body.encode();B=dict(((SafeString(B),C)for(B,C)in _params_to_pairs(A.headers)));B['User-Agent']='python-requests/2.22.0'
		if M:H+='?'+M
		logging.debug('Request(%r, %r, headers=%r, method=%r',H,N,B,A.method);O=Request(H,data=N,headers=B,method=A.method);D=_A
		if A.tls:D=ssl.create_default_context();D.check_hostname=_B;D.verify_mode=ssl.CERT_NONE;D.load_cert_chain(A.tls.certPath,A.tls.keyPath,lambda:A.tls.keyPassword)
		else:D=ssl._create_unverified_context()
		try:
			with urlopen(O,context=D)as F:
				I=F.info();logging.info('%r',I.items());G=I.get(P,_A)
				if G and G.lower()==Q:C=gzip.decompress(F.read()).decode(J)
				else:C=F.read().decode(J)
				logging.debug(R,F.status,C);B=[_ApiParam(A,B)for(A,B)in I.items()];L(K.eb_core.eb_ApiResponse(F.status,C,B))
		except HTTPError as E:
			G=E.headers[P]
			if G and G.lower()==Q:C=gzip.decompress(E.fp.read()).decode(J)
			else:C=E.fp.read().decode(J)
			logging.error(R,E.status,C);B=[_ApiParam(A,B)for(A,B)in E.headers.items()];L(K.eb_core.eb_ApiResponse(E.status,C,B))
	def genUUID(A):return str(uuid.uuid1())
	def getRequestId(A,endpoint):"Generate unique ID which is intended to be used as a correlation id\n\n        Keyword Arguments:\n            endpoint {str} -- Bank's API endpoint which the request will be sent to (default: {None})\n\n        Returns:\n            str -- UUID.\n                   If you don't want to set a request-id, just return None instead.\n                   Note that this parameter is required for some banks and None is not allowed there.\n        ";return A.genUUID()
	def getTimestamp(B,utc=_B):
		if utc:A=datetime.utcnow()
		else:A=datetime.now()
		return int(A.timestamp())
	def getCurrentDateTime(B,format,utc=_B):
		'Get current DateTime string according to passed format\n\n        Arguments:\n            format {str} -- date format according to strftime\n\n        Keyword Arguments:\n            utc {bool} -- If DateTime needs to be in UTC (default: {False})\n\n        Returns:\n            str -- current DateTime string\n        '
		if utc:A=datetime.utcnow()
		else:A=datetime.now()
		return A.strftime(format)
	def _prepare_public_key(E,cert_path):
		'Create a key object out of public .pem certificate\n\n        Arguments:\n            cert_path {str} -- Path to a public key\n\n        Returns:\n            _RSAPublicKey -- Private key class instance\n        ';A=default_backend();B=open(cert_path,'rb').read()
		try:C=A.load_pem_public_key(B)
		except ValueError:D=A.load_pem_x509_certificate(B);C=D.public_key()
		return C
	@staticmethod
	def _decode_signature(signature,hash_algorithm):
		A=hash_algorithm;B={_C:256}
		try:D=B[A]
		except KeyError:raise ValueError(f"Wrong hash algorithm: {A}. Allowed: {list(B.keys())}")
		C=(D+7)//8;E,F=decode_dss_signature(signature);return int_to_bytes(E,C)+int_to_bytes(F,C)
	@staticmethod
	def _get_hash_algorithm(hash_algorithm):
		A=hash_algorithm;A=A.upper();B={_C:hashes.SHA256}
		try:return B[A]()
		except AttributeError:raise AttributeError(f"Wrong hash algorithm: {A}. Allowed: {list(B.keys())}")
	@staticmethod
	def _base64_add_padding(data):return data+'='*((4-len(data)%4)%4)
	def signWithKey(D,data,key_path,hash_algorithm=_A):
		'Sign passed data with private key\n\n        Arguments:\n            data {String} -- Data to be signed\n            key_path {String} -- Path to a file with a private key\n            hash_algorithm {String} -- Hash algorithm to use.\n                                       If not provided then `sha256` will be used\n\n        Returns:\n            String -- Base64 encoded signed with a private key string\n        ';B=hash_algorithm
		if B is _A:B=_C
		E=D._get_hash_algorithm(B);F=data.encode();G=default_backend();C=G.load_pem_private_key(open(key_path,'rb').read(),_A);A=b''
		if isinstance(C,_RSAPrivateKey):A=C.sign(F,padding.PKCS1v15(),E)
		elif isinstance(C,_EllipticCurvePrivateKey):A=C.sign(F,ec.ECDSA(E));A=D._decode_signature(A,B)
		return base64.b64encode(A).decode('utf8')
	def verifySignature(A,signature,message,cert_path,hash_algorithm=_A):
		'Verify passed signature with a public key\n\n        Arguments:\n            signature {str} -- Base64 urlsafe encoded signature to verify\n            message {str} -- Message to verify against\n            cert_path {str} -- Path to a public certificate to use for verification\n\n        Returns:\n            bool -- Shows if signature is valid\n        ';B=hash_algorithm
		if B is _A:B=_C
		C=A._get_hash_algorithm(B);D=base64.urlsafe_b64decode(A._base64_add_padding(signature).encode());E=message.encode();F=A._prepare_public_key(cert_path)
		try:F.verify(D,E,padding.PKCS1v15(),C)
		except InvalidSignature:return _B
		return True
	def getDateTimeWithOffset(D,offset,format,utc=_B):
		'Return DateTime with `offset` in seconds from current DateTime according to `format`\n\n        Arguments:\n            offset {Integer} -- Offset in seconds from current datetime\n            format {String} -- strftime format\n            utc {Bool} -- Shows if the returned value in utc\n\n        Returns:\n            String -- DateTime string according to a passed format\n        ';C=int(datetime.now().timestamp());A=C+offset
		if utc:B=datetime.utcfromtimestamp(A)
		else:B=datetime.fromtimestamp(A)
		return B.strftime(format)