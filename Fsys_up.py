#!/usr/bin/env python3
# THIS SCRIPT ALLOWS YOU TO DO 
# A GLOBAL UPDATE FOR YOUR FEDORA 
# TO A NEW FRESH RELEASE VERSION 
# ------------
# *-WARNING-*| 
# ------------
# BACK UP your important data. 
# Every system change is potentially risky,[ BE PREPARED] 
#------------------------------------
# ▛▀▘▛▀▘▛▀▖▞▀▖▛▀▖▞▀▖        ▖▗▌ 
# ▙▄ ▙▄ ▌ ▌▌ ▌▙▄▘▙▄▌ ▌ ▌▛▀▖▄▙▖▌ 
# ▌  ▌  ▌ ▌▌ ▌▌▚ ▌ ▌ ▌ ▌▙▄▘ ▌ ▌ 
# ▘  ▀▀▘▀▀ ▝▀ ▘ ▘▘ ▘ ▝▀▘▌    ▝▀ 
#------------------------------------
import sys 
import time 
from f_utils.futil import Futil 

S_CL="\033[1;32m"
E_CL="\033[1;31m"
W_CL="\033[1;33m"
I_CL="\033[1;36m"
D_CL="\033[0m"

def main () : 

    fedo              = Futil()
    #@ look up the type architure system 
    fedo.archx64_support() 
    print(" {} {} {}".format (I_CL , fedo.msg_warn() , D_CL)) 
    time.sleep(3) 
    fedo.power_watcher() 
    cmd_ref           = fedo.get_requirements("f_cid.json")
    dist_name,curver  = fedo.extract_needed_data(cmd_ref,"CMD_RELEASE_MOD") 
    next_release      = fedo.get_current_os_last_release(cmd_ref) 
    trigger_reboot    = curver  

    if not fedo.f_mid(cmd_ref , dist_name) :
        print("""
        your running on {} distribution
        only {} fedora dist is allowed to run the upgrade 
                """.format(dist_name , cmd_ref["TARGET_DISTRO"]))
        sys.exit(1) 

    if next_release == 0x0 : 
        print("{}your current os is already up-to-date{}".format(S_CL , D_CL)) 
        print("{}your are running on {} {} {}".format(I_CL ,dist_name,curver,D_CL)) 
    else :
        print("{}your release version is [{}] and your are out of date{}".format(E_CL ,curver,D_CL))
        print("jumping {} version...".format(next_release))
        curver+=next_release
        try :
            assert fedo.fd_refresh()                                           == 0x0
            assert fedo.fd_update_plugin()                                     == 0x0 
            assert fedo.fd_pkg_up( cmd_ref["CURRENT_VERSION_RELEASE"],curver)  == 0x0 
            assert fedo.import_rpm_gpg_key(cmd_ref["CURRENT_VERSION_RELEASE"]) == 0x0  
            if trigger_reboot != curver :
                print("{} Reebooting ...{}".format(W_CL , D_CL)) 
                time.sleep(5)  
                assert fedo.fd_reboot() ==0x0       
        
        except  AssertionError as sys_up_broke : 
            print("{} connot do the upgrate to [{}]  {}".format(E_CL , curver , D_CL))
            sys.exit(2)
        
        except ValueError as v_err : 
            print("{}{}{}".format( W_CL, v_err ,D_CL))
            sys.exit(1)

if __name__=="__main__" : 
    main() 
