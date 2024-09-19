# AI on IBM Power Playbooks

## Description

This repository contains Ansible playbooks helping to set up IBM Power environments for running AI workloads on them.


## Usage

Make sure to adjust the example inventory file before using it.

```shell
ansible-playbook -i example-inventory.yml playbooks/basic-llama.cpp.yml
```


## Configuration

The following parameters can be specified in the inventory:

- **auto_start** (*bool*): If set to `true`, the llama.cpp server will be started by Ansible.
- **conda_dir** (*string*): Path is used as the `root_prefix` and `prefix` of Micromamba. Will be created if it does not exist.
- **detached** (*bool*): If set to `true`, the llama.cpp server is started in the background and the playbook can finish without terminating the process. Is ignored if `auto_start` is set to `false`.
- **micromamba_location** (*string*): Path to where the Micromamba binary gets stored.
- **python_version** (*string*): Python version number, e.g. `3.11`.
- **working_directory** (*string*): Path to the working directory. Will be created if it does not exist.
