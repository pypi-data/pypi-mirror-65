# -*- coding: utf-8 -*-
'''
  ____  ___   ____________  ___  ___  ____     _________________
 / __ \/ _ | / __/  _/ __/ / _ \/ _ \/ __ \__ / / __/ ___/_  __/
/ /_/ / __ |_\ \_/ /_\ \  / ___/ , _/ /_/ / // / _// /__  / /   
\____/_/ |_/___/___/___/ /_/  /_/|_|\____/\___/___/\___/ /_/    
         Operational Aid Source for Infra-Structure 

Created on 2020. 3. 9..
@author: Hye-Churn Jang, CMBU Specialist in Korea, VMware [jangh@vmware.com]
'''

from vvv_vra import *
SDK.VRA.system('https://vra.vmkloud.com', 'jangh', 'David*#8090')




#===============================================================================
# LoadBalancer & Security Group
#===============================================================================
# print(LoadBalancer.list())
# lb = LoadBalancer('7853aaa62ffa54755a0f311d90a58')
# print(lb)
# print(lb.CloudAccount)
# print(lb.CloudAccounts)
# print(lb.NetworkInterfaces)
# print(lb.Targets)
# print(SecurityGroup.list())
# sg = SecurityGroup('7099c69b5e6cb87559bb7fd23af40')
# print(sg)
# print(sg.CloudAccounts)

#===============================================================================
# Network
#===============================================================================
# net = Network('7099c69b5e6cb87559bb82687f7b1')
# print(net)
# print(net.Domain)
# print(net.Domain.CloudAccounts)
# print(Network.Domain.list())
# print(Network.IpRange.list())
# print(Network.Profile.list())
# np = (Network.Profile('7099c69b5e6cb87559bb82687c100'))
# print(np)
# print(np.Region)
# print(np.IsolatedExternalFabricNetwork)
# print(np.FabricNetworks)


#===============================================================================
# Machine
#===============================================================================
# print(Machine.list())
# vm = Machine('9fe0f5fcc4f8b427')
# print(vm)
# print(vm.Operations)
# print(vm.Disks)
# print(vm.Disk.list())
# print(vm.Disk('7853aaa62ffa54755a06fc73d8cb8'))
# print(vm.NetworkInterfaces)
# print(vm.NetworkInterface.list())
# intf = vm.NetworkInterface('fa989c16238f193f')
# print(intf)
# print(intf.Network)

#===============================================================================
# Image
#===============================================================================
# print(Image.list())
# print(Image.Profile.list())
# img = Image.Profile('3e74e64e-3613-4973-9a31-766d654d42e8-db0a9d6f4d5fb87559c830d749028')
# print(img)
# print(img.Region)

#===============================================================================
# Flavor
#===============================================================================
# print(Flavor.list())
# print(Flavor.Fabric.list())
# print(Flavor.Profile.list())
# fv = Flavor.Profile('3e74e64e-3613-4973-9a31-766d654d42e8-7099c69b5e6cb87559bb7fc0a4060')
# print(fv)
# print(fv.Region)

#===============================================================================
# Cloud
#===============================================================================
# print(CloudAccount.list())
# ca = CloudAccount('7099c69b5e6cb87559bb7fbfeb35a')
# print(ca)
# print(ca.Regions)
# print(ca.AssociatedCloudAccounts)
# print(Region.list())
# rg = Region('7099c69b5e6cb87559bb7fc0a4060')
# print(rg)
# print(rg.CloudAccount)
# print(Zone.list())
# zn = Zone('7099c69b5e6cb87559bb8062ebb98')
# print(zn)
# print(zn.CloudAccount)
# print(zn.Region)
# print(zn.Projects)
# print(Project.list())
# prj = Project('5991fbf0-6c49-4548-b8b3-a84a5a0d7b3a')
# print(prj)
# print(prj.Metadata)
# print(Tag.list())

#===============================================================================
# Deployment
#===============================================================================
# print(Deployment.list())
# dp = Deployment('d32fd7df-d689-4db0-a198-98eeb76291d9')
# print(dp)
# print(dp.Actions)
# print(dp.Action('PowerOff'))
# print(dp.Action('PowerOff').Request())
# print(dp.Resources)
# rsc = dp.Resource('5c9a4e4f-56e0-40f6-bc0c-c511ccb97b03')
# print(rsc)
# print(rsc.Actions)
# print(rsc.Action('PowerOff'))
# print(rsc.Action('PowerOff').Request())
# print(Deployment.CheckName('asdf'))
# print(Deployment.CheckName('deployment_d32fd7df-d689-4db0-a198-98eeb76291d9'))
# print(Deployment.Filter.list())
# print(Deployment.Filter('requestedBy'))

#===============================================================================
# Blueprint
#===============================================================================
# print(Blueprint.list())
# bp = Blueprint('6df07cf3-ca79-4091-beb8-24f7792bcc6e')
# print(bp)
# print(bp.Input)
# print(bp.Versions)
# print(bp.Version('1'))
