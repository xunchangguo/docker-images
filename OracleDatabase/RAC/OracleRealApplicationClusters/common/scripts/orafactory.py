#!/usr/bin/python3

#############################
# Copyright (c) 2024, Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl
# Author: paramdeep.saini@oracle.com
############################

"""
 This file contains to the code call different classes objects based on setup type
"""

import os
import sys
sys.path.insert(0, "/opt/scripts/startup/scripts")


from oralogger import *
from oraenv import *
from oracommon import *
from oramachine import *
from oragiprov import *
from oragiadd import *
from orasshsetup import *
from oraracadd import *
from oraracprov import *
from oraracdel import *
from oramiscops import *

class OraFactory:
    """ 
    This is a class for calling child objects to setup RAC/DG/GRID/DB/Sharding based on OP_TYPE env variable.
      
    Attributes: 
        oralogger (object): object of OraLogger Class.
        ohandler (object): object of Handler class.
        oenv (object): object of singleton OraEnv class.
        ocommon(object): object of OraCommon class.
        ora_env_dict(dict): Dict of env variable populated based on env variable for the setup.
        file_name(string): Filename from where logging message is populated. 
    """
    def __init__(self,oralogger,orahandler,oraenv,oracommon):
        """
        This is a class for calling child objects to setup RAC/DG/GRID/DB based on OP_TYPE env variable.
    
        Attributes:
           oralogger (object): object of OraLogger Class.
           ohandler (object): object of Handler class.
           oenv (object): object of singleton OraEnv class.
           ocommon(object): object of OraCommon class.
           ora_env_dict(dict): Dict of env variable populated based on env variable for the setup.
           file_name(string): Filename from where logging message is populated.
        """
        self.ologger             = oralogger
        self.ohandler            = orahandler 
        self.oenv                = oraenv.get_instance() 
        self.ocommon             = oracommon
        self.ocvu                = OraCvu(self.ologger,self.ohandler,self.oenv,self.ocommon)
        self.osetupssh           = OraSetupSSH(self.ologger,self.ohandler,self.oenv,self.ocommon)
        self.ora_env_dict        = oraenv.get_env_vars() 
        self.file_name           = os.path.basename(__file__)
    def get_ora_objs(self):
        '''
        Return the instance of a classes which will setup the enviornment.

        Returns:
         ofactory_obj: List of objects  
        '''  
        ofactory_obj = []

        msg='''ora_env_dict set to : {0}'''.format(self.ora_env_dict)
        self.ocommon.log_info_message(msg,self.file_name) 

        msg='''Adding machine setup object in orafactory'''
        self.ocommon.log_info_message(msg,self.file_name)
        omachine=OraMachine(self.ologger,self.ohandler,self.oenv,self.ocommon,self.ocvu,self.osetupssh)         
        self.ocommon.log_info_message(msg,self.file_name) 
        ofactory_obj.append(omachine) 

        msg="Checking the OP_TYPE and Version to begin the installation"
        self.ocommon.log_info_message(msg,self.file_name)

        # Checking the OP_TYPE
        op_type=None
        if self.ocommon.check_key("CUSTOM_RUN_FLAG",self.ora_env_dict):
           if self.ocommon.check_key("OP_TYPE",self.ora_env_dict):
              op_type=self.ora_env_dict["OP_TYPE"]

        self.ocommon.populate_rac_env_vars()
        if self.ocommon.check_key("OP_TYPE",self.ora_env_dict):
           if op_type is not None:
              self.ocommon.update_key("OP_TYPE",op_type,self.ora_env_dict)
           msg='''OP_TYPE variable is set to {0}.'''.format(self.ora_env_dict["OP_TYPE"])
           self.ocommon.log_info_message(msg,self.file_name)
        else:
           self.ora_env_dict=self.ocommon.add_key("OP_TYPE","nosetup",self.ora_env_dict)
           msg="OP_TYPE variable is set to default nosetup. No value passed as an enviornment variable."
           self.ocommon.log_info_message(msg,self.file_name)

         ## Calling this function from here to make sure INSTALL_NODE is set
        self.ocommon.update_gi_env_vars_from_rspfile()
        # Check the OP_TYPE value and call objects based on it value
        install_node,pubhost=self.ocommon.get_installnode()
        if install_node.lower() == pubhost.lower():
            if self.ora_env_dict["OP_TYPE"] == 'setupgrid':
               msg="Creating and calling instance to provGrid"
               ogiprov = OraGIProv(self.ologger,self.ohandler,self.oenv,self.ocommon,self.ocvu,self.osetupssh)
               self.ocommon.log_info_message(msg,self.file_name)
               ofactory_obj.append(ogiprov)
            elif self.ora_env_dict["OP_TYPE"] == 'setuprac':
               msg="Creating and calling instance to prov RAC DB"
               oracdb = OraRacProv(self.ologger,self.ohandler,self.oenv,self.ocommon,self.ocvu,self.osetupssh)
               self.ocommon.log_info_message(msg,self.file_name)
               ofactory_obj.append(oracdb)
            elif self.ora_env_dict["OP_TYPE"] == 'setupssh':
               msg="Creating and calling instance to setup ssh between computes"
               ossh = self.osetupssh 
               self.ocommon.log_info_message(msg,self.file_name)
               ofactory_obj.append(ossh)
            elif self.ora_env_dict["OP_TYPE"] == 'setupracstandby':
               msg="Creating and calling instance to setup RAC standby database"
               oracstdby = OraRacStdby(self.ologger,self.ohandler,self.oenv,self.ocommon,self.ocvu,self.osetupssh)
               self.ocommon.log_info_message(msg,self.file_name)
               ofactory_obj.append(oracstdby)
            elif self.ora_env_dict["OP_TYPE"] == 'gridaddnode':
               msg="Creating and calling instance to add grid"
               oaddgi = OraGIAdd(self.ologger,self.ohandler,self.oenv,self.ocommon,self.ocvu,self.osetupssh)
               self.ocommon.log_info_message(msg,self.file_name)
               ofactory_obj.append(oaddgi)
            elif self.ora_env_dict["OP_TYPE"] == 'racaddnode':
               msg="Creating and calling instance to add RAC node"
               oaddrac = OraRacAdd(self.ologger,self.ohandler,self.oenv,self.ocommon,self.ocvu,self.osetupssh)
               self.ocommon.log_info_message(msg,self.file_name)
               ofactory_obj.append(oaddrac)
            elif self.ora_env_dict["OP_TYPE"] == 'setupenv':
               msg="Creating and calling instance to setup the racenv"
               osetupenv = OraSetupEnv(self.ologger,self.ohandler,self.oenv,self.ocommon,self.ocvu,self.osetupssh)
               self.ocommon.log_info_message(msg,self.file_name)
               ofactory_obj.append(osetupenv)
            elif self.ora_env_dict["OP_TYPE"] == 'racdelnode':
               msg="Creating and calling instance to delete the rac node"
               oracdel = OraRacDel(self.ologger,self.ohandler,self.oenv,self.ocommon,self.ocvu,self.osetupssh)
               self.ocommon.log_info_message(msg,self.file_name)
               ofactory_obj.append(oracdel)
            elif self.ora_env_dict["OP_TYPE"] == 'miscops':
               msg="Creating and calling instance to perform the miscellenous operations"
               oramops = OraMiscOps(self.ologger,self.ohandler,self.oenv,self.ocommon,self.ocvu,self.osetupssh)
               self.ocommon.log_info_message(msg,self.file_name)
               ofactory_obj.append(oramops)
            else:
               msg="OP_TYPE must be set to {setupgrid|setuprac|setupssh|setupracstandby|gridaddnode|racaddnode}"
               self.ocommon.log_info_message(msg,self.file_name)
        elif install_node.lower() != pubhost.lower() and self.ocommon.check_key("CUSTOM_RUN_FLAG",self.ora_env_dict): 
            if self.ora_env_dict["OP_TYPE"] == 'miscops':
               msg="Creating and calling instance to perform the miscellenous operations"
               oramops = OraMiscOps(self.ologger,self.ohandler,self.oenv,self.ocommon,self.ocvu,self.osetupssh)
               self.ocommon.log_info_message(msg,self.file_name)
               ofactory_obj.append(oramops)
        else:
           msg="INSTALL_NODE {0} is not matching with the hostname {1}. Resetting OP_TYPE to nosetup.".format(install_node,pubhost)
           self.ocommon.log_info_message(msg,self.file_name)
           self.ocommon.update_key("OP_TYPE","nosetup",self.ora_env_dict)
         

        return ofactory_obj
