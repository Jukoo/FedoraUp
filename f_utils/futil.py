#!/usr/bin/env python3 

import os 
import subprocess 
import time
import json
import sys 

class Futil :
   
    def get_requirements (self , json_file): 
        if os.path.exists(json_file) and os.path.getsize(json_file)> 0 : 
            return json.load(open(json_file)) 
        else:
            raise FileNotFoundError("the file is missing or empty") 

    def extract_needed_data(self ,d_obj, key) : 
        assert key in d_obj.keys()
        f_std = os.popen(d_obj[key]).read() 
        # parsing f_std output 
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
        return return_code_status 
   
    def fd_refresh(self) :
        assert self.fd_ops("sudo dnf upgrade --refresh") == 0x0
        return self.fd_ops("sudo dnf install --refresh")
    

    def fd_update_plugin(self) : 
        assert self.fd_ops("sudo dnf install dnf-plugin-system-upgrade") == 0x0 
        return self.fd_ops("sudo dnf install dnf-plugin-system-upgrade") 


    def fd_pkg_up (self,d_obj_cid,comming_up_release) : 
        if comming_up_release > int(d_obj_cid):raise ValueError("A new release has not set yet")
        initial_cmd ="sudo dnf system-upgrade download --refresh --releasever=?" #--setopt='module_platform_id=platform:f?'" 
        up_to = initial_cmd.replace("?" , comming_up_release) 
        return self.fd_ops(up_to) 

    def import_rpm_gpg_key (self , current_release_version) :   
        rpm_cmd = "sudo rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-?-primary" 
        jump_next_branch_release  = int(current_os_release) + 1  
        rpm_gpg = rpm_cmd.replace("?" , jump_next_branch_release)  
        assert self.fd_ops(rpm_gpg) == 0x0 
        return self.fd_ops(rpm_gpg) 


    def fd_reboot(self): 
        return self.fd_ops("sudo dnf system-upgrade reboot")  


    def power_source(self) : 
        # check if acpi is available on the current os  
        try : 
            assert self.fd_ops("acpi") == 0x0 
            bat_stat = os.popen("acpi").read().replace("\n" , "")
            unk = bat_stat.split(":")[1] 
            status , percentage_unit = unk.split(",")[0:2]
            print("batterie status :{}".format(status))
            print("power bettery   :{}".format(percentage_unit)) 
            power_lvl = percentage_unit.replace("%" , "")
            return (int(power_lvl),status) ;   
        except AssertionError as no_acpi_support : 
            print("your  computer haven't acpitool package available !! try sudo dnf isntall acpitool")
    
    def power_watcher (self) : 
       power_lvl , status = self.power_source() 
       if power_lvl < 0x45 and status == " Discharging" : 
           print("please charge your computer or plug it into a power outlet to continue...") 
           time.sleep(5)
           sys.exit(1)

       # sometimes some computers fail to have the state of the battery 
       if power_lvl  > 0x45 or status == " Charging" or status == " Unknown" : return True 

    def msg_warn (self) : 
        return""" 
        before launching the program make sure you have enough load battery on your computer 
        because it ' ll take a few moments 
        """

