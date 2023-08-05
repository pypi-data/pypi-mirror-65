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


@SDK.VRA.create
@SDK.VRA.list
@SDK.VRA.get()
@SDK.VRA.delete
@SDK.VRA.entry
@SDK.VRA(api='/policy/api/policies', url='/policy/api/policies/{policyId}', policyId='id')
class Policy(Model):
    
    '''
    {
        "createdAt": "2020-04-07T05:35:11.005Z",
        "createdBy": "string",
        "criteria": {
            "matchExpression": [{}]
        },
        "definition": {},
        "description": "string",
        "enforcementType": "SOFT",
        "id": "string",
        "lastUpdatedAt": "2020-04-07T05:35:11.005Z",
        "lastUpdatedBy": "string",
        "name": "string",
        "orgId": "string",
        "projectId": "string",
        "statistics": {
            "conflictCount": 0,
            "enforcedCount": 0,
            "notEnforcedCount": 0
        },
        "typeId": "string"
    }
    '''
    
    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA(api='/policy/api/policyDecisions', url='/policy/api/policyDecisions/{decisionId}', decisionId='id')
    class Decision(Model): pass
    
    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA(api='/policy/api/policyTypes', url='/policy/api/policyTypes/{typeId}', typeId='id')
    class Type(Model): pass
