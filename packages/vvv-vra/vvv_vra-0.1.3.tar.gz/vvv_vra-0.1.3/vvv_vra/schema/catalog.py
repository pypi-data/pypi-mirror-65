# -*- coding: utf-8 -*-
'''
  ____  ___   ____________  ___  ___  ____     _________________
 / __ \/ _ | / __/  _/ __/ / _ \/ _ \/ __ \__ / / __/ ___/_  __/
/ /_/ / __ |_\ \_/ /_\ \  / ___/ , _/ /_/ / // / _// /__  / /   
\____/_/ |_/___/___/___/ /_/  /_/|_|\____/\___/___/\___/ /_/    
         Operational Aid Source for Infra-Structure 

Created on 2020. 4. 7..
@author: Hye-Churn Jang, CMBU Specialist in Korea, VMware [jangh@vmware.com]
'''

from pygics import Model


@SDK.VRA.list
@SDK.VRA.get()
@SDK.VRA.entry
@SDK.VRA(api='/catalog/api/items', url='/catalog/api/items/{catalogId}', catalogId='id')
class Catalog(Model):
    
    @SDK.VRA.create()
    @SDK.VRA(api='/catalog/api/items/{catalogId}/request')
    class Request(Model):
        
        '''
        {
            "deploymentName": "string",
            "inputs": {},
            "projectId": "string",
            "reason": "string",
            "version": "string"
        }
        '''
    
    @SDK.VRA.create()
    @SDK.VRA.get
    @SDK.VRA(api='/catalog/api/items/{catalogId}/upfront-prices', url='/catalog/api/items/{catalogId}/upfront-prices/{upfrontPriceId}', upfrontPriceId='upfrontPriceId')
    class Price(Model):
        
        '''
        {
            "deploymentName": "string",
            "inputs": {},
            "projectId": "string",
            "reason": "string",
            "version": "string"
        }
        '''
    
    @property
    def Versions(self):
        if hasattr(self, '_versions'): return self._versions
        self._versions = self.Version.list()
        return self._versions
    
    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA(api='/catalog/api/items/{catalogId}/versions', url='/catalog/api/items/{catalogId}/versions/{versionId}', versionId='id')
    class Version(Model): pass
    
    @SDK.VRA.create
    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA.delete
    @SDK.VRA(api='/catalog/api/admin/sources', url='/catalog/api/admin/sources/{sourceId}', sourceId='id')
    class Source(Model):
        
        '''
        {
            "config": {},
            "createdAt": "2020-04-07T04:22:34.864Z",
            "createdBy": "string",
            "description": "string",
            "global": true,
            "id": "string",
            "itemsFound": 0,
            "itemsImported": 0,
            "lastImportCompletedAt": "2020-04-07T04:22:34.864Z",
            "lastImportErrors": ["string"],
            "lastImportStartedAt": "2020-04-07T04:22:34.864Z",
            "lastUpdatedAt": "2020-04-07T04:22:34.864Z",
            "lastUpdatedBy": "string",
            "name": "string",
            "projectId": "string",
            "typeId": "string"
        }
        '''
    
    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA.update('patch')
    @SDK.VRA(api='/catalog/api/admin/items', url='/catalog/api/admin/items/{itemId}', itemId='id')
    class Item(Model): pass
    
    @SDK.VRA.create()
    @SDK.VRA.list
    @SDK.VRA.delete
    @SDK.VRA(api='/catalog/api/admin/entitlements', url='/catalog/api/admin/entitlements/{entitlementId}', entitlementId='id')
    class Entitlement(Model):
        
        '''
        {
            "definition": {
                "description": "string",
                "iconId": "string",
                "id": "string",
                "name": "string",
                "numItems": 0,
                "sourceName": "string",
                "sourceType": "string",
                "type": "string"
            },
            "id": "string",
            "projectId": "string"
        }
        '''
    
    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA(api='/catalog/api/types', url='/catalog/api/types/{typeId}', typeId='id')
    class Type(Model): pass
        
