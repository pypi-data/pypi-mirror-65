_E='result'
_D='params'
_C='POST'
_B='%d %r'
_A='utf-8'
import gzip,logging,ssl,json
from typing import Union,Optional
from urllib.error import HTTPError
from urllib.request import Request,urlopen
from enablebanking.eb.platform import Platform,_params_to_pairs,_ApiParam
class BrokerPlatform(Platform):
	def __init__(A,eb_core,origin,cert_path,key_path,ca_cert_path):'\n        Arguments:\n            eb_core -- core module reference\n            origin -- broker origin, e.g. https://localorigin\n            cert_path -- Path to a client tls certificate\n            key_path -- Path to a client tls private key\n            ca_cert_path -- Path to a CA public certificate (shall be the same for the broker)\n        ';super().__init__(eb_core);A.origin=origin;A.cert_path=cert_path;A.key_path=key_path;A.ca_cert_path=ca_cert_path
	def _get_broker_ssl_context(B):A=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT);A.load_cert_chain(B.cert_path,B.key_path);A.verify_mode=ssl.CERT_REQUIRED;A.load_verify_locations(B.ca_cert_path);return A
	def _handle_http_error(C,error):A=error;B=A.fp.read().decode(_A);logging.error(_B,A.status,B);raise HTTPError(A.filename,A.status,f"Broker error: {B}",A.headers,A.fp)
	def makeRequest(B,request,callback):
		M='headers';A=request;H=_params_to_pairs(A.query);D=_params_to_pairs(A.headers);C=None
		if A.tls:
			C={'cert_path':A.tls.certPath,'key_path':A.tls.keyPath}
			if A.tls.caCertPath:C['ca_cert_path']=A.tls.caCertPath
			if A.tls.keyPassword:C['key_password']=A.tls.keyPassword
		I=Request(B.origin+'/makeRequest',method=_C,data=json.dumps({_D:{'request':{'method':A.method,'origin':A.origin,'path':A.path,'query':H,'body':A.body,M:D,'tls':C}}}).encode());J=B._get_broker_ssl_context()
		try:
			with urlopen(I,context=J)as E:K=E.info();logging.info('%r',K.items());G=E.read().decode(_A);logging.debug(_B,E.status,G);F=json.loads(G)[_E];D=[_ApiParam(A,B)for(A,B)in F[M]];callback(B.eb_core.eb_ApiResponse(F['status'],F['response'],D))
		except HTTPError as L:B._handle_http_error(L)
	def signWithKey(A,data,key_id,hash_algorithm=None):
		D=Request(A.origin+'/sign',method=_C,data=json.dumps({_D:{'data':data,'key_id':key_id,'hash_algorithm':hash_algorithm}}).encode());E=A._get_broker_ssl_context()
		try:
			with urlopen(D,context=E)as B:F=B.info();logging.info('%r',F.items());C=B.read().decode(_A);logging.debug(_B,B.status,C);G=json.loads(C)[_E];return G
		except HTTPError as H:A._handle_http_error(H)