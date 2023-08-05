"""
// ========================================================================
// Copyright (c) 2018-2019 Iotium, Inc.
// ------------------------------------------------------------------------
// All rights reserved.
//
// ========================================================================
"""

__author__ = "Rashtrapathy"
__copyright__ = "Copyright (c) 2018-2019 by Iotium, Inc."
__license__ = "All rights reserved."
__email__ = "rashtrapathy.c@iotium.io"

from iotiumlib.requires.commonWrapper import *
from iotiumlib.requires.resourcePayload import *

userId = str()
subId = str()

class user(object):
    def __init__(self, action, payload=None, filters=None, user_id=None):

        if payload is None:
            payload = {}

        def getv2_user(uri):
            return user.User(self, method='getv2', uri=uri, filters=filters)

        def add_user(uri):
            return user.User(self, method='post', uri=uri)

        def edit_user(uri):
            return user.User(self, method='put', uri=uri)

        def delete_user(uri):
            return user.User(self, method='delete', uri=uri)

        def notifications_user(uri):
            return user.Notifications(self, method='notifications', uri=uri, filters=filters)

        _function_mapping = {
            'getv2': getv2_user,
            'add' : add_user,
            'edit' : edit_user,
            'delete':delete_user,
            'notifications': notifications_user
        }

        self.uri = {
            getv2_user: 'api/v2/user',
            add_user: 'api/v1/user',
            edit_user: 'api/v1/user/{userId}',
            delete_user: 'api/v1/user/{userId}',
            notifications_user: 'api/v2/notification'
        }

        self.payload = resourcePaylod.User(payload).__dict__

        self.userId = user_id

        self.Response = Response()

        _wrapper_fun = _function_mapping[action]
        args = '{}_user'.format(action)
        _wrapper_fun(self.uri[eval(args)])

    def User(self, method, uri, filters=None):

        respOp = dict()
        paramRequired = checkforUriParam(uri)
        if paramRequired:
            for param in paramRequired:
                uri = re.sub(r'{{{}}}'.format(param), eval('self.{}'.format(param)), uri)

        if method == 'get':
            respOp = getApi(formUri(uri))
        elif method == 'getv2':
            self.Response = getApiv2(formUri(uri), filters)
            return self.Response
        elif method == 'post':
            respOp = postApi(formUri(uri), self.payload)
        elif method == 'put':
            respOp = putApi(formUri(uri), self.payload)
        elif method == 'delete':
            respOp = deleteApi(formUri(uri))
        else:
            return self.Response
        self.Response.output = respOp.json()
        self.Response.code = respOp.status_code
        return self.Response

    def Notifications(self, method, uri, filters=None):
        paramRequired = checkforUriParam(uri)
        if paramRequired:
            for param in paramRequired:
                uri = re.sub(r'{{{}}}'.format(param), eval('self.{}'.format(param)), uri)
        if method == 'notifications':
            self.Response = getApiv2(formUri(uri), filters)
            return self.Response
        else:
            return self.Response

    @staticmethod
    def add(name, email, password, role_id, org_id=None, timezone=None):
        return user(action='add', payload=locals())

    @staticmethod
    def edit(user_id, name=None, role_id=None):
        return user(action='edit', payload=locals(), user_id=user_id)

    @staticmethod
    def delete(user_id):
        return user(action='delete', user_id=user_id)

    @staticmethod
    def getv2(filters=None):
        return user(action='getv2', filters=filters)

    @staticmethod
    def notifications(org_id=None, node_id=None, type=None, filters=None):

        if filters is None:
            filters = dict()

        if org_id:
            filters.update({"org_id": org_id})

        if node_id:
            filters.update({"node_id": node_id})

        if type:
            filters.update({'type': type})

        return user(action="notifications", filters=filters)

    def __del__(self):
        self.payload = dict()
        self.Response = Response()

    class mysubscriptions(object):
        def __init__(self, action, payload=None, filters=None, sub_id=None):

            if payload is None:
                payload = {}

            def add_sub(uri):
                return user.mysubscriptions.MySub(self, method='post', uri=uri)

            def getv2_sub(uri):
                return user.mysubscriptions.MySub(self, method='getv2', uri=uri, filters=filters)

            def delete_sub(uri):
                return user.mysubscriptions.MySub(self, method='delete', uri=uri)

            _function_mapping = {
                'getv2': getv2_sub,
                'add' : add_sub,
                'delete':delete_sub,
            }

            self.uri = {
                getv2_sub: 'api/v2/mysubscriptions',
                add_sub: 'api/v1/mysubscriptions',
                delete_sub: 'api/v1/mysubscriptions/{subId}',
            }

            self.payload = resourcePaylod.Subscriptions(payload).__dict__

            self.subId = sub_id

            self.Response = Response()

            _wrapper_fun = _function_mapping[action]
            args = '{}_sub'.format(action)
            _wrapper_fun(self.uri[eval(args)])

        def MySub(self, method, uri, filters=None):
            respOp = dict()
            paramRequired = checkforUriParam(uri)
            if paramRequired:
                for param in paramRequired:
                    uri = re.sub(r'{{{}}}'.format(param), eval('self.{}'.format(param)), uri)
            if method == 'notifications':
                self.Response = getApiv2(formUri(uri), filters)
                return self.Response

            if method == 'getv2':
                self.Response = getApiv2(formUri(uri), filters)
                return self.Response
            elif method == 'post':
                respOp = postApi(formUri(uri), self.payload)
            elif method == 'delete':
                respOp = deleteApi(formUri(uri))
            else:
                return self.Response
            self.Response.output = respOp.json()
            self.Response.code = respOp.status_code
            return self.Response

        @staticmethod
        def add(alert_name, type, org_id, node_id=None, include_child=False, duration=5,
                pod_id=None, network_id=None, tunnel_id=None):
            """
            :param pod_id:
            :param network_id:
            :param tunnel_id:
            :param alert_name:
            :param type:
                CERT_EXPIRY,
                HEADLESS_EXPIRY,
                NODE_STATE_CHANGE,
                SERVICE_STATE_CHANGE,
                TUNNEL_STATE_CHANGE,
                NODE_IP_CHANGE,
                NODE_REBOOT,
                NODE_INTERNAL,
                SERVICE_INTERNAL,
                NETWORK_INTERNAL,
                USER_WELCOME_EMAIL,
                USER_VERIFY_EMAIL,
                USER_FORGOT_PASSWORD,
                USER_PASSWORD_CHANGED,
                NODE_UPGRADE;
            :param duration: in minutes.
            :param org_id:
            :param node_id:
            :param include_child: bool
            :return:
            """
            def get_alert_me_from_type(_type):
                _map_ = {
                    'NODE_STATE_CHANGE': "ALIVE,UNREACHABLE",
                    'TUNNEL_STATE_CHANGE': "CONNECTED,TERMINATED",
                    'SERVICE_STATE_CHANGE': "HEALTHY,TERMINATED,UNHEALTHY",
                    'CERT_EXPIRY': "80,100",
                    'HEADLESS_EXPIRY': "80,100",
                    'NODE_UPGRADE': "ENABLED,DISABLED,SUCCESSFUL,FAILED",
                    'NODE_IP_CHANGE': "PRIVATE_IP,PUBLIC_IP"
                }
                return _map_.get(_type, None)
            alert_me = get_alert_me_from_type(type)
            return user.mysubscriptions(action='add', payload=locals())

        @staticmethod
        def delete(sub_id):
            return user.mysubscriptions(action="delete", sub_id=sub_id, payload=locals())

        @staticmethod
        def getv2(filters=None):
            return user.mysubscriptions(action='getv2', filters=filters)

        def __del__(self):
            self.payload = dict()
            self.Response = Response()
