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

from pygics import Model, loadYaml


@SDK.VRA.create
@SDK.VRA.list
@SDK.VRA.get()
@SDK.VRA.update('put')
@SDK.VRA.delete
@SDK.VRA.entry
@SDK.VRA(api='/blueprint/api/blueprints', url='/blueprint/api/blueprints/{blueprintId}', blueprintId='id')
class Blueprint(Model):
    
    '''
    {
        "content": "string",
        "description": "string",
        "name": "string",
        "projectId": "string",
        "requestScopeOrg": true
    }
    '''
    
    @SDK.VRA.property
    @SDK.VRA(url='/blueprint/api/blueprints/{blueprintId}/inputs-schema')
    class Input(Model): pass
    
    @property
    def Content(self):
        if hasattr(self, '_content'): return self._content
        else:
            if 'content' in self:
                self._content = Model(**loadYaml(self.content))
            else:
                detail = Blueprint(self.id)
                self['content'] = detail.content
                self._content = Model(**loadYaml(self.content))
            return self._content
    
    @property
    def Versions(self):
        if hasattr(self, '_versions'): return self._versions
        self._versions = self.Version.list()
        return self._versions
    
    @SDK.VRA.create
    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA.update('put')
    @SDK.VRA.delete
    @SDK.VRA(api='/blueprint/api/blueprints/{blueprintId}/versions', url='/blueprint/api/blueprints/{blueprintId}/versions/{version}', version='id')
    class Version(Model):
        
        '''
        {
            "changeLog": "string",
            "description": "string",
            "release": true,
            "version": "string"
        }
        '''
        
        def Release(self):
            return self.__data__(**SDK.VRA.doPostMethod(self.__url__('/actions/release')).json())
        
        def Restore(self):
            return Blueprint.__model__(**SDK.VRA.doPostMethod('/blueprint/api/blueprints/{blueprintId}/versions/{version}/actions/restore'.format(**self.__keys__())).json())
            
        def Unrelease(self):
            return self.__data__(**SDK.VRA.doPostMethod(self.__url__('/actions/unrelease')).json())
        
    @SDK.VRA.create()
    @SDK.VRA.list
    @SDK.VRA.get
    @SDK.VRA.update('put')
    @SDK.VRA.delete
    @SDK.VRA(api='/blueprint/api/blueprint-requests', url='/blueprint/api/blueprint-requests/{requestId}', requestId='id')
    class Request(Model):
        
        '''
        {
            "blueprintId": "string",
            "blueprintVersion": "string",
            "content": "string",
            "deploymentId": "string",
            "deploymentName": "string",
            "description": "string",
            "destroy": true,
            "ignoreDeleteFailures": true,
            "inputs": {},
            "plan": true,
            "projectId": "string",
            "reason": "string",
            "simulate": true
        }
        '''
        
        @staticmethod
        def __create_filter__(model, intent):
            if 'blueprintId' not in intent:
                intent['blueprintId'] = (-model).id
        
        def Cancle(self):
            SDK.VRA.doPostMethod(self.__url__('/actions/cancel'))
            return self
        
    @SDK.VRA.create()
    @SDK.VRA(api='/blueprint/api/blueprint-validation')
    class Validation(Model):
        
        '''
        {
            "blueprintId": "string",
            "content": "string",
            "inputs": {},
            "projectId": "string"
        }
        '''
        
        @staticmethod
        def __create_filter__(model, intent):
            if 'blueprintId' not in intent:
                intent['blueprintId'] = (-model).id

    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA(api='/blueprint/api/resource-types', url='/blueprint/api/resource-types/{resourceTypeId}', resourceTypeId='id')
    class ResourceType(Model): pass
