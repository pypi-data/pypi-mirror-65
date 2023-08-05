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
@SDK.VRA.get()
@SDK.VRA.entry
@SDK.VRA(api='/iaas/api/fabric-images', url='/iaas/api/fabric-images/{fabricImageId}', fabricImageId='id')
class FabricImage(VRA):

    @property
    def Region(self):
        if hasattr(self, '_region'): return self._region
        return self.__get_href__(Region, 'region', '_region')


@SDK.VRA.list
@SDK.VRA.entry
@SDK.VRA(api='/iaas/api/images')
class Image(VRA):
    
    @SDK.VRA.create
    @SDK.VRA.list
    @SDK.VRA.get()
    @SDK.VRA.update('patch')
    @SDK.VRA.delete
    @SDK.VRA(api='/iaas/api/image-profiles', url='/iaas/api/image-profiles/{imageProfileId}', imageProfileId='id')
    class Profile(VRA):
        
        '''
        {
            "regionId": "9e49",
            "imageMapping": "{ \"ubuntu\": { \"id\": \"9e49\", \"name\": \"ami-ubuntu-16.04-1.9.1-00-1516139717\"}, \"coreos\": { \"id\": \"9e50\", \"name\": \"ami-coreos-26.04-1.9.1-00-543254235\"}}",
            "name": "string",
            "description": "string"
        }
        '''
        
        @property
        def Region(self):
            if hasattr(self, '_region'): return self._region
            return self.__get_href__(Region, 'region', '_region')
