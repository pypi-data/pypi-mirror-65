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
from .cloud import Region


@SDK.VRA.list
@SDK.VRA.entry
@SDK.VRA(api='/iaas/api/fabric-flavors')
class FabricFlavor(VRA): pass


@SDK.VRA.list
@SDK.VRA.entry
@SDK.VRA(api='/iaas/api/flavors')
class Flavor(VRA):
    
    @SDK.VRA.create
    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA.update('patch')
    @SDK.VRA.delete
    @SDK.VRA(api='/iaas/api/flavor-profiles', url='/iaas/api/flavor-profiles/{flavorProfileId}', flavorProfileId='id')
    class Profile(VRA):
        
        '''
        {
            "regionId": "9e49",
            "name": "string",
            "description": "string",
            "flavorMapping": "{ \"small\": { \"name\": \"t2.small\" }, \"medium\": { \"name\": \"t2.medium\"}}, \"vSphere_small\": { \"cpuCount\": \"2\", \"memoryInMB\": \"2048\"}, \"vSphere_medium\": { \"cpuCount\": \"4\", \"memoryInMB\": \"4096\"}}"
        }
        '''
        
        @property
        def Region(self):
            if hasattr(self, '_region'): return self._region
            return self.__get_href__(Region, 'region', '_region')
