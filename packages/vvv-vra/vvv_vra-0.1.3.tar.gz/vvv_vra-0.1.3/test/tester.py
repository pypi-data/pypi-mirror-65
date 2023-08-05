# -*- coding: utf-8 -*-
'''
  ____  ___   ____________  ___  ___  ____     _________________
 / __ \/ _ | / __/  _/ __/ / _ \/ _ \/ __ \__ / / __/ ___/_  __/
/ /_/ / __ |_\ \_/ /_\ \  / ___/ , _/ /_/ / // / _// /__  / /   
\____/_/ |_/___/___/___/ /_/  /_/|_|\____/\___/___/\___/ /_/    
         Operational Aid Source for Infra-Structure 

Created on 2020. 3. 18..
@author: Hye-Churn Jang, CMBU Specialist in Korea, VMware [jangh@vmware.com]
'''

from vvv_vra import *

SDK.VRA.system('https://vra.vmkloud.com', 'jangh', 'David*#8090')


# prjs = Project.list()
# print(prjs)
# prj = Project('5991fbf0-6c49-4548-b8b3-a84a5a0d7b3a')
# print(prj)
# print(prj.Metadata)
# prj.Metadata['tags'] = []
# prj.Metadata.update()




# cats = Catalog.list()
# for cat in cats:
#     print(cat)

cat = Catalog('f84383f0-5ec5-3f72-9c31-7d11181aa8da')
# print(cat)
# print(cat.Version.list())
# print(cat.Price(**{
#             "deploymentName": "test",
#             "inputs": {},
#             "projectId": "5991fbf0-6c49-4548-b8b3-a84a5a0d7b3a",
#             "version": "1"
#         }))
# print(cat.Price.get('6b47cc73-5173-44a0-b1d1-7dab7a2f1805'))

print(cat.Request(**{
            "deploymentName": "test",
            "inputs": {},
            "projectId": "5991fbf0-6c49-4548-b8b3-a84a5a0d7b3a",
            "version": "1"
        }))
