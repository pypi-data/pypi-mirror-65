# -*- coding: utf-8 -*-
'''
  ____  ___   ____________  ___  ___  ____     _________________
 / __ \/ _ | / __/  _/ __/ / _ \/ _ \/ __ \__ / / __/ ___/_  __/
/ /_/ / __ |_\ \_/ /_\ \  / ___/ , _/ /_/ / // / _// /__  / /   
\____/_/ |_/___/___/___/ /_/  /_/|_|\____/\___/___/\___/ /_/    
         Operational Aid Source for Infra-Structure 

Created on 2020. 3. 16..
@author: Hye-Churn Jang, CMBU Specialist in Korea, VMware [jangh@vmware.com]
'''

from .abstract import *
from .cloud import CloudAccount
from .compute import Machine
from .network import Network


@SDK.VRA.create
@SDK.VRA.list
@SDK.VRA.get()
@SDK.VRA.delete
@SDK.VRA.entry
@SDK.VRA(api='/iaas/api/load-balancers', url='/iaas/api/load-balancers/{loadBalancerId}', loadBalancerId='id')
class LoadBalancer(VRA):
    
    '''
    {
        "routes": [{
            "protocol": "TCP, UDP",
            "port": "80",
            "memberPort": "80",
            "memberProtocol": "TCP, UDP",
            "healthCheckConfiguration": {
                "protocol": "HTTP, HTTPS",
                "port": "80",
                "timeoutSeconds": 5,
                "unhealthyThreshold": 5,
                "healthyThreshold": 2,
                "urlPath": "/index.html",
                "intervalSeconds": 60
            }
        }],
        "customProperties": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
        },
        "targetLinks": "[ \"/iaas/machines/eac3d\" ]",
        "internetFacing": true,
        "name": "string",
        "nics": [{
            "addresses": "[ \"10.1.2.190\" ]",
            "customProperties": "{ \"awaitIp\" : \"true\" }",
            "securityGroupIds": ["string"],
            "name": "string",
            "description": "string",
            "networkId": "dcd9",
            "deviceIndex": 1
        }],
        "description": "string",
        "projectId": "e058",
        "tags": "[ { \"key\" : \"ownedBy\", \"value\": \"Rainpole\" } ]"
    }
    '''
    
    def Scale(self, **intent):
        SDK.VRA.doPostMethod(self.__url__() + '/operations/scale', intent)
        return self
    
    def Delete(self, **intent):
        SDK.VRA.doPostMethod(self.__url__() + '/operations/delete')
        return self
    
    @property
    def CloudAccounts(self):
        if hasattr(self, '_cloud_accounts'): return self._cloud_accounts
        return self.__list_hrefs__(CloudAccount, 'cloud-accounts', '_cloud_accounts')
    
    @property
    def CloudAccount(self):
        if hasattr(self, '_cloud_account'): return self._cloud_account
        return self.__get_href__(CloudAccount, 'cloud-account', '_cloud_account')
    
    @property
    def Targets(self):
        if hasattr(self, '_targets'): return self._targets
        return self.__list_hrefs__(Machine, 'load-balancer-targets', '_targets')
    
    @property
    def NetworkInterfaces(self):
        if hasattr(self, '_network_interfaces'): return self._network_interfaces
        return self.__list_hrefs__(LoadBalancer.NetworkInterface, 'network-interfaces', '_network_interfaces')
    
    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA(api='/iaas/api/load-balancers/{loadBalancerId}/network-interfaces', url='/iaas/api/load-balancers/{loadBalancerId}/network-interfaces/{networkInterfaceId}', networkInterfaceId='id')
    class NetworkInterface(VRA):
        
        def __inst_list_wrapper__(self, **clause):
            return (-self).NetworkInterfaces
        
        @property
        def Network(self):
            if hasattr(self, '_network'): return self._network
            return self.__get_href__(Network, 'network', '_network')
