# -*- coding: utf-8 -*-
'''
  ____  ___   ____________  ___  ___  ____     _________________
 / __ \/ _ | / __/  _/ __/ / _ \/ _ \/ __ \__ / / __/ ___/_  __/
/ /_/ / __ |_\ \_/ /_\ \  / ___/ , _/ /_/ / // / _// /__  / /   
\____/_/ |_/___/___/___/ /_/  /_/|_|\____/\___/___/\___/ /_/    
         Operational Aid Source for Infra-Structure 

Created on 2020. 2. 15.
@author: Hye-Churn Jang, CMBU Specialist in Korea, VMware [jangh@vmware.com]
'''

from pygics import Model
from requests.exceptions import HTTPError


@SDK.VRA.list
@SDK.VRA.get()
@SDK.VRA.update('patch')
@SDK.VRA.delete
@SDK.VRA.entry
@SDK.VRA(api='/deployment/api/deployments', url='/deployment/api/deployments/{depId}', depId='id')
class Deployment(Model):
    
    @classmethod
    def CheckName(cls, name):
        try:
            SDK.VRA.doGetMethod('/deployment/api/deployments/names/{name}'.format(name=name))
        except HTTPError as e:
            if 'Not Found' in str(e): return False
            raise e
        return True
    
    @classmethod
    def CheckCount(cls, project_id):
        return SDK.VRA.doGetMethod('/deployment/api/projects/{projectId}/deployment-count'.format(projectId=project_id)).json()['totalElements']
    
    @property
    def Resources(self):
        if hasattr(self, '_resources'): return self._resources
        self._resources = self.Resource.list()
        return self._resources
    
    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA.delete
    @SDK.VRA(api='/deployment/api/deployments/{depId}/resources', url='/deployment/api/deployments/{depId}/resources/{resourceId}', resourceId='id')
    class Resource(Model):
        
        @property
        def Actions(self):
            if hasattr(self, '_actions'): return self._actions
            self._actions = self.Action.list()
            return self._actions
        
        @SDK.VRA.list
        @SDK.VRA.get()
        @SDK.VRA(api='/deployment/api/deployments/{depId}/resources/{resourceId}/actions', url='/deployment/api/deployments/{depId}/resources/{resourceId}/actions/{actionId}', actionId='id', list_layer=[])
        class Action(Model):
            
            @staticmethod
            def __get_filter__(model, args, keys):
                component_type = (-model)['properties']['componentType']
                if len(args) == 1 and component_type not in args[0]:
                    args[0] = '%s.%s' % (component_type, args[0])
            
            @SDK.VRA.create()
            @SDK.VRA(api='/deployment/api/deployments/{depId}/resources/{resourceId}/requests')
            class Request(Model):
                
                '''
                {
                    "actionId": "string",
                    "inputs": {},
                    "reason": "string"
                }
                '''
                
                @staticmethod
                def __create_filter__(model, intent):
                    if 'actionId' not in intent:
                        intent['actionId'] = (-model).id
                
                def Cancle(self):
                    SDK.VRA.doPostMethod('/deployment/api/requests/{}?action=cancle'.format(self.id))
                    return self
                
                def Dismiss(self):
                    SDK.VRA.doPostMethod('/deployment/api/requests/{}?action=dismiss'.format(self.id))
                    return self
    
    @property
    def Actions(self):
        if hasattr(self, '_actions'): return self._actions
        self._actions = self.Action.list()
        return self._actions
    
    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA(api='/deployment/api/deployments/{depId}/actions', url='/deployment/api/deployments/{depId}/actions/{actionId}', actionId='id', list_layer=[])
    class Action(Model):
        
        @staticmethod
        def __get_filter__(model, args, keys):
            if len(args) == 1 and 'Deployment.' not in args[0]:
                args[0] = 'Deployment.' + args[0]
        
        @SDK.VRA.create()
        @SDK.VRA(api='/deployment/api/deployments/{depId}/requests')
        class Request(Model):
            
            '''
            {
                "actionId": "string",
                "inputs": {},
                "reason": "string"
            }
            '''
            
            @staticmethod
            def __create_filter__(model, intent):
                if 'actionId' not in intent:
                    intent['actionId'] = (-model).id
            
            def Cancle(self):
                SDK.VRA.doPostMethod('/deployment/api/requests/{}?action=cancle'.format(self.id))
                return self
            
            def Dismiss(self):
                SDK.VRA.doPostMethod('/deployment/api/requests/{}?action=dismiss'.format(self.id))
                return self

    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA(api='/deployment/api/deployments/filters', url='/deployment/api/deployments/filters/{filterId}', filterId='id', list_layer=['filters'])
    class Filter(Model): pass
