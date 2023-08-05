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


@SDK.VRA.entry
@SDK.VRA()
class About(Model):
    
    @SDK.VRA.get()
    @SDK.VRA(url='/blueprint/api/about')
    class Blueprint(Model): pass
    
    @SDK.VRA.get()
    @SDK.VRA(url='/iaas/api/about')
    class IaaS(Model): pass
    
