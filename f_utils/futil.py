#!/usr/bin/env python3 

import os 
import subprocess 
import json 

class Futil :
   
    def get_requirements (self , json_file): 
        if os.path.exists(json_file) and os.path.getsize(json_file)> 0 : 
            return json.load(open(json_file)) 
        else:raise FileNotFoundError("the file is missing or empty") 

    def extract_needed_data(self ,d_obj, key) : 
        assert key in d_obj.keys()
        f_std = os.popen(d_obj[key]).read() 
        r_tabs = f_std.replace("\t" ,"") 
        r_scap = r_tabs.replace("\n" ,"") 
        f_stand_desc=r_scap.split(":")[0x005]
        essential_data = f_stand_desc.split(" ") 
        return essential_data[0] , int(essential_data[2])

    def f_mid(self ,d_obj , check_keys) : 
        return (False,True)[check_keys in d_obj.values()] 
    

    def get_current_os_last_release (self , d_obj ) : 
        actuall_release = d_obj["CURRENT_VERSION_RELEASE"]
        current_os_release = self.extract_needed_data(d_obj  ,"CMD_RELEASE_MOD")[1] 
        #calculate depth release 
        release_depht= int(actuall_release)-int(current_os_release)
        if release_depht == 0x0:return  0x0 
        if release_depht  > 0x0:return  release_depht


    
    def fd_ops (self , cmd) : 
        process_status = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True)
        return_code_status = process_status.wait() 
        assert return_code_status == 0x0 
        return return_code_status 
   
    def fd_refresh(self) :
        return self.fd_ops("sudo dnf install dnf-plugin-system-upgrade")
    

    def fd_update_plugin(self) : 
        return self.fd_ops("sudo dnf install dnf-plugin-system-upgrade")

    
    def fd_pkg_up (self,d_obj_cid,comming_up_release) :
        if comming_up_release > int(d_obj_cid):raise ValueError("A new release has not set yet")
        initial_cmd ="sudo dnf system-upgrade download --refresh --releasever=? --setopt='module_platform_id=platform:f?'" 
        up_to.replace("?" , comming_up_release) 
        return self.fd_ops(up_to) 
    def fd_reboot(self): 
        return self.fd_ops("sudo dnf system-upgrade reboot")     
