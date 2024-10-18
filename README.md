# AI on IBM Power Playbooks

## Description

This repository contains Ansible playbooks helping to set up IBM Power environments for running AI workloads on them.


## Usage

If Ansible is not already installed on your local machine, you can install it via ([more information](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)):

```shell
pip install ansible
```

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
- **model_repository** (*string*): Huggingface repository name, e.g. `QuantFactory/Meta-Llama-3-8B-GGUF`.
- **model_file** (*string*): File to download from given `model_repository`, e.g. `Meta-Llama-3-8B.Q8_0.gguf`.
- **python_version** (*string*): Python version number, e.g. `3.11`.
- **working_directory** (*string*): Path to the working directory. Will be created if it does not exist.
- **llama_cpp_args** (*dictionary*): Key-value pairs passed to `llama-server` in the format `-KEY VALUE`. For parameters without additional value, like `-v`, leave the value blank.
- **llama_cpp_argv** (*dictionary*): Key-value pairs passed to `llama-server` in the format `--KEY VALUE`. For parameters without additional value, like `--verbose`, leave the value blank.
- **uvicorn_cpp_args** (*dictionary*): Key-value pairs passed to `uvicorn` in the format `-KEY VALUE`. For parameters without additional value, like `-v`, leave the value blank.
- **uvicorn_cpp_argv** (*dictionary*): Key-value pairs passed to `uvicorn` in the format `--KEY VALUE`. For parameters without additional value, like `--verbose`, leave the value blank.
