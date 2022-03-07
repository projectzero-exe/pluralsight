#!/usr/bin/env python

from yaml import safe_load
from netmiko import Netmiko


def main():
    """
    Execution starts here.
    """

    # Read the hosts file into structured data, may raise YAMLError
    with open("hosts.yml", "r") as handle:
        host_root = safe_load(handle)
    #print(host_root)

    # Iterate over the list of hosts (list of dictionaries)
    for host in host_root["production"]:

        # Load the host-specific VRF declarative state
        # with open(f"vars/commands_{host}.yml", "r") as handle:
        with open(f"vars/qc_commands.yml", "r") as handle:
            commands = safe_load(handle)

        # Create netmiko SSH connection handler to access the device
        # For a list of device types, check the source code:
        # github.com/ktbyers/netmiko/blob/develop/netmiko/ssh_dispatcher.py#L83
        conn = Netmiko(
            host=host["ip"],
            username="cisco",
            password="cisco",
            device_type="cisco_ios",
        )

        print(f"\nLogged into {conn.find_prompt()} successfully")

        # Iterate over list of commands, issue each one, and print
        # the results
        qc_path = "/home/ares/Desktop/ENAUT_LABS/pluralsight/enauto1/m3/qc_files/"
        qc_filename = f"{host['name']}.txt"
        with open(qc_path + qc_filename, "w") as f:            
            for command in commands["commands"]:
                result = conn.send_command(command)                
                f.write(f"\nBegin: {command}\n{'-' * 80}\n")
                f.write(result)
                f.write(f"\n\nEnd of {command}\n{'-' * 80}\n")
                # print(result)



if __name__ == "__main__":
    main()
