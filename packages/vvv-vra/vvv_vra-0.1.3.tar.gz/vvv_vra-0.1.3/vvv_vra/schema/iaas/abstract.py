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

from pygics import Model, ModelList


class VRA(Model):
    
    def __get_href__(self, model, path_name, cache_var_name):
        try: data = model.__model__(**SDK.VRA.doGetMethod(self._links[path_name]['href']).json())
        except: data = None
        self.__setattr__(cache_var_name, data)
        return data
    
    def __list_hrefs__(self, model, path_name, cache_var_name):
        list_of_data = ModelList(model)
        self.__setattr__(cache_var_name, list_of_data)
        try:
            for url in self._links[path_name]['hrefs']:
                try: data = SDK.VRA.doGetMethod(url).json()
                except: pass
                else: list_of_data(**data)
        except: pass
        return list_of_data
    
