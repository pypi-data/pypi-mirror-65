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

from pygics import Rest, RestUser, sdk


class VRAUser(RestUser):
    
    def __headers__(self, **kwargs):
        RestUser.__headers__(self, **{
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        self.token = self.sdk.doPostMethod('/csp/gateway/am/api/login?access_token', {'username' : self.username, 'password' : self.password}).json()['access_token']
        RestUser.__headers__(self, Authorization='Bearer ' + self.token)


@sdk
class VRA(Rest):
    
    def __init__(self):
        Rest.__init__(self, user_model=VRAUser, list_layer=['content'])


from .schema.about import About
from .schema.blueprint import Blueprint
from .schema.deployment import Deployment
from .schema.catalog import Catalog
from .schema.policy import Policy
from .schema.gateway import User
from .schema.iaas.cloud import CloudAccount, Region, Project, Zone, Tag
from .schema.iaas.flavor import FabricFlavor, Flavor 
from .schema.iaas.image import FabricImage, Image
from .schema.iaas.compute import Machine
from .schema.iaas.network import FabricNetwork, Network, SecurityGroup
from .schema.iaas.loadbalance import LoadBalancer
