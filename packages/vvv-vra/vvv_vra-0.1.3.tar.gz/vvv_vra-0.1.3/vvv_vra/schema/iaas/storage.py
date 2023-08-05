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

from pygics import Model


@SDK.VRA.create
@SDK.VRA.list
@SDK.VRA.get
@SDK.VRA.delete
@SDK.VRA.entry
@SDK.VRA(api='/iaas/api/block-devices', url='/iaas/api/block-devices/{blockDeviceId}', blockDeviceId='id')
class BlockDevice(Model): pass

@SDK.VRA.entry
@SDK.VRA()
class Storage(Model):
    
    @SDK.VRA.create
    @SDK.VRA.list
    @SDK.VRA.get
    @SDK.VRA.update_using_put
    @SDK.VRA.delete
    @SDK.VRA(api='/iaas/api/storage-profiles', url='/iaas/api/storage-profiles/{storageProfileId}', storageProfileId='id')
    class Profile(Model):
        
        
        @SDK.VRA.create
        @SDK.VRA.list
        @SDK.VRA.get
        @SDK.VRA.update_using_patch()
        @SDK.VRA.delete
        @SDK.VRA(api='/iaas/api/storage-profiles-vsphere', url='/iaas/api/storage-profiles-vsphere/{storageProfilevSphereId}', storageProfilevSphereId='id')
        class vSphere(Model): pass
        
        @SDK.VRA.create
        @SDK.VRA.list
        @SDK.VRA.get
        @SDK.VRA.update_using_patch()
        @SDK.VRA.delete
        @SDK.VRA(api='/iaas/api/storage-profiles-aws', url='/iaas/api/storage-profiles-aws/{storageProfileAWSId}', storageProfileAWSId='id')
        class AWS(Model): pass
        
        @SDK.VRA.create
        @SDK.VRA.list
        @SDK.VRA.get
        @SDK.VRA.update_using_patch()
        @SDK.VRA.delete
        @SDK.VRA(api='/iaas/api/storage-profiles-azure', url='/iaas/api/storage-profiles-azure/{storageProfileAzureId}', storageProfileAzureId='id')
        class Azure(Model): pass
        
        