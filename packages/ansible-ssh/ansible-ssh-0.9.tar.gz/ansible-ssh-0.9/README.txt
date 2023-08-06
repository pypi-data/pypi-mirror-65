Adds interactive SSH capabilities to Ansible.  

usage: ansible-ssh [-h] [--inventory INVENTORY] [--key-file KEYFILE]
                   [--user USER] [--verbose] [--become]
                   host

positional arguments:
  host                  the host to ssh into

optional arguments:
  -h, --help            show this help message and exit
  --inventory INVENTORY, -i INVENTORY
                        ansible inventory file to use instead of the one
                        defined in ansible.cfg
  --key-file KEYFILE, -k KEYFILE
                        ssh private key file to use instead of the default for
                        the user
  --user USER, -u USER, -l USER
                        override the user defined in ansible inventory file
  --verbose, -v         pass verbose flag to ssh command
  --become, -b          ssh as root instead of the inventory-supplied account
