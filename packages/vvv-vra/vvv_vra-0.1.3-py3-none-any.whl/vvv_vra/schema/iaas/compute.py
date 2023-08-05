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
from .cloud import CloudAccount
from .network import Network


@SDK.VRA.create
@SDK.VRA.list
@SDK.VRA.get()
@SDK.VRA.update('patch')
@SDK.VRA.delete
@SDK.VRA.entry
@SDK.VRA(api='/iaas/api/machines', url='/iaas/api/machines/{machineId}', machineId='id')
class Machine(VRA):
    
    '''
    {
        "image": "vmware-gold-master, ubuntu-latest, rhel-compliant, windows",
        "disks": [{
            "blockDeviceId": "1298765",
            "name": "string",
            "description": "string"
        }],
        "imageDiskConstraints": "[{\"mandatory\" : \"true\", \"expression\": \"environment:prod\"}, {\"mandatory\" : \"false\", \"expression\": \"pci\"}]",
        "description": "string",
        "machineCount": 3,
        "constraints": "[{\"mandatory\" : \"true\", \"expression\": \"environment\":\"prod\"}, {\"mandatory\" : \"false\", \"expression\": \"pci\"}]",
        "tags": "[ { \"key\" : \"ownedBy\", \"value\": \"Rainpole\" } ]",
        "flavor": "small, medium, large",
        "customProperties": {
        "additionalProp1": "string",
        "additionalProp2": "string",
        "additionalProp3": "string"
        },
        "bootConfig": {
        "content": "#cloud-config"
        },
        "name": "string",
        "nics": [
        {
        "addresses": "[ \"10.1.2.190\" ]",
        "customProperties": "{ \"awaitIp\" : \"true\" }",
        "securityGroupIds": [
        "string"
        ],
        "name": "string",
        "description": "string",
        "networkId": "dcd9",
        "deviceIndex": 1
        }
        ],
        "imageRef": "ami-f6795a8c",
        "projectId": "e058"
    }
    '''
    
    @property
    def CloudAccounts(self):
        if hasattr(self, '_cloud_accounts'): return self._cloud_accounts
        return self.__list_hrefs__(CloudAccount, 'cloud-accounts', '_cloud_accounts')
    
    @property
    def Operations(self):
        if hasattr(self, '_operations'): return self._operations
        if 'operations' in self._links:
            self._operations = [ op.split(self.id + '/')[1] for op in self._links['operations']['hrefs'] ]
        else:
            self._operations = []
        return self._operations
    
    def Operation(self, operation):
        SDK.VRA.doPostMethod(self.__url__() + '/%s' % operation)
        return self
    
    def Resize(self, cpu_count=None, memory_in_mb=None, flavor=None):
        query = []
        if cpu_count != None:
            query.append('cpuCount=%s' % str(cpu_count))
        if memory_in_mb != None:
            query.append('memoryInMB=%s' % str(memory_in_mb))
        if flavor != None:
            query.append('name=%s' % flavor)
        query = '&'.join(query)
        return self.Operation('/operations/resize?' + query)
    
    def Restart(self):
        return self.Operation('operations/restart')
     
    def Reboot(self):
        return self.Operation('operations/reboot')
     
    def PowerOff(self):
        return self.Operation('operations/power-off')
     
    def Suspend(self):
        return self.Operation('operations/suspend')
     
    def ShutDown(self):
        return self.Operation('operations/shutdown')
     
    def PowerOn(self):
        return self.Operation('operations/shutdown')
     
    def Reset(self):
        return self.Operation('operations/reset')
     
    def Revert(self):
        return self.Operation('operations/revert')
    
    @SDK.VRA.create()
    @SDK.VRA.list
    @SDK.VRA.delete
    @SDK.VRA(api='/iaas/api/machines/{machineId}/snapshots', url='/iaas/api/machines/{machineId}/snapshots/{snapshotId}', snapshotId='id')
    class SnapShot(VRA):
         
        '''
        {
            "owner": "csp@vmware.com",
            "organizationId": "deprecated",
            "createdAt": "2012-09-27",
            "snapshotMemory": true,
            "customProperties": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
            },
            "_links": {
                "additionalProp1": {
                    "hrefs": ["string"],
                    "href": "string"
                },
                "additionalProp2": {
                    "hrefs": ["string"],
                    "href": "string"
                },
                "additionalProp3": {
                    "hrefs": ["string"],
                    "href": "string"
                }
            },
            "name": "my-name",
            "description": "my-description",
            "id": "9e49",
            "orgId": "9e49",
            "updatedAt": "2012-09-27"
        }
        '''
         
        def __inst_create_wrapper__(self, **intent):
            return self.__class__.__model__(**SDK.VRA.doPostMethod(self.__api__().replace('snapshots', 'operations/snapshots'), intent).json())
    
    def AttachDisk(self, **intent):
        self.Disk.create(**intent)
        return self
    
    @property
    def Disks(self):
        if hasattr(self, '_disks'): return self._disks
        return self.__list_hrefs__(Machine.Disk, 'disks', '_disks')
    
    @SDK.VRA.create
    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA.delete
    @SDK.VRA(api='/iaas/api/machines/{machineId}/disks', url='/iaas/api/machines/{machineId}/disks/{diskId}', diskId='id')
    class Disk(VRA):
        
        '''
        {
            "blockDeviceId": "1298765",
            "name": "string",
            "description": "string"
        }
        '''

    @property
    def NetworkInterfaces(self):
        if hasattr(self, '_network_interfaces'): return self._network_interfaces
        return self.__list_hrefs__(Machine.NetworkInterface, 'network-interfaces', '_network_interfaces')
    
    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA(api='/iaas/api/machines/{machineId}/network-interfaces', url='/iaas/api/machines/{machineId}/network-interfaces/{networkInterfaceId}', networkInterfaceId='id')
    class NetworkInterface(VRA):
        
        def __inst_list_wrapper__(self, **clause):
            return (-self).NetworkInterfaces
        
        @property
        def Network(self):
            if hasattr(self, '_network'): return self._network
            return self.__get_href__(Network, 'network', '_network')
