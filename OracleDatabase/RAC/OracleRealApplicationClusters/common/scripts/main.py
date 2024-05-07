#!/usr/bin/python3

#############################
# Copyright (c) 2024, Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl
# Author: paramdeep.saini@oracle.com
############################

"""
This is the main file which calls other file to setup the sharding.
"""

from oralogger import *
from orafactory import *
from oraenv import *
from oracommon import *


def main(): 

   # Checking Comand line Args
   opts=""
   try:
      opts, args = getopt.getopt(sys.argv[1:], '', ['help','resetpassword=','delracnode=','addtns=', 'checkracinst=', 'checkgilocal=','checkdbrole=','checkracdb=','checkconnstr=','checkpdbconnstr=','setupdblsnr=','setuplocallsnr='])
   except getopt.GetoptError:
      pass
  
   # Initializing oraenv instance 
   oenv=OraEnv()
   file_name  = os.path.basename(__file__)
   funcname = sys._getframe(1).f_code.co_name

   log_file_name = oenv.logfile_name("NONE")

   # Initialiing logger instance
   oralogger  = OraLogger(log_file_name)
   console_handler = CHandler()
   file_handler = FHandler()
   stdout_handler = StdHandler()
   # Setting next log handlers
   stdout_handler.nextHandler = file_handler
   file_handler.nextHandler = console_handler
   console_handler.nextHandler = PassHandler()

   ocommon = OraCommon(oralogger,stdout_handler,oenv)

   for opt, arg in opts:
      if opt in ('--help'):
         oralogger.msg_ = '''{:^17}-{:^17} : You can pass parameter --help'''
         stdout_handler.handle(oralogger)
      elif opt in ('--resetpassword'):
           file_name = oenv.logfile_name("RESET_PASSWORD")   
           oralogger.filename_ =  file_name
           ocommon.log_info_message("=======================================================================",file_name)
           oenv.add_custom_variable("RESET_PASSWORD",arg)
      elif opt in ('--delracnode'):
           file_name = oenv.logfile_name("DEL_PARAMS")
           oralogger.filename_ =  file_name
           ocommon.log_info_message("=======================================================================",file_name)
           oenv.add_custom_variable("DEL_PARAMS",arg)
           oenv.add_custom_variable("CUSTOM_RUN_FLAG","true")
           oenv.add_custom_variable("DEL_RACHOME","true")
           oenv.add_custom_variable("DEL_GIHOME","true") 
           if ocommon.check_key("OP_TYPE",oenv.get_env_dict()):
              oenv.update_key("OP_TYPE","racdelnode")
           else:
              oenv.add_custom_variable("OP_TYPE","miscops")
      elif opt in ('--addtns'):
           file_name = oenv.logfile_name("ADD_TNS")
           oralogger.filename_ =  file_name
           ocommon.log_info_message("=======================================================================",file_name)
           oenv.add_custom_variable("TNS_PARAMS",arg)
           oenv.add_custom_variable("CUSTOM_RUN_FLAG","true")
           if ocommon.check_key("OP_TYPE",oenv.get_env_dict()):
              oenv.update_key("OP_TYPE","racdelnode")
           else:
              oenv.add_custom_variable("OP_TYPE","miscops") 
      elif opt in ('--checkracinst'):
           file_name = oenv.logfile_name("CHECK_RAC_INST")
           oralogger.filename_ =  file_name
           ocommon.log_info_message("=======================================================================",file_name)
           oenv.add_custom_variable("CHECK_RAC_INST",arg)
           oenv.add_custom_variable("CUSTOM_RUN_FLAG","true")
           if ocommon.check_key("OP_TYPE",oenv.get_env_dict()):
              oenv.update_key("OP_TYPE","miscops")
           else:
              oenv.add_custom_variable("OP_TYPE","miscops")
      elif opt in ('--checkgilocal'):
           file_name = oenv.logfile_name("CHECK_GI_LOCAL")
           oralogger.filename_ =  file_name
           ocommon.log_info_message("=======================================================================",file_name)
           oenv.add_custom_variable("CHECK_GI_LOCAL",arg)
           oenv.add_custom_variable("CUSTOM_RUN_FLAG","true")
           if ocommon.check_key("OP_TYPE",oenv.get_env_dict()):
              oenv.update_key("OP_TYPE","miscops")
           else:
              oenv.add_custom_variable("OP_TYPE","miscops")
      elif opt in ('--checkracdb'):
           file_name = oenv.logfile_name("CHECK_RAC_DB")
           oralogger.filename_ =  file_name
           ocommon.log_info_message("=======================================================================",file_name)
           oenv.add_custom_variable("CHECK_RAC_DB",arg)
           oenv.add_custom_variable("CUSTOM_RUN_FLAG","true")
           if ocommon.check_key("OP_TYPE",oenv.get_env_dict()):
              oenv.update_key("OP_TYPE","miscops")
           else:
              oenv.add_custom_variable("OP_TYPE","miscops")
      elif opt in ('--checkdbrole'):
           file_name = oenv.logfile_name("CHECK_DB_ROLE")
           oralogger.filename_ =  file_name
           ocommon.log_info_message("=======================================================================",file_name)
           oenv.add_custom_variable("CHECK_DB_ROLE",arg)
           oenv.add_custom_variable("CUSTOM_RUN_FLAG","true")
           if ocommon.check_key("OP_TYPE",oenv.get_env_dict()):
              oenv.update_key("OP_TYPE","miscops")
           else:
              oenv.add_custom_variable("OP_TYPE","miscops")
      elif opt in ('--checkconnstr'):
           file_name = oenv.logfile_name("CHECK_CONNECT_STR")
           oralogger.filename_ =  file_name
           ocommon.log_info_message("=======================================================================",file_name)
           oenv.add_custom_variable("CHECK_CONNECT_STR",arg)
           oenv.add_custom_variable("CUSTOM_RUN_FLAG","true")
           if ocommon.check_key("OP_TYPE",oenv.get_env_dict()):
              oenv.update_key("OP_TYPE","miscops")
           else:
              oenv.add_custom_variable("OP_TYPE","miscops")
      elif opt in ('--checkpdbconnstr'):
           file_name = oenv.logfile_name("CHECK_PDB_CONNECT_STR")
           oralogger.filename_ =  file_name
           ocommon.log_info_message("=======================================================================",file_name)
           oenv.add_custom_variable("CHECK_PDB_CONNECT_STR",arg)
           oenv.add_custom_variable("CUSTOM_RUN_FLAG","true")
           if ocommon.check_key("OP_TYPE",oenv.get_env_dict()):
              oenv.update_key("OP_TYPE","miscops")
           else:
              oenv.add_custom_variable("OP_TYPE","miscops")
      elif opt in ('--setupdblsnr'):
           file_name = oenv.logfile_name("SETUP_DB_LSNR")
           oralogger.filename_ =  file_name
           ocommon.log_info_message("=======================================================================",file_name)
           oenv.add_custom_variable("NEW_DB_LSNR_ENDPOINTS",arg)
           oenv.add_custom_variable("CUSTOM_RUN_FLAG","true")
           if ocommon.check_key("OP_TYPE",oenv.get_env_dict()):
              oenv.update_key("OP_TYPE","miscops")
      elif opt in ('--setuplocallsnr'):
           file_name = oenv.logfile_name("SETUP_LOCAL_LSNR")
           oralogger.filename_ =  file_name
           ocommon.log_info_message("=======================================================================",file_name)
           oenv.add_custom_variable("NEW_LOCAL_LISTENER",arg)
           oenv.add_custom_variable("CUSTOM_RUN_FLAG","true")
           if ocommon.check_key("OP_TYPE",oenv.get_env_dict()):
              oenv.update_key("OP_TYPE","miscops")
           else:
              oenv.add_custom_variable("OP_TYPE","miscops")
      else:
         pass

   # Initializing orafactory instances   
   oralogger.msg_ = '''{:^17}-{:^17} : Calling OraFactory to start the setup'''.format(file_name,funcname)
   stdout_handler.handle(oralogger)
   orafactory = OraFactory(oralogger,stdout_handler,oenv,ocommon)
   
   # Get the ora objects
   ofactory=orafactory.get_ora_objs()

   # Traverse through returned factory objects and execute the setup function
   for obj in ofactory:
       obj.setup()
    
# Using the special variable  
if __name__=="__main__": 
    main() 
