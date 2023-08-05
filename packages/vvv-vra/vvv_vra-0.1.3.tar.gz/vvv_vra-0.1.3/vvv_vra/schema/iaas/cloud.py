# -*- coding: utf-8 -*-
'''
  ____  ___   ____________  ___  ___  ____     _________________
 / __ \/ _ | / __/  _/ __/ / _ \/ _ \/ __ \__ / / __/ ___/_  __/
/ /_/ / __ |_\ \_/ /_\ \  / ___/ , _/ /_/ / // / _// /__  / /   
\____/_/ |_/___/___/___/ /_/  /_/|_|\____/\___/___/\___/ /_/    
         Operational Aid Source for Infra-Structure 

Created on 2020. 3. 13..
@author: Hye-Churn Jang, CMBU Specialist in Korea, VMware [jangh@vmware.com]
'''

from .abstract import *


@SDK.VRA.create
@SDK.VRA.list
@SDK.VRA.get()
@SDK.VRA.update('patch')
@SDK.VRA.delete
@SDK.VRA.entry
@SDK.VRA(api='/iaas/api/cloud-accounts', url='/iaas/api/cloud-accounts/{cloudAccountId}', cloudAccountId='id')
class CloudAccount(VRA):
    
    @property
    def Regions(self):
        if hasattr(self, '_regions'): return self._regions
        return self.__list_hrefs__(Region, 'regions', '_regions')
    
    @property
    def AssociatedCloudAccounts(self):
        if hasattr(self, '_associated_cloud_accounts'): return self._associated_cloud_accounts
        return self.__list_hrefs__(CloudAccount, 'associated-cloud-accounts', '_associated_cloud_accounts')
    
    @SDK.VRA.create()
    @SDK.VRA(api='/iaas/api/cloud-accounts/region-enumeration')
    class RegionEnumeration(VRA):
        
        '''
        {
            "cloudAccountProperties": "{\"supportPublicImages\": \"true\", \"acceptSelfSignedCertificate\": \"true\" }",
            "privateKey": "gfsScK345sGGaVdds222dasdfDDSSasdfdsa34fS",
            "associatedCloudAccountIds": "[ \"42f3e0d199d134755684cd935435a\" ]",
            "createDefaultZones": true,
            "customProperties": "{ \"sampleadapterProjectId\" : \"projectId\" }",
            "cloudAccountType": "vsphere, aws, azure, nsxv, nsxt",
            "name": "string",
            "description": "string",
            "regionIds": "[ \"us-east-1\", \"ap-northeast-1\" ]",
            "privateKeyId": "ACDC55DB4MFH6ADG75KK",
            "tags": "[ { \"key\" : \"env\", \"value\": \"dev\" } ]"
        }
        '''
    
    @SDK.VRA.create
    @SDK.VRA.list
    @SDK.VRA.get
    @SDK.VRA.update('patch')
    @SDK.VRA.delete
    @SDK.VRA(api='/iaas/api/cloud-accounts-vsphere', url='/iaas/api/cloud-accounts-vsphere/{cloudAccountId}', cloudAccountId='id')
    class vSphere(VRA):
        
        '''
        {
            "hostName": "vc.mycompany.com",
            "acceptSelfSignedCertificate": false,
            "associatedCloudAccountIds": "[ \"42f3e0d199d134755684cd935435a\" ]",
            "password": "cndhjslacd90ascdbasyoucbdh",
            "createDefaultZones": true,
            "dcid": "23959a1e-18bc-4f0c-ac49-b5aeb4b6eef4",
            "name": "string",
            "description": "string",
            "regionIds": "[ \"Datacenter:datacenter-2\" ]",
            "username": "administrator@mycompany.com",
            "tags": "[ { \"key\" : \"env\", \"value\": \"dev\" } ]"
        }
        '''
        
        @SDK.VRA.create()
        @SDK.VRA(api='/iaas/api/cloud-accounts-vsphere/region-enumeration')
        class RegionEnumeration(VRA): pass
    
    @SDK.VRA.create
    @SDK.VRA.list
    @SDK.VRA.get
    @SDK.VRA.update('patch')
    @SDK.VRA.delete
    @SDK.VRA(api='/iaas/api/cloud-accounts-aws', url='/iaas/api/cloud-accounts-aws/{cloudAccountId}', cloudAccountId='id')
    class AWS(VRA):
        
        '''
        {
            "accessKeyId": "ACDC55DB4MFH6ADG75KK",
            "secretAccessKey": "gfsScK345sGGaVdds222dasdfDDSSasdfdsa34fS",
            "createDefaultZones": true,
            "name": "string",
            "description": "string",
            "regionIds": "[ \"us-east-1\", \"ap-northeast-1\" ]",
            "tags": "[ { \"key\" : \"env\", \"value\": \"dev\" } ]"
        }
        '''
        
        @SDK.VRA.create()
        @SDK.VRA(api='/iaas/api/cloud-accounts-aws/region-enumeration')
        class RegionEnumeration(VRA): pass
    
    @SDK.VRA.create
    @SDK.VRA.list
    @SDK.VRA.get
    @SDK.VRA.update('patch')
    @SDK.VRA.delete
    @SDK.VRA(api='/iaas/api/cloud-accounts-azure', url='/iaas/api/cloud-accounts-azure/{cloudAccountId}', cloudAccountId='id')
    class Azure(VRA):
        
        '''
        {
            "createDefaultZones": true,
            "clientApplicationId": "3287dd6e-76d8-41b7-9856-2584969e7739",
            "clientApplicationSecretKey": "GDfdasDasdASFas321das32cas2x3dsXCSA76xdcasg=",
            "name": "string",
            "tenantId": "9a13d920-4691-4e2d-b5d5-9c4c1279bc9a",
            "description": "string",
            "regionIds": "[ \"East US\", \"North Europe\" ]",
            "subscriptionId": "064865b2-e914-4717-b415-8806d17948f7",
            "tags": "[ { \"key\" : \"env\", \"value\": \"dev\" } ]"
        }
        '''
        
        @SDK.VRA.create()
        @SDK.VRA(api='/iaas/api/cloud-accounts-azure/region-enumeration')
        class RegionEnumeration(VRA): pass
    
    @SDK.VRA.create
    @SDK.VRA.list
    @SDK.VRA.get
    @SDK.VRA.update('patch')
    @SDK.VRA.delete
    @SDK.VRA(api='/iaas/api/cloud-accounts-gcp', url='/iaas/api/cloud-accounts-gcp/{cloudAccountId}', cloudAccountId='id')
    class GCP(VRA):
        
        '''
        {
            "privateKey": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
            "createDefaultZones": true,
            "clientEmail": "321743978432-compute@developer.gserviceaccount.com",
            "name": "string",
            "description": "string",
            "regionIds": "[ \"us-east1\", \"northamerica-northeast1\" ]",
            "projectId": "example-gcp-project",
            "privateKeyId": "027f73d50a19452eedf5775a9b42c5083678abdf",
            "tags": "[ { \"key\" : \"env\", \"value\": \"dev\" } ]"
        }
        '''
        
        @SDK.VRA.create()
        @SDK.VRA(api='/iaas/api/cloud-accounts-gcp/region-enumeration')
        class RegionEnumeration(VRA): pass
    
    @SDK.VRA.create
    @SDK.VRA.list
    @SDK.VRA.get
    @SDK.VRA.update('patch')
    @SDK.VRA.delete
    @SDK.VRA(api='/iaas/api/cloud-accounts-nsx-t', url='/iaas/api/cloud-accounts-nsx-t/{cloudAccountId}', cloudAccountId='id')
    class NSXT(VRA):
        
        '''
        {
            "hostName": "nsxt.mycompany.com",
            "acceptSelfSignedCertificate": false,
            "password": "cndhjslacd90ascdbasyoucbdh",
            "dcid": "23959a1e-18bc-4f0c-ac49-b5aeb4b6eef4",
            "name": "string",
            "description": "string",
            "username": "administrator@mycompany.com",
            "tags": "[ { \"key\" : \"env\", \"value\": \"dev\" } ]"
        }
        '''
    
    @SDK.VRA.create
    @SDK.VRA.list
    @SDK.VRA.get
    @SDK.VRA.update('patch')
    @SDK.VRA.delete
    @SDK.VRA(api='/iaas/api/cloud-accounts-nsx-v', url='/iaas/api/cloud-accounts-nsx-v/{cloudAccountId}', cloudAccountId='id')
    class NSXV(VRA):
        
        '''
        {
            "hostName": "nsxv.mycompany.com",
            "acceptSelfSignedCertificate": false,
            "password": "cndhjslacd90ascdbasyoucbdh",
            "dcid": "23959a1e-18bc-4f0c-ac49-b5aeb4b6eef4",
            "name": "string",
            "description": "string",
            "username": "administrator@mycompany.com",
            "tags": "[ { \"key\" : \"env\", \"value\": \"dev\" } ]"
        }
        '''


@SDK.VRA.list
@SDK.VRA.get()
@SDK.VRA.entry
@SDK.VRA(api='/iaas/api/regions', url='/iaas/api/regions/{regionId}', regionId='id')
class Region(VRA):
    
    @property
    def CloudAccount(self):
        if hasattr(self, '_cloud_account'): return self._cloud_account
        return self.__get_href__(CloudAccount, 'cloud-account', '_cloud_account')


@SDK.VRA.create
@SDK.VRA.list
@SDK.VRA.get()
@SDK.VRA.update('patch')
@SDK.VRA.delete
@SDK.VRA.entry
@SDK.VRA(api='/iaas/api/projects', url='/iaas/api/projects/{projectId}', projectId='id')
class Project(VRA):
    
    '''
    {
        "machineNamingTemplate": "${project.name}-test-${####}",
        "sharedResources": true,
        "operationTimeout": 30,
        "members": "[{ \"email\":\"member@vmware.com\" }]",
        "zoneAssignmentConfigurations": [{
            "zoneId": "77ee1",
            "maxNumberInstances": 50,
            "priority": 1
        }],
        "name": "string",
        "description": "string",
        "constraints": "{\"network\":[{\"mandatory\": \"true\", \"expression\": \"env:dev\"}],\"storage\":[{\"mandatory\": \"false\", \"expression\": \"gold\"}],\"extensibility\":[{\"mandatory\": \"false\", \"expression\": \"key:value\"}]}",
        "administrators": "[{ \"email\":\"administrator@vmware.com\" }]"
    }
    '''
    
    @SDK.VRA.update('patch')
    @SDK.VRA.property
    @SDK.VRA(url='/iaas/api/projects/{projectId}/resource-metadata')
    class Metadata(VRA): pass


@SDK.VRA.create
@SDK.VRA.list
@SDK.VRA.get()
@SDK.VRA.update('patch')
@SDK.VRA.delete
@SDK.VRA.entry
@SDK.VRA(api='/iaas/api/zones', url='/iaas/api/zones/{zoneId}', zoneId='id')
class Zone(VRA):
    
    @property
    def CloudAccount(self):
        #=======================================================================
        # referenced not normal url 
        #=======================================================================
        if hasattr(self, '_cloud_account'): return self._cloud_account
        try: data = Zone.__model__(**SDK.VRA.doGetMethod('/iaas/api/cloud-accounts/%s' % self._links['cloud-account']['href'].split('/endpoints/')[1]).json())
        except: data = None
        self._cloud_account = data
        return data
    
    @property
    def Region(self):
        if hasattr(self, '_region'): return self._region
        return self.__get_href__(Region, 'region', '_region')
    
    @property
    def Projects(self):
        if hasattr(self, '_projects'): return self._projects
        return self.__list_hrefs__(Project, 'projects', '_projects')
    

@SDK.VRA.list
@SDK.VRA.entry
@SDK.VRA(api='/iaas/api/tags')
class Tag(VRA): pass
