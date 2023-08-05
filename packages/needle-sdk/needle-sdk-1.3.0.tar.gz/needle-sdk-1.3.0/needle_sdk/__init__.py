# Copyright (c) 2020, Varlogix Technologies
# All rights reserved.
# Our terms: https://needle.sh/terms

import requests
import json
import time
import threading
import platform
import re

########### Classes ###########

# Class to pass request data
class RequestData:
    data = []
    remote_addr = ''
    request_method = ''
    http_host = ''
    path_info = ''
    http_user_agent = ''
    incident_action = ''
    incident_module = ''
    incident_rule = ''


# Class to keep track of instrumented methods
class InstrMethod:
    sec_module = ''
    py_module = ''
    orig_method = None
    is_instr = False


# Main class
class NeedleApp:
    agent_version = ''
    app_id = ''
    api_key = ''
    server_url = ''
    platform = 'python'
    framework = ''
    project_dir = ''
    settings = {}
    app_active = False
    errors = []
    total_requests = 0
    mal_requests = []
    modules_used = []
    test_mode = False
    debug_mode = False
    instr_list = []
    is_instr = False
    libinjec = None
    sqli_pattern = None
    xss_pattern = None
    cmdi_pattern = None
    mdbi_pattern = None
    scan_pattern = None
    orig_sql_cursor_execute = None
    show_blocked_message = False
    use_libinjec = True # Mark false if libinjection should not be used

    def __init__(self, debug):
        # Check if framework supported
        if self.detect_framework():
            self.debug_mode = debug
        else:
            # Framework not supported, stop execution
            print("Needle.sh error: Web framework not supported. Stopping agent.")
            return

        # Load settings from .ini file
        try:
            filepath = self.project_dir + '/needle.ini'
            with open(filepath) as fp:
                for cnt, line in enumerate(fp):
                    # print("line = " + line)
                    if line[0] != '#':
                        s_name, s_value = line.strip().split('=')
                        if s_name == 'app_id': self.app_id = s_value
                        if s_name == 'api_key': self.api_key = s_value
                        if s_name == 'server_url': self.server_url = s_value
                        if s_name == 'test_mode':
                            if s_value == '0':
                                self.test_mode = False
                            elif s_value == '1':
                                self.test_mode = True
                                print('Needle.sh: Agent in Test Mode...')
                        if self.debug_mode: print(s_name, '=', s_value)
        except Exception as e:
            error_data = str(e)
            self.add_error('Error opening needle.ini file. Please make sure that the file is present in your project\'s '
                           'root folder.', error_data)
            return

        if self.app_id == '' or self.api_key == '':
            print("Needle.sh error: App ID or API key incorrect. Stopping agent.")
            return

    # Detect project framework
    def detect_framework(self):
        detected = False
        # Check for Django framework
        try:
            from django.conf import settings
            self.framework = 'django'
            self.project_dir = settings.BASE_DIR
            detected = True
        except Exception as e:
            pass

        return detected

    # Add error
    def add_error(self, error, error_data):
        if self.debug_mode: print('Needle.sh: Error! ', error)
        self.errors.append({'platform': self.platform, 'error': error, 'error_data': error_data})

    # Add malicious request
    def add_mal_request(self, action, reason, arg_type, arg_name, arg_value, req_data):

        # Check for sensitive data
        arg_name, arg_value = self.check_sensitive_data(arg_name, arg_value)

        mal_req = {}
        mal_req['type'] = action
        mal_req['reason'] = reason
        mal_req['arg_type'] = arg_type
        mal_req['arg_name'] = arg_name
        mal_req['arg_value'] = arg_value
        mal_req['client_ip'] = req_data.remote_addr
        mal_req['http_method'] = req_data.request_method
        mal_req['server'] = req_data.http_host
        mal_req['path'] = req_data.path_info
        mal_req['user_agent'] = req_data.http_user_agent

        if self.debug_mode: print('Needle.sh: Adding incident: ', mal_req)
        self.mal_requests.append(mal_req)

    # Add module
    def add_module(self, type, package, method):
        module = {'type': type, 'package': package, 'method': method}
        if not (module in self.modules_used): self.modules_used.append(module)

    # Call APIs at regular intervals
    def api_thread(self):
        settings_ping_count = 0
        errors_count = 0
        app_info_count = 0

        try:
            while True:
                # Get app settings
                if settings_ping_count == 0:
                    self.api_get_settings()

                # Send total_req data every minute
                if self.app_active and (self.total_requests > 0 or len(self.mal_requests) > 0):
                    self.api_send_req_data()

                # Send agent errors
                if self.app_active and errors_count == 0 and (len(self.errors) > 0):
                    self.api_send_app_info('errors')

                # Send modules used data
                if self.app_active and app_info_count == 0 and (len(self.modules_used) > 0):
                    self.api_send_app_info('modules_used')

                settings_ping_count += 1
                errors_count += 1
                app_info_count += 1

                if settings_ping_count == 1: settings_ping_count = 0
                if errors_count == 1: errors_count = 0
                if app_info_count == 10: app_info_count = 0  # Send frequency = 10 mins

                # Pause for 60 seconds
                time.sleep(30)
        except Exception as e:
            error_data = str(e)
            self.add_error('Error while sending req data', error_data)

    # Get payload for API calls
    def get_api_payload(self):
        test_mode = 0
        if self.test_mode: test_mode = 1
        libinjec = 0
        if self.get_libinjec(): libinjec = 1

        payload = {'app_id': self.app_id, 'api_key': self.api_key, 'test_mode': test_mode, 'libinjec': libinjec,
                   'platform': self.platform, 'framework': self.framework, 'agent_version': self.agent_version}
        return payload

    # Send app info - agent errors, modules used
    def api_send_app_info(self, info):
        if self.debug_mode: print('Needle.sh: Sending app info data')

        try:
            url = self.server_url + '/api/store_app_info'
            data = self.get_api_payload()

            if info == 'errors' and len(self.errors) > 0:
                data['agent_errors'] = self.errors
                self.errors = []  # Todo: restore errors if they are not sent successfully

            if info == 'modules_used' and len(self.modules_used) > 0:
                data['modules_used'] = self.modules_used
                self.modules_used = []  # Todo: restore modules_used if they are not sent successfully

            json_data = json.dumps(data)
            x = requests.post(url, data=json_data)
        except Exception as e:
            error_data = str(e)
            self.add_error('Error while sending app info', error_data)

    # Send requests data - total requests, malicious requests
    def api_send_req_data(self):
        if self.debug_mode: print('Needle.sh: Sending requests data')

        data = {}
        try:
            url = self.server_url + '/api/store_requests'
            data = self.get_api_payload()

            if self.total_requests > 0:
                data['total_requests'] = self.total_requests
                self.total_requests = 0

            if len(self.mal_requests) > 0:
                data['mal_requests'] = self.mal_requests
                self.mal_requests = []

            json_data = json.dumps(data)
            req = requests.post(url, data=json_data)
            # print("----- Wally: Req status code = ", x.status_code)
        except Exception as e:
            error_data = str(e)
            self.add_error('Error while sending req data', error_data)
            # Since requests data could not be sent, save in variable
            # Todo: Make sure that total_req and mal_req dont become too big in size
            self.total_requests += data['total_requests']
            if len(data['mal_requests']) > 0:
                a = data['mal_requests']
                b = self.mal_requests
                a.extend(b)
                self.mal_requests = a

    # Get app settings
    def api_get_settings(self):
        if self.debug_mode: print('Needle.sh: Getting app settings')

        try:
            api_url = self.server_url + '/api/get_app_settings'
            # if self.debug_mode: print('Needle API: get app settings. url = ', api_url)
            data = self.get_api_payload()
            json_data = json.dumps(data)

            req = requests.post(api_url, data=json_data)
            if self.debug_mode: print("Needle.sh: Received app settings = ", req.text)

            resp = json.loads(req.text)
            self.settings = resp['settings']
        except Exception as e:
            error_data = str(e)
            self.add_error('Error while fetching settings', error_data)

        try:
            if self.settings['active'] == 1:
                self.app_active = True
                self.instrument('basic', True)

                if 'sqli' in self.settings and self.settings['sqli']['active'] == 1:
                    self.instrument('sqli', True)
                else:
                    self.instrument('sqli', False)

                if 'xss' in self.settings and self.settings['xss']['active'] == 1:
                    self.instrument('xss', True)
                else:
                    self.instrument('xss', False)

                if 'cmdi' in self.settings and self.settings['cmdi']['active'] == 1:
                    self.instrument('cmdi', True)
                else:
                    self.instrument('cmdi', False)

            elif self.settings['active'] == 0:
                self.app_active = False
                self.instrument('basic', False)
                self.instrument('sqli', False)
                self.instrument('xss', False)
                self.instrument('cmdi', False)
        except Exception as e:
            error_data = str(e)
            self.add_error('Error while instrumenting', error_data)

    # Update instr status for module
    def update_instr_status(self, sec_module, py_module, orig_method, is_instr):
        is_present = False
        for index, obj in enumerate(self.instr_list):
            if obj.sec_module == sec_module and obj.py_module == py_module:
                is_present = True
                self.instr_list[index].is_instr = is_instr
                break

        # If not present, add object with new status
        if not is_present:
            instr_method = InstrMethod()
            instr_method.sec_module = sec_module
            instr_method.py_module = py_module
            instr_method.orig_method = orig_method
            instr_method.is_instr = is_instr
            self.instr_list.append(instr_method)

        return is_instr

    # Get instrumentation status for module
    def get_module_status(self, py_module):
        is_instr = False
        for obj in self.instr_list:
            if obj.py_module == py_module and obj.is_instr:
                is_instr = True
                break

        return is_instr

    # Return original method for instrumented method
    def get_orig_method(self, py_module):
        for obj in self.instr_list:
            if obj.py_module == py_module:
                return obj.orig_method

    # Instrument/Uninstrument methods for security module
    def instrument(self, sec_module, is_instr):
        instr_module_list = [
            {'sec_module': 'basic', 'framework': 'django',
             'py_module': 'django.core.handlers.base.BaseHandler.get_response'},
            {'sec_module': 'xss', 'framework': 'django', 'py_module': 'django.template.loader.render_to_string'},
            {'sec_module': 'sqli', 'framework': '', 'py_module': 'mysql.connector.connect'},
            {'sec_module': 'sqli', 'framework': '', 'py_module': 'psycopg2.connect'},
            {'sec_module': 'cmdi', 'framework': '', 'py_module': 'os.system'},
            {'sec_module': 'cmdi', 'framework': '', 'py_module': 'os.popen'}
        ]

        for mod in instr_module_list:
            if mod['sec_module'] != sec_module: continue
            if mod['framework'] != '' and mod['framework'] != self.framework: continue

            py_module = mod['py_module']

            if is_instr != self.get_module_status(py_module):
                if is_instr:
                    # Instrument module
                    if self.debug_mode: print('Needle.sh: Instrumenting sec module:', py_module)
                    try:
                        orig_method = ''
                        if py_module == 'django.core.handlers.base.BaseHandler.get_response':
                            try:
                                from django.core.handlers.base import BaseHandler
                                orig_method = BaseHandler.get_response
                                BaseHandler.get_response = needle_django_get_response
                            except ImportError:
                                pass

                        if py_module == 'django.template.loader.render_to_string':
                            try:
                                import django.template.loader
                                orig_method = django.template.loader.render_to_string
                                django.template.loader.render_to_string = needle_django_template_render
                            except ImportError:
                                pass

                        if py_module == 'mysql.connector.connect':
                            try:
                                import mysql.connector
                                orig_method = mysql.connector.connect
                                mysql.connector.connect = needle_mysql_connect
                            except ImportError:
                                pass

                        if py_module == 'psycopg2.connect':
                            try:
                                import psycopg2
                                orig_method = psycopg2.connect
                                psycopg2.connect = needle_psycopg2_connect
                            except ImportError:
                                pass

                        if py_module == 'os.system':
                            try:
                                import os
                                orig_method = os.system
                                os.system = needle_os_system
                            except ImportError:
                                pass

                        if py_module == 'os.popen':
                            try:
                                import os
                                orig_method = os.popen
                                os.popen = needle_os_popen
                            except ImportError:
                                pass

                        # Update instr status for py_module
                        self.update_instr_status(sec_module, py_module, orig_method, True)
                    except Exception as e:
                        error_data = str(e)
                        self.add_error('Error while instrumenting module: ' + py_module, error_data)
                else:
                    # Uninstrument module
                    #if self.debug_mode: print('Un-instrumenting sec module:', sec_module)
                    try:
                        orig_method = ''
                        if py_module == 'django.core.handlers.base.BaseHandler.get_response':
                            try:
                                from django.core.handlers.base import BaseHandler
                                orig_method = self.get_orig_method(py_module)
                                BaseHandler.get_response = orig_method
                            except ImportError:
                                pass

                        if py_module == 'django.template.loader.render_to_string':
                            try:
                                import django.template.loader
                                orig_method = self.get_orig_method(py_module)
                                django.template.loader.render_to_string = orig_method
                            except ImportError:
                                pass

                        if py_module == 'mysql.connector.connect':
                            try:
                                import mysql.connector
                                orig_method = self.get_orig_method(py_module)
                                mysql.connector.connect = orig_method
                            except ImportError:
                                pass

                        if py_module == 'psycopg2.connect':
                            try:
                                import psycopg2
                                orig_method = self.get_orig_method(py_module)
                                psycopg2.connect = orig_method
                            except ImportError:
                                pass

                        if py_module == 'os.system':
                            try:
                                import os
                                orig_method = self.get_orig_method(py_module)
                                os.system = orig_method
                            except ImportError:
                                pass

                        if py_module == 'os.popen':
                            try:
                                import os
                                orig_method = self.get_orig_method(py_module)
                                os.popen = orig_method
                            except ImportError:
                                pass

                        # Update instr status for py_module
                        self.update_instr_status(sec_module, py_module, orig_method, False)
                    except Exception as e:
                        error_data = str(e)
                        self.add_error('Error while un-instrumenting module: ' + py_module, error_data)

    # Get security headers to be inserted
    def get_sec_headers(self):
        headers = {}

        try:
            if self.app_active:
                if 'h_cj' in self.settings:
                    headers['X-Frame-Options'] = self.settings['h_cj']

                if 'h_xss' in self.settings:
                    headers['X-XSS-Protection'] = self.settings['h_xss']

                if 'h_mime' in self.settings:
                    headers['X-Content-Type-Options'] = self.settings['h_mime']

                if 'h_ref' in self.settings:
                    headers['Referrer-Policy'] = self.settings['h_ref']
        except Exception as e:
            error_data = str(e)
            self.add_error('Error getting security headers: ', error_data)

        return headers

    # Is XSS security module active?
    def xss_module_active(self):
        active = False
        action = ''

        try:
            if self.app_active and 'xss' in self.settings and self.settings['xss']['active'] == 1:
                active = True
                action = self.settings['xss']['action']
        except Exception as e:
            error_data = str(e)
            self.add_error('Error checking module active: xss: ', error_data)

        return active, action

    # Is Command Injection module active?
    def cmdi_module_active(self):
        active = False
        action = ''

        try:
            if self.app_active and 'cmdi' in self.settings and self.settings['cmdi']['active'] == 1:
                active = True
                action = self.settings['cmdi']['action']
        except Exception as e:
            error_data = str(e)
            self.add_error('Error checking module active: cmdi: ', error_data)

        return active, action

    # Is SQL injection security module active?
    def sqli_module_active(self):
        active = False
        action = ''

        try:
            if self.app_active and 'sqli' in self.settings and self.settings['sqli']['active'] == 1:
                active = True
                action = self.settings['sqli']['action']
        except Exception as e:
            error_data = str(e)
            self.add_error('Error checking module active: sqli: ', error_data)

        return active, action

    # Is security scanner security module active?
    def scan_module_active(self):
        active = False
        action = ''

        try:
            if self.app_active and 'scan' in self.settings and self.settings['scan']['active'] == 1:
                active = True
                action = self.settings['scan']['action']
        except Exception as e:
            error_data = str(e)
            self.add_error('Error checking module active: scan: ', error_data)

        return active, action

    # Get libinjection module
    def get_libinjec(self):

        # Check the use_libinjec setting
        if not self.use_libinjec:
            return None

        try:
            if self.libinjec:
                return self.libinjec
            if not self.libinjec:
                libinjec = None
                op_system = platform.system()
                if op_system == 'Darwin':  # Mac OS
                    from needle_sdk.libinjection2.mac_x86_64 import libinjection
                    libinjec = libinjection
                elif op_system == 'Linux':
                    from needle_sdk.libinjection2.linux import libinjection
                    libinjec = libinjection
                elif op_system == '':
                    self.add_error('Error getting libinjec module for platform: ', 'Unrecognised platform')

                self.libinjec = libinjec
                return self.libinjec
        except Exception as e:
            error_data = str(e)
            self.add_error('Error getting libinjec module for platform: ', error_data)
            return None

    # Get XSS pattern (if libinjec not found)
    def get_xss_pattern(self):
        try:
            if self.xss_pattern:
                return self.xss_pattern
            else:
                import os, sys, inspect
                current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
                filepath = current_dir + '/js_event_list'

                str_pattern = ''
                with open(filepath) as fp:
                    for cnt, line in enumerate(fp):
                        line = line.strip()
                        if line == '' or line[0] == '#': continue

                        str_pattern += line + '|'

                str_pattern = str_pattern.rstrip('|')
                str_pattern = r'\b(' + str_pattern + r')\b'
                str_pattern = r'(<[\\s]*script[\\s]*[>]*|javascript:|javascript&colon;|FSCommand)|' + str_pattern
                pattern = re.compile(str_pattern, re.IGNORECASE)

                self.xss_pattern = pattern
                return self.xss_pattern
        except Exception as e:
            error_data = str(e)
            self.add_error('Error getting XSS pattern:', error_data)
            return None

    # Get sqli pattern
    def get_sqli_pattern(self):
        try:
            if self.sqli_pattern:
                return self.sqli_pattern
            else:
                pattern = re.compile(
                    r'\b(select|update|insert|alter|create|drop|delete|merge|union|show|exec|or|and|order|sleep|having|'
                    r'xor|like|regexp)\b|(&&|\|\|)',
                    re.IGNORECASE)

                self.sqli_pattern = pattern
                return self.sqli_pattern
        except Exception as e:
            error_data = str(e)
            self.add_error('Error getting sqli pattern:', error_data)
            return None

    # Get command injection pattern
    def get_cmdi_pattern(self):
        try:
            if self.cmdi_pattern:
                return self.cmdi_pattern
            else:
                import os, sys, inspect
                current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
                filepath = current_dir + '/unix_cmd_list'

                str_pattern = ''
                with open(filepath) as fp:
                    for cnt, line in enumerate(fp):
                        line = line.strip()
                        if line == '' or line[0] == '#': continue

                        str_pattern += line.rstrip('+') + '|'

                str_pattern = str_pattern.rstrip('|')
                str_pattern = r'(?:;|\{|\||\|\||&|&&|\n|\r|\$\(|\$\(\(|`|\${|<\(|>\(|\(\s*\))\s*' \
                              r'(?:{|\s*\(\s*|\w+=(?:[^\s]*|\$.*|\$.*|<.*|>.*|\'.*\'|\".*\")\s+|!\s*|\$)*\s*(?:\'|\")*' \
                              r'(?:[\?\*\[\]\(\)\-\|+\w\'\"\./\\\\]+\/)?[\\\\\'\"]*'+str_pattern+'\b'

                pattern = re.compile(str_pattern, re.IGNORECASE)

                self.cmdi_pattern = pattern
                return self.cmdi_pattern
        except Exception as e:
            error_data = str(e)
            self.add_error('Error getting cmdi pattern:', error_data)
            return None

    # Get security scanner pattern
    def get_scanner_pattern(self):
        try:
            if self.scan_pattern:
                return self.scan_pattern
            else:
                import os, sys, inspect
                current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
                filepath = current_dir + '/scanners_list'

                str_pattern = ''
                with open(filepath) as fp:
                    for cnt, line in enumerate(fp):
                        line = line.strip()
                        if line == '' or line[0] == '#': continue

                        str_pattern += line.rstrip('+') + '|'

                str_pattern = str_pattern.rstrip('|')
                str_pattern = r'\b(' + str_pattern + r')\b'

                pattern = re.compile(str_pattern, re.IGNORECASE)

                self.scan_pattern = pattern
                return self.scan_pattern
        except Exception as e:
            error_data = str(e)
            self.add_error('Error getting scan pattern:', error_data)
            return None

    # Get project modules
    def get_project_modules(self):
        try:
            import sys
            all_modules = sys.modules.keys()
            # print('All Modules = ', len(all_modules), all_modules)
            module_list = []
            for m in all_modules:
                # Only get parent module name. e.g. If module is mysql.connector, only get mysql
                parts = m.split('.')
                # print(parts[0])
                if parts[0] not in module_list:
                    module_list.append(parts[0])

            # print('Modules = ', len(module_list), module_list)
        except Exception as e:
            error_data = str(e)
            self.add_error('Error getting module list', error_data)

    # Return content for blocked message
    def get_blocked_page_content(self, module_id=''):
        str_content = ''
        if self.show_blocked_message:
            module_name = ''

            if module_id == 'sqli': module_name = 'SQL injection'
            if module_id == 'xss': module_name = 'Cross-site Scripting(XSS)'
            if module_id == 'cmdi': module_name = 'Command injection'
            if module_id == 'scan': module_name = 'Security scanner'

            str_content = 'Blocked by Needle.sh! Attack type: ' + module_name

        return str_content

    # Check if keys have sensitive info
    def check_sensitive_data(self, arg_name, arg_value):
        try:
            # Check if argument value is credit-card info
            import re
            pattern = r'(\d[ -]*){13,16}'
            pattern = re.compile(pattern, re.IGNORECASE)

            # Check for sensitive types of arguments
            sensitive_arg_names = ['password', 'passwd', 'api_key', 'apikey', 'access_token', 'secret', 'authorization']

            if len(pattern.findall(arg_value)) > 0 or arg_name in sensitive_arg_names:
                # Probably credit card info. Don't send to server
                arg_value = '[Sensitive data removed by Needle.sh]'
        except Exception as e:
            error_data = str(e)
            self.add_error('Error while checking sensitive data', error_data)

        return arg_name, arg_value


########### Functions ###########
# Save Request Get/Post params
def needle_django_get_response(*args, **kwargs):
    # print('Inside Needle get_response')

    py_module = 'django.core.handlers.base.BaseHandler.get_response'
    global needle_app

    try:
        needle_app.total_requests += 1

        request_data = RequestData()

        values = []
        for key, value in args[1].GET.items():
            values.append({'type': 'get', 'name': key, 'value': value})

        for key, value in args[1].POST.items():
            values.append({'type': 'post', 'name': key, 'value': value})

        path_args = args[1].path.split('/')
        for p in path_args:
            values.append({'type': 'path', 'name': 'path', 'value': p})

        request_data.data = values

        request_data.remote_addr = args[1].META['REMOTE_ADDR']
        request_data.request_method = args[1].META['REQUEST_METHOD']
        request_data.http_host = args[1].META['HTTP_HOST']
        request_data.path_info = args[1].META['PATH_INFO']
        request_data.http_user_agent = args[1].META['HTTP_USER_AGENT']

        needle_data.req_data = request_data

        # Check for security scanner
        try:
            scan_check, action = needle_app.scan_module_active()
            if scan_check:
                match, arg_type, arg_name, arg_value = check_sec_scanner()
                if match:
                    if needle_app.debug_mode: print('Needle.sh: New Incident of type: Security scanner')

                    # Save request action to thread-data
                    needle_data.req_data.incident_action = action
                    needle_data.req_data.incident_module = 'scan'

                    # Add mal request
                    needle_app.add_mal_request(action, 'scan', arg_type, arg_name, arg_value, needle_data.req_data)

        except Exception as e:
            error_data = str(e)
            needle_app.add_error('Error checking security scanner', error_data)

        # Call original method
        response = needle_app.get_orig_method(py_module)(*args, **kwargs)

        # Insert security related HTTP headers
        sec_headers = needle_app.get_sec_headers()
        for i, (key, value) in enumerate(sec_headers.items()):
            response[key] = value

        return response
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error while adding request data to thread storage', error_data)


# Check for XSS attack
def check_content_xss(content):
    global needle_app
    match = False
    arg_type = ''
    arg_name = ''
    arg_value = ''

    try:
        libinjec = needle_app.get_libinjec()

        for obj in needle_data.req_data.data:
            value = obj['value']
            if value == '': continue

            if libinjec:
                resp = libinjec.xss(value)
                if resp == 1:
                    # Check if content contains arg value
                    if content.find(value) > -1:
                        match = True
                        arg_type = obj['type']
                        arg_name = obj['name']
                        arg_value = obj['value']

                        return match, arg_type, arg_name, arg_value

            # If XSS not detected using libinjec module, use regex
            if needle_app.debug_mode: print('Checking XSS using regex...')
            xss_pattern = needle_app.get_xss_pattern()

            if xss_pattern:
                if len(xss_pattern.findall(value)) > 0:
                    # Check if content contains arg value
                    if content.find(value) > -1:
                        match = True
                        arg_type = obj['type']
                        arg_name = obj['name']
                        arg_value = obj['value']

                        return match, arg_type, arg_name, arg_value
            else:
                needle_app.add_error('Error checking XSS:', 'XSS pattern unavailable')
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking XSS:', error_data)

    return match, arg_type, arg_name, arg_value


# Monkey patch: Render template function
def needle_django_template_render(*args, **kwargs):
    #print('Inside Needle django render...')

    py_module = 'django.template.loader.render_to_string'
    global needle_app

    try:
        # Add module used
        needle_app.add_module('xss', 'django.template.loader', 'render_to_string')

        # Get HTML content
        content = needle_app.get_orig_method(py_module)(*args, **kwargs)

        # Save request action to thread-data
        if needle_data.req_data.incident_action == 'block':
            content = needle_app.get_blocked_page_content(needle_data.req_data.incident_module)
        else:
            # Check for Reflected XSS flag
            xss_check, action = needle_app.xss_module_active()
            if xss_check:
                if needle_app.debug_mode: print('Checking XSS...')

                match, arg_type, arg_name, arg_value = check_content_xss(content)
                if match:
                    if needle_app.debug_mode: print('Needle.sh: New Incident of type: XSS')

                    if action == 'block':
                        # Show blocked message
                        content = needle_app.get_blocked_page_content('xss')

                    # Add mal request
                    needle_app.add_mal_request(action, 'xss', arg_type, arg_name, arg_value, needle_data.req_data)

        # print(">>>>>>>>> Content = ", content)
        return content
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking reflected XSS', error_data)


# Check command injection
def check_command_injection(command):
    global needle_app
    match = False
    arg_type = ''
    arg_name = ''
    arg_value = ''

    try:
        cmdi_pattern = needle_app.get_cmdi_pattern()

        if cmdi_pattern:
            for obj in needle_data.req_data.data:
                value = obj['value']
                if value == '': continue

                remove_chars = ['\'', '"', '\\', '$@', '`', '$(', ')']  # Remove characters that will be ignored by command shell
                for c in remove_chars:
                    value = value.replace(c, '')
                    command = command.replace(c, '')

                if value == '': continue

                if len(cmdi_pattern.findall(value)) > 0:
                    # Check if command contains arg value
                    if command.find(value) > -1:
                        match = True
                        arg_type = obj['type']
                        arg_name = obj['name']
                        arg_value = obj['value']
                        return match, arg_type, arg_name, arg_value
        else:
            needle_app.add_error('Error checking command injection:', 'Unavailable cmdi pattern')

    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking command injection', error_data)

    return match, arg_type, arg_name, arg_value


# Check command injection
def needle_cmdi_check(py_module, *args, **kwargs):
    global needle_app

    # Add module used
    needle_app.add_module('cmdi', '', py_module)

    try:
        cmdi_check, action = needle_app.cmdi_module_active()

        if cmdi_check:
            match, arg_type, arg_name, arg_value = check_command_injection(args[0])

            if match:
                if needle_app.debug_mode: print('Needle.sh: New Incident of type: Command injection')

                if action == 'block':
                    # Replace with blank command
                    args = ('',)

                    # Save request action to thread-data
                    needle_data.req_data.incident_action = 'block'
                    needle_data.req_data.incident_module = 'cmdi'

                # Add mal request
                needle_app.add_mal_request(action, 'cmdi', arg_type, arg_name, arg_value, needle_data.req_data)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking command injection', error_data)

    # Call original function
    return needle_app.get_orig_method(py_module)(*args, **kwargs)


# Instrumented method for os.system
def needle_os_system(*args, **kwargs):
    # print('Inside Needle os.system ->', args, kwargs)

    try:
        py_module = 'os.system'
        return needle_cmdi_check(py_module, *args, **kwargs)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking command injection', error_data)


# Instrumented method for os.popen
def needle_os_popen(*args, **kwargs):
    # print('Inside Needle os.popen ->', args, kwargs)

    try:
        py_module = 'os.popen'
        return needle_cmdi_check(py_module, *args, **kwargs)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking command injection', error_data)


# Check SQL injection
def check_sql_injection(query):
    global needle_app

    match = False
    arg_type = ''
    arg_name = ''
    arg_value = ''

    if needle_app.debug_mode: print('Needle.sh: Checking SQL injection...')

    try:
        libinjec = needle_app.get_libinjec()

        for obj in needle_data.req_data.data:
            value = obj['value']

            if value == '': continue

            if libinjec:
                resp = libinjec.sqli(value, '')
                if resp == 1:
                    # Check if SQL query contains arg value
                    if query.find(value) > -1:
                        match = True
                        arg_type = obj['type']
                        arg_name = obj['name']
                        arg_value = obj['value']

                        # Save request action to thread-data
                        needle_data.req_data.incident_action = 'block'
                        needle_data.req_data.incident_module = 'sqli'
                        needle_data.req_data.incident_rule = 'sqli_1'

                        return match, arg_type, arg_name, arg_value

            # If no sql injection detected with libinjection, use regex
            pattern = needle_app.get_sqli_pattern()

            if len(value.split()) > 1 and len(pattern.findall(value)) > 0:
                match = True
                arg_type = obj['type']
                arg_name = obj['name']
                arg_value = obj['value']

                # Save request action to thread-data
                needle_data.req_data.incident_action = 'block'
                needle_data.req_data.incident_module = 'sqli'
                needle_data.req_data.incident_rule = 'sqli_2'

                return match, arg_type, arg_name, arg_value

    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking SQL injection:', error_data)

    return match, arg_type, arg_name, arg_value


# Instrumented function for mysql.connection.cursor.execute
def needle_sql_cursor_execute(*args, **kwargs):
    # print('Inside Needle MySQL execute ...')

    global needle_app
    # Add module used
    needle_app.add_module('sqli', 'mysql.connection.cursor', 'execute')

    try:
        # Check for SQL injection
        sqli_check, action = needle_app.sqli_module_active()
        if sqli_check:
            match, arg_type, arg_name, arg_value = check_sql_injection(args[0])
            if match:
                if needle_app.debug_mode: print('Needle.sh: New Incident of type: SQL injection')

                if action == 'block':
                    # Change query to blank query
                    args = ('-- Query blocked by Needle.sh agent (Possible SQL injection)',)

                # Add mal request
                needle_app.add_mal_request(action, 'sqli', arg_type, arg_name, arg_value, needle_data.req_data)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking SQL injection', error_data)

    return needle_app.orig_sql_cursor_execute(*args, **kwargs)


# Wrapper class around mysql.connection.cursor
class NeedleSqlCursor():
    def __init__(self, cursor):
        try:
            self.cursor = cursor
            # self.execute = patcher(self.cursor.execute)
            needle_app.orig_sql_cursor_execute = self.cursor.execute
            self.execute = needle_sql_cursor_execute
        except Exception as e:
            error_data = str(e)
            needle_app.add_error('Error initialising cursor object:', error_data)

    def __getattr__(self, name):
        try:
            return getattr(self.cursor, name)
        except Exception as e:
            error_data = str(e)
            needle_app.add_error('Error returning custom cursor method:', error_data)


# Wrapper class around mysql.connection
class NeedleSqlConnection():
    def __init__(self, connection):
        try:
            self.connection = connection
        except Exception as e:
            error_data = str(e)
            needle_app.add_error('Error initialising custom SQL connection object:', error_data)

    def cursor(self, *args, **kwargs):
        try:
            orig_cursor = self.connection.cursor(*args, **kwargs)
            return NeedleSqlCursor(orig_cursor)
        except Exception as e:
            error_data = str(e)
            needle_app.add_error('Error getting cursor object from SQL connection:', error_data)

    # Handle unknown method calls
    def __getattr__(self, name):
        try:
            return getattr(self.connection, name)
        except Exception as e:
            error_data = str(e)
            needle_app.add_error('Error returning custom connection method:', error_data)


# Instrumented function for MySQL connect
def needle_mysql_connect(*args, **kwargs):
    # print("--- Inside Needle MySQL connect: Args = ", args, kwargs)
    py_module = 'mysql.connector.connect'
    global needle_app

    try:
        # conn = needle_app.orig_mysql_connect(*args, **kwargs)
        conn = needle_app.get_orig_method(py_module)(*args, **kwargs)
        return NeedleSqlConnection(conn)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error in instrumented MySQL connect:', error_data)


# Instrumented function for MySQL connect
def needle_psycopg2_connect(*args, **kwargs):
    # print("--- Inside Needle Postgres connect: Args = ", args, kwargs)
    py_module = 'psycopg2.connect'
    global needle_app

    try:
        # conn = needle_app.orig_mysql_connect(*args, **kwargs)
        conn = needle_app.get_orig_method(py_module)(*args, **kwargs)
        return NeedleSqlConnection(conn)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error in instrumented psycopg2 connect:', error_data)


# Check security scanner
def check_sec_scanner():
    global needle_app

    match = False
    arg_type = ''
    arg_name = ''
    arg_value = ''

    if needle_app.debug_mode: print('Needle.sh: Checking security scanner...')

    try:
        scan_pattern = needle_app.get_scanner_pattern()
        if not scan_pattern: return match, arg_type, arg_name, arg_value

        value = needle_data.req_data.http_user_agent

        if value == '': return match, arg_type, arg_name, arg_value

        if len(scan_pattern.findall(value)) > 0:
            match = True
            arg_type = 'http_header'
            arg_name = 'user_agent'
            arg_value = value

            return match, arg_type, arg_name, arg_value

    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking security scanner:', error_data)

    return match, arg_type, arg_name, arg_value


# Start the SDK
def start(debug=False, show_blocked_message=False):
    print("Needle.sh: Starting SDK (version " + g_sdk_version + ")")

    global needle_app
    needle_app = NeedleApp(debug)
    needle_app.agent_version = g_sdk_version
    needle_app.show_blocked_message = show_blocked_message

    try:
        # Start thread to send data to Wally server
        x = threading.Thread(target=needle_app.api_thread, args=(), daemon=True)
        x.start()
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error starting Wally thread to send data', error_data)


########### Globals ###########
needle_app = None
needle_data = threading.local()
g_sdk_version = '1.3.0'
