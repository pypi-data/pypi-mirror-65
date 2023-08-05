# Copyright (c) 2020, Varlogix Technologies
# All rights reserved.
# Our terms: https://needle.sh/terms

_e='Error while sending req data'
_d='errors'
_c='platform'
_b='test_mode'
_a='app_id'
_Z='block'
_Y='action'
_X='basic'
_W='modules_used'
_V='path'
_U='django'
_T='api_key'
_S='Error checking command injection'
_R='|'
_Q='os.popen'
_P='os.system'
_O='psycopg2.connect'
_N='mysql.connector.connect'
_M='django.template.loader.render_to_string'
_L='django.core.handlers.base.BaseHandler.get_response'
_K='name'
_J='active'
_I='framework'
_H='type'
_G='value'
_F='cmdi'
_E='xss'
_D=None
_C='sqli'
_B=True
_A=False
import requests,json,time,threading,platform,re,importlib
class RequestData:data=[];remote_addr='';request_method='';http_host='';path_info='';http_user_agent=''
class InstrMethod:sec_module='';py_module='';orig_method=_D;is_instr=_A
class NeedleApp:
	agent_version='0.1';app_id='';api_key='';server_url='';platform='python';framework='';project_dir='';settings={};app_active=_A;errors=[];total_requests=0;mal_requests=[];modules_used=[];test_mode=_A;debug_mode=_A;instr_list=[];is_instr=_A;libinjec=_D;xss_pattern=_D;cmdi_pattern=_D;orig_sql_cursor_execute=_D
	def __init__(A,debug):
		I='='
		if A.detect_framework():A.debug_mode=debug
		else:print('Needle.sh error: Web framework not supported. Stopping agent.');return
		try:
			E=A.project_dir+'/needle_settings.ini'
			with open(E)as F:
				for (J,D) in enumerate(F):
					if D[0]!='#':
						C,B=D.strip().split(I)
						if C==_a:A.app_id=B
						if C==_T:A.api_key=B
						if C=='server_url':A.server_url=B
						if C==_b:
							if B=='0':A.test_mode=_A
							elif B=='1':A.test_mode=_B;print('Needle.sh: Agent in Test Mode...')
						if A.debug_mode:print(C,I,B)
		except Exception as G:H=str(G);A.add_error('Error opening settings INI file',H)
		if A.app_id==''or A.api_key=='':print('Needle.sh error: App ID or API key incorrect. Stopping agent.');return
	def detect_framework(A):
		B=_A
		try:from django.conf import settings as C;A.framework=_U;A.project_dir=C.BASE_DIR;B=_B
		except Exception as D:pass
		return B
	def add_error(A,error,error_data):
		B=error
		if A.debug_mode:print('Adding error: ',B)
		A.errors.append({_c:A.platform,'error':B,'error_data':error_data})
	def add_mal_request(E,action,reason,arg_type,arg_name,arg_value,req_data):D=arg_value;C=arg_name;B=req_data;C,D=E.check_sensitive_data(C,D);A={};A[_H]=action;A['reason']=reason;A['arg_type']=arg_type;A['arg_name']=C;A['arg_value']=D;A['client_ip']=B.remote_addr;A['http_method']=B.request_method;A['server']=B.http_host;A[_V]=B.path_info;A['user_agent']=B.http_user_agent;E.mal_requests.append(A)
	def add_module(A,type,package,method):
		B={_H:type,'package':package,'method':method}
		if not B in A.modules_used:A.modules_used.append(B)
	def api_thread(A):
		B=0;C=0;D=0
		try:
			while _B:
				if B==0:A.api_get_settings()
				if A.app_active and(A.total_requests>0 or len(A.mal_requests)>0):A.api_send_req_data()
				if A.app_active and C==0 and len(A.errors)>0:A.api_send_app_info(_d)
				if A.app_active and D==0 and len(A.modules_used)>0:A.api_send_app_info(_W)
				B+=1;C+=1;D+=1
				if B==1:B=0
				if C==1:C=0
				if D==10:D=0
				time.sleep(60)
		except Exception as E:F=str(E);A.add_error(_e,F)
	def get_api_payload(A):
		B=0
		if A.test_mode:B=1
		C=0
		if A.get_libinjec():C=1
		D={_a:A.app_id,_T:A.api_key,_b:B,'libinjec':C,_c:A.platform,_I:A.framework,'agent_version':A.agent_version};return D
	def api_send_app_info(A,info):
		if A.debug_mode:print('Needle.sh: Sending app info data')
		try:
			C=A.server_url+'/api/store_app_info';B=A.get_api_payload()
			if info==_d and len(A.errors)>0:B['agent_errors']=A.errors;A.errors=[]
			if info==_W and len(A.modules_used)>0:B[_W]=A.modules_used;A.modules_used=[]
			D=json.dumps(B);G=requests.post(C,data=D)
		except Exception as E:F=str(E);A.add_error('Error while sending app info',F)
	def api_send_req_data(A):
		J='total_requests';D='mal_requests'
		if A.debug_mode:print('Needle.sh: Sending requests data')
		try:
			E=A.server_url+'/api/store_requests';B=A.get_api_payload()
			if A.total_requests>0:B[J]=A.total_requests;A.total_requests=0
			if len(A.mal_requests)>0:B[D]=A.mal_requests;A.mal_requests=[]
			F=json.dumps(B);K=requests.post(E,data=F)
		except Exception as G:
			H=str(G);A.add_error(_e,H);A.total_requests+=B[J]
			if len(B[D])>0:C=B[D];I=A.mal_requests;C.extend(I);A.mal_requests=C
	def api_get_settings(A):
		if A.debug_mode:print('Needle.sh: Getting app settings')
		try:
			E=A.server_url+'/api/get_app_settings';F=A.get_api_payload();G=json.dumps(F);D=requests.post(E,data=G)
			if A.debug_mode:print('Needle.sh: Received app settings = ',D.text)
			H=json.loads(D.text);A.settings=H['settings']
		except Exception as B:C=str(B);A.add_error('Error while fetching settings',C)
		try:
			if A.settings[_J]==1:
				A.app_active=_B;A.instrument(_X,_B)
				if _C in A.settings and A.settings[_C][_J]==1:A.instrument(_C,_B)
				else:A.instrument(_C,_A)
				if _E in A.settings and A.settings[_E][_J]==1:A.instrument(_E,_B)
				else:A.instrument(_E,_A)
				if _F in A.settings and A.settings[_F][_J]==1:A.instrument(_F,_B)
				else:A.instrument(_F,_A)
			elif A.settings[_J]==0:A.app_active=_A;A.instrument(_X,_A);A.instrument(_C,_A);A.instrument(_E,_A)
		except Exception as B:C=str(B);A.add_error('Error while instrumenting',C)
	def update_instr_status(B,sec_module,py_module,orig_method,is_instr):
		E=py_module;D=sec_module;C=is_instr;F=_A
		for (H,G) in enumerate(B.instr_list):
			if G.sec_module==D and G.py_module==E:F=_B;B.instr_list[H].is_instr=C;break
		if not F:A=InstrMethod();A.sec_module=D;A.py_module=E;A.orig_method=orig_method;A.is_instr=C;B.instr_list.append(A)
		return C
	def get_module_status(C,py_module):
		A=_A
		for B in C.instr_list:
			if B.py_module==py_module and B.is_instr:A=_B;break
		return A
	def get_orig_method(B,py_module):
		for A in B.instr_list:
			if A.py_module==py_module:return A.orig_method
	def is_module_installed(B,module):A=importlib.find_loader('spam');C=A is not _D
	def instrument(C,sec_module,is_instr):
		L=is_instr;I=sec_module;E='py_module';D='sec_module';M=[{D:_X,_I:_U,E:_L},{D:_E,_I:_U,E:_M},{D:_C,_I:'',E:_N},{D:_C,_I:'',E:_O},{D:_F,_I:'',E:_P},{D:_F,_I:'',E:_Q}]
		for F in M:
			if F[D]!=I:continue
			if F[_I]!=''and F[_I]!=C.framework:continue
			A=F[E]
			if L!=C.get_module_status(A):
				if L:
					try:
						B=''
						if A==_L:
							try:from django.core.handlers.base import BaseHandler as G;B=G.get_response;G.get_response=needle_django_get_response
							except ImportError:pass
						if A==_M:
							try:import django.template.loader;B=django.template.loader.render_to_string;django.template.loader.render_to_string=needle_django_template_render
							except ImportError:pass
						if A==_N:
							try:import mysql.connector;B=mysql.connector.connect;mysql.connector.connect=needle_mysql_connect
							except ImportError:pass
						if A==_O:
							try:import psycopg2 as H;B=H.connect;H.connect=needle_psycopg2_connect
							except ImportError:pass
						if A==_P:
							try:import os;B=os.system;os.system=needle_os_system
							except ImportError:pass
						if A==_Q:
							try:import os;B=os.popen;os.popen=needle_os_popen
							except ImportError:pass
						C.update_instr_status(I,A,B,_B)
					except Exception as J:K=str(J);C.add_error('Error while instrumenting module: '+A,K)
				else:
					try:
						B=''
						if A==_L:
							try:from django.core.handlers.base import BaseHandler as G;B=C.get_orig_method(A);G.get_response=B
							except ImportError:pass
						if A==_M:
							try:import django.template.loader;B=C.get_orig_method(A);django.template.loader.render_to_string=B
							except ImportError:pass
						if A==_N:
							try:import mysql.connector;B=C.get_orig_method(A);mysql.connector.connect=B
							except ImportError:pass
						if A==_O:
							try:import psycopg2 as H;B=C.get_orig_method(A);H.connect=B
							except ImportError:pass
						if A==_P:
							try:import os;B=C.get_orig_method(A);os.system=B
							except ImportError:pass
						if A==_Q:
							try:import os;B=C.get_orig_method(A);os.popen=B
							except ImportError:pass
						C.update_instr_status(I,A,B,_A)
					except Exception as J:K=str(J);C.add_error('Error while un-instrumenting module: '+A,K)
	def get_sec_headers(A):
		H='ref_policy_header';G='mime_sniff_header';F='xss_header';E='cj_header';B={}
		try:
			if A.app_active:
				if E in A.settings:B['X-Frame-Options']=A.settings[E]
				if F in A.settings:B['X-XSS-Protection']=A.settings[F]
				if G in A.settings:B['X-Content-Type-Options']=A.settings[G]
				if H in A.settings:B['Referrer-Policy']=A.settings[H]
		except Exception as C:D=str(C);A.add_error('Error getting security headers: ',D)
		return B
	def xss_module_active(A):
		B=_A;C=''
		try:
			if A.app_active and _E in A.settings and A.settings[_E][_J]==1:B=_B;C=A.settings[_E][_Y]
		except Exception as D:E=str(D);A.add_error('Error checking module active: xss: ',E)
		return B,C
	def cmdi_module_active(A):
		B=_A;C=''
		try:
			if A.app_active and _F in A.settings and A.settings[_F][_J]==1:B=_B;C=A.settings[_F][_Y]
		except Exception as D:E=str(D);A.add_error('Error checking module active: cmdi: ',E)
		return B,C
	def sqli_module_active(A):
		B=_A;C=''
		try:
			if A.app_active and _C in A.settings and A.settings[_C][_J]==1:B=_B;C=A.settings[_C][_Y]
		except Exception as D:E=str(D);A.add_error('Error checking module active: sqli: ',E)
		return B,C
	def get_libinjec(A):
		G='Error getting libinjec module for platform: '
		try:
			if A.libinjec:return A.libinjec
			if not A.libinjec:
				B=_D;C=platform.system()
				if C=='Darwin':from needle_agent.libinjection2.mac_x86_64 import libinjection as D;B=D
				elif C=='Linux':from needle_agent.libinjection2.linux import libinjection as D;B=D
				elif C=='':A.add_error(G,'Unrecognised platform')
				A.libinjec=B;return A.libinjec
		except Exception as E:F=str(E);A.add_error(G,F);return _D
	def get_xss_pattern(B):
		try:
			if B.xss_pattern:return B.xss_pattern
			else:
				import os,sys,inspect as D;E=os.path.dirname(os.path.abspath(D.getfile(D.currentframe())));F=E+'/js_event_list';A=''
				with open(F)as G:
					for (K,C) in enumerate(G):
						C=C.strip()
						if C==''or C[0]=='#':continue
						A+=C+_R
				A=A.rstrip(_R);A='\\b('+A+')\\b';A='(<[\\\\s]*script[\\\\s]*[>]*|javascript:|javascript&colon;|FSCommand)|'+A;H=re.compile(A,re.IGNORECASE);B.xss_pattern=H;return B.xss_pattern
		except Exception as I:J=str(I);B.add_error('Error getting XSS pattern:',J);return _D
	def get_cmdi_pattern(B):
		try:
			if B.cmdi_pattern:return B.cmdi_pattern
			else:
				import os,sys,inspect as D;E=os.path.dirname(os.path.abspath(D.getfile(D.currentframe())));F=E+'/unix_cmd_list';A=''
				with open(F)as G:
					for (K,C) in enumerate(G):
						C=C.strip()
						if C==''or C[0]=='#':continue
						A+=C.rstrip('+')+_R
				A=A.rstrip(_R);A='(^|\\s|;|&&|\\|\\||&|\\|)('+A+')($|\\s|;|&&|\\|\\||&|\\||<)|(\\*|\\?)';H=re.compile(A,re.IGNORECASE);B.cmdi_pattern=H;return B.cmdi_pattern
		except Exception as I:J=str(I);B.add_error('Error getting cmdi pattern:',J);return _D
	def get_project_modules(C):
		try:
			import sys;D=sys.modules.keys();A=[]
			for E in D:
				B=E.split('.')
				if B[0]not in A:A.append(B[0])
		except Exception as F:G=str(F);C.add_error('Error getting module list',G)
	def check_sensitive_data(D,arg_name,arg_value):
		C=arg_name;A=arg_value
		try:
			import re;B='(\\d[ -]*){13,16}';B=re.compile(B,re.IGNORECASE);E=['password','passwd',_T,'apikey','access_token','secret','authorization']
			if len(B.findall(A))>0 or C in E:A='[Sensitive data removed by Needle.sh]'
		except Exception as F:G=str(F);D.add_error('Error while checking sensitive data',G)
		return C,A
needle_app=_D
needle_data=threading.local()
def needle_start(debug=_A):
	print('Starting Needle.sh agent');global needle_app;needle_app=NeedleApp(debug)
	try:A=threading.Thread(target=needle_app.api_thread,args=(),daemon=_B);A.start()
	except Exception as B:C=str(B);needle_app.add_error('Error starting Wally thread to send data',C)
def needle_django_get_response(*A,**G):
	H=_L;global needle_app
	try:
		needle_app.total_requests+=1;B=RequestData();E=[]
		for (C,D) in A[1].GET.items():E.append({_H:'get',_K:C,_G:D})
		for (C,D) in A[1].POST.items():E.append({_H:'post',_K:C,_G:D})
		I=A[1].path.split('/')
		for J in I:E.append({_H:_V,_K:_V,_G:J})
		B.data=E;B.remote_addr=A[1].META['REMOTE_ADDR'];B.request_method=A[1].META['REQUEST_METHOD'];B.http_host=A[1].META['HTTP_HOST'];B.path_info=A[1].META['PATH_INFO'];B.http_user_agent=A[1].META['HTTP_USER_AGENT'];needle_data.req_data=B;F=needle_app.get_orig_method(H)(*A,**G);K=needle_app.get_sec_headers()
		for (N,(C,D)) in enumerate(K.items()):F[C]=D
		return F
	except Exception as L:M=str(L);needle_app.add_error('Error while adding request data to thread storage',M)
def check_content_xss(content):
	M='Error checking XSS:';G=content;global needle_app;B=_A;C='';D='';E=''
	try:
		H=needle_app.get_libinjec()
		for A in needle_data.req_data.data:
			F=A[_G]
			if F=='':continue
			if H:
				J=H.xss(F)
				if J==1:
					if G.find(F)>-1:B=_B;C=A[_H];D=A[_K];E=A[_G];return B,C,D,E
			else:
				I=needle_app.get_xss_pattern()
				if I:
					if len(I.findall(F))>0:
						if G.find(F)>-1:B=_B;C=A[_H];D=A[_K];E=A[_G];return B,C,D,E
				else:needle_app.add_error(M,'XSS pattern unavailable')
	except Exception as K:L=str(K);needle_app.add_error(M,L)
	return B,C,D,E
def needle_django_template_render(*C,**D):
	E=_M;global needle_app
	try:
		needle_app.add_module(_E,'django.template.loader','render_to_string');A=needle_app.get_orig_method(E)(*C,**D);F,B=needle_app.xss_module_active()
		if F:
			G,H,I,J=check_content_xss(A)
			if G:
				if needle_app.debug_mode:print('Needle.sh: New Incident of type: XSS')
				if B==_Z:A=''
				needle_app.add_mal_request(B,_E,H,I,J,needle_data.req_data)
		return A
	except Exception as K:L=str(K);needle_app.add_error('Error checking reflected XSS',L)
def check_command_injection(command):
	C=command;global needle_app;D=_A;E='';F='';G=''
	try:
		H=needle_app.get_cmdi_pattern()
		if H:
			for B in needle_data.req_data.data:
				A=B[_G]
				if A=='':continue
				J=["'",'"','\\','$@']
				for I in J:A=A.replace(I,'');C=C.replace(I,'')
				if A=='':continue
				if len(H.findall(A))>0:
					if C.find(A)>-1:D=_B;E=B[_H];F=B[_K];G=B[_G];return D,E,F,G
		else:needle_app.add_error('Error checking command injection:','Unavailable cmdi pattern')
	except Exception as K:L=str(K);needle_app.add_error(_S,L)
	return D,E,F,G
def needle_cmdi_check(py_module,*A,**D):
	B=py_module;global needle_app;needle_app.add_module(_F,'',B)
	try:
		E,C=needle_app.cmdi_module_active()
		if E:
			F,G,H,I=check_command_injection(A[0])
			if F:
				if needle_app.debug_mode:print('Needle.sh: New Incident of type: Command injection')
				if C==_Z:A='',
				needle_app.add_mal_request(C,_F,G,H,I,needle_data.req_data)
	except Exception as J:K=str(J);needle_app.add_error(_S,K)
	return needle_app.get_orig_method(B)(*A,**D)
def needle_os_system(*A,**B):
	try:C=_P;return needle_cmdi_check(C,*A,**B)
	except Exception as D:E=str(D);needle_app.add_error(_S,E)
def needle_os_popen(*A,**B):
	try:C=_Q;return needle_cmdi_check(C,*A,**B)
	except Exception as D:E=str(D);needle_app.add_error(_S,E)
def check_sql_injection(query):
	global needle_app;B=_A;C='';D='';E=''
	try:
		G=needle_app.get_libinjec()
		for A in needle_data.req_data.data:
			F=A[_G]
			if F=='':continue
			if G:
				H=G.sqli(F,'')
				if H==1:
					if query.find(F)>-1:B=_B;C=A[_H];D=A[_K];E=A[_G];return B,C,D,E
			else:
				I=re.compile('\\b(select|update|insert|alter|create|drop|delete|merge|union|show|exec|or|and|order|sleep|having)\\b|(&&|\\|\\|)',re.IGNORECASE)
				if len(F.split())>1 and len(I.findall(F))>0:B=_B;C=A[_H];D=A[_K];E=A[_G];return B,C,D,E
	except Exception as J:K=str(J);needle_app.add_error('Error checking SQL injection:',K)
	return B,C,D,E
def needle_sql_cursor_execute(*A,**C):
	global needle_app;needle_app.add_module(_C,'mysql.connection.cursor','execute')
	try:
		D,B=needle_app.sqli_module_active()
		if D:
			E,F,G,H=check_sql_injection(A[0])
			if E:
				if needle_app.debug_mode:print('Needle.sh: New Incident of type: SQL injection')
				if B==_Z:A='-- Query blocked by Needle.sh agent (Possible SQL injection)',
				needle_app.add_mal_request(B,_C,F,G,H,needle_data.req_data)
	except Exception as I:J=str(I);needle_app.add_error('Error checking SQL injection',J)
	return needle_app.orig_sql_cursor_execute(*A,**C)
class NeedleSqlCursor:
	def __init__(A,cursor):
		try:A.cursor=cursor;needle_app.orig_sql_cursor_execute=A.cursor.execute;A.execute=needle_sql_cursor_execute
		except Exception as B:C=str(B);needle_app.add_error('Error initialising cursor object:',C)
	def __getattr__(A,name):
		try:return getattr(A.cursor,name)
		except Exception as B:C=str(B);needle_app.add_error('Error returning custom cursor method:',C)
class NeedleSqlConnection:
	def __init__(A,connection):
		try:A.connection=connection
		except Exception as B:C=str(B);needle_app.add_error('Error initialising custom SQL connection object:',C)
	def cursor(A,*B,**C):
		try:D=A.connection.cursor(*B,**C);return NeedleSqlCursor(D)
		except Exception as E:F=str(E);needle_app.add_error('Error getting cursor object from SQL connection:',F)
	def __getattr__(A,name):
		try:return getattr(A.connection,name)
		except Exception as B:C=str(B);needle_app.add_error('Error returning custom connection method:',C)
def needle_mysql_connect(*A,**B):
	C=_N;global needle_app
	try:D=needle_app.get_orig_method(C)(*A,**B);return NeedleSqlConnection(D)
	except Exception as E:F=str(E);needle_app.add_error('Error in instrumented MySQL connect:',F)
def needle_psycopg2_connect(*A,**B):
	C=_O;global needle_app
	try:D=needle_app.get_orig_method(C)(*A,**B);return NeedleSqlConnection(D)
	except Exception as E:F=str(E);needle_app.add_error('Error in instrumented psycopg2 connect:',F)