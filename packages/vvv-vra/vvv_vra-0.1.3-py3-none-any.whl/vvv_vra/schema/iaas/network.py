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
from .cloud import CloudAccount, Region


@SDK.VRA.list
@SDK.VRA.get()
@SDK.VRA.update('patch')
@SDK.VRA.entry
@SDK.VRA(api='/iaas/api/fabric-networks', url='/iaas/api/fabric-networks/{fabricNetworkId}', fabricNetworkId='id')
class FabricNetwork(VRA):
     
    '''
    {
        "tags": "[ { \"key\" : \"fast-network\", \"value\": \"true\" } ]"
    }
    '''
    
    @property
    def Regions(self):
        if hasattr(self, '_regions'): return self._regions
        return self.__list_hrefs__(Region, 'regions', '_regions')
     
    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA.update('patch')
    @SDK.VRA(api='/iaas/api/fabric-networks-vsphere', url='/iaas/api/fabric-networks-vsphere/{fabricNetworkvSphereId}', fabricNetworkvSphereId='id')
    class vSphere(VRA):
          
        '''
        {
            "ipv6Cidr": "2001:eeee:6bd:2a::1/64",
            "isDefault": true,
            "domain": "sqa.local",
            "defaultIpv6Gateway": "2001:eeee:6bd:2a::1",
            "dnsServerAddresses": "[1.1.1.1]",
            "isPublic": true,
            "cidr": "10.1.2.0/24",
            "defaultGateway": "10.1.2.1",
            "tags": "[ { \"key\" : \"fast-network\", \"value\": \"true\" } ]",
            "dnsSearchDomains": "[vmware.com]"
        }
        '''
        
        @property
        def Regions(self):
            if hasattr(self, '_regions'): return self._regions
            return self.__list_hrefs__(Region, 'regions', '_regions')

    
@SDK.VRA.create
@SDK.VRA.list
@SDK.VRA.get()
@SDK.VRA.delete
@SDK.VRA.entry
@SDK.VRA(api='/iaas/api/networks', url='/iaas/api/networks/{networkId}', networkId='id')
class Network(VRA):
    
    '''
    {
        "customProperties": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
        },
        "outboundAccess": true,
        "name": "string",
        "description": "string",
        "projectId": "e058",
        "constraints": "[{\"mandatory\" : \"true\", \"expression\": \"environment\":\"prod\"}, {\"mandatory\" : \"false\", \"expression\": \"pci\"}]",
        "tags": "[ { \"key\" : \"vmware.enumeration.type\", \"value\": \"nec2_vpc\" } ]"
    }
    '''
    
    def __getattribute__(self, name):
        if name == 'Domain': return self._Domain
        return VRA.__getattribute__(self, name)
    
    @property
    def _Domain(self):
        if hasattr(self, '_domains'): return self._domains
        return self.__get_href__(Network.Domain, 'network-domains', '_domains')
    
    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA(api='/iaas/api/network-domains', url='/iaas/api/network-domains/{networkDomainId}', networkDomainId='id')
    class Domain(VRA):
        
        @property
        def CloudAccounts(self):
            if hasattr(self, '_cloud_accounts'): return self._cloud_accounts
            return self.__list_hrefs__(CloudAccount, 'cloud-accounts', '_cloud_accounts')
    
    @SDK.VRA.create
    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA.update('patch')
    @SDK.VRA.delete
    @SDK.VRA(api='/iaas/api/network-ip-ranges', url='/iaas/api/network-ip-ranges/{networkIpRangeId}', networkIpRangeId='id')
    class IpRange(VRA):
         
        '''
        {
            "ipVersion": "IPv4",
            "fabricNetworkId": "string",
            "name": "string",
            "description": "string",
            "startIPAddress": "string",
            "endIPAddress": "string",
            "tags": "[ { \"key\" : \"fast-network\", \"value\": \"true\" } ]"
        }
        '''
     
    @SDK.VRA.create
    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA.update('patch')
    @SDK.VRA.delete
    @SDK.VRA(api='/iaas/api/network-profiles', url='/iaas/api/network-profiles/{networkProfileId}', networkProfileId='id')
    class Profile(VRA):
         
        '''
        {
            "fabricNetworkIds": "[ \"6543\" ]",
            "customProperties": "{ \"resourcePoolId\" : \"resource-pool-1\" }",
            "regionId": "9e49",
            "securityGroupIds": "[ \"6545\" ]",
            "name": "string",
            "description": "string",
            "isolationExternalFabricNetworkId": "1234",
            "isolationType": "SUBNET",
            "isolatedNetworkCIDRPrefix": 24,
            "isolationNetworkDomainCIDR": "10.10.10.0/24",
            "isolationNetworkDomainId": "1234",
            "tags": "[ { \"key\" : \"dev\", \"value\": \"hard\" } ]"
        }
        '''
        
        @property
        def Region(self):
            if hasattr(self, '_region'): return self._region
            return self.__get_href__(Region, 'region', '_region')
        
        @property
        def FabricNetworks(self):
            if hasattr(self, '_fabric_networks'): return self._fabric_networks
            return self.__list_hrefs__(FabricNetwork, 'fabric-networks', '_fabric_networks')
        
        @property
        def IsolatedExternalFabricNetwork(self):
            if hasattr(self, '_isolated_external_fabric_network'): return self._isolated_external_fabric_network
            return self.__get_href__(FabricNetwork, 'isolated-external-fabric-networks', '_isolated_external_fabric_network')
        
        @property
        def Domain(self):
            if hasattr(self, '_domains'): return self._domains
            return self.__get_href__(Network.Domain, 'network-domains', '_domains')


@SDK.VRA.list
@SDK.VRA.get()
@SDK.VRA.entry
@SDK.VRA(api='/iaas/api/security-groups', url='/iaas/api/security-groups/{securityGroupid}', securityGroupid='id')
class SecurityGroup(VRA):
    
    @property
    def CloudAccounts(self):
        if hasattr(self, '_cloud_accounts'): return self._cloud_accounts
        return self.__list_hrefs__(CloudAccount, 'cloud-accounts', '_cloud_accounts')

