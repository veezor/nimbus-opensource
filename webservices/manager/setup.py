from cx_Freeze import setup, Executable


import sys
sys.path.append("../libs/")





setup(
        name = "NimbusManager",
        version = "1.4",
        description = "Nimbus Manager",
        executables = [ Executable("bin/nimbus-manager", targetName="nimbus-manager")],
        options = { "build_exe": 
                    { "build_exe" : "binary",
                        "compressed" :  True, 
                        "silent" : True,
                        "optimize" :  "1", 
                        "create_shared_zip" :  False,
                        "include_in_shared_zip" : False,   
                        "excludes" : ["Tkinter","_tkinter"],
                        "append_script_to_exe" :  True,
                        "packages": [ "networkutils", "netifaces"]  }}
)
