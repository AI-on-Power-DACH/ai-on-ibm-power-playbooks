# Milvus on IBM Power Playbooks

A sub collection of ansible playbooks for deploying the vector database [milvus](https://milvus.io/).

## Ways to run milvus:
- using a single container (docker or podman/oci)
- using three containers (docker composer)
- in a cluster (kubernetes/open shift)
- 

## Playbooks:
- `basic-milvus-podman`: 
    Installs milvus as a standalone podman pod.  Also copies the script [milvus_embed.sh](standalone_embed_ppc64le.sh) to manage the pods
- `prepare-pymilvus`: 
    Installs `pymilvus` and `sentence-transformers` into a mamba environment called `milvus` ready to connect to a running DB via python.
- `baremetal-milvus`:
    Install milvus and its required services `etcd` and `minio` on the remote LPAR without a container around them. Milvus documentation encourages the use of the container variant for standalone installations.

## Configuration

The following additional parameters can be specified in the inventory:

- **milvus_port** (integer): The port to expose milvus on
- **milvus_etcd_port** (integer): The port for milvus embedded etcd service 
- **auto_start** (boolean): whether the milvus pod should be started immediately.
- Also take a look at the root level README. Many parameters also apply here.

For an example configuration, see the [example-inventory.yml](example-inventory.yml) file in this directory.

### Baremetal

Since the baremetal installation does not run everything encapsulated in docker, more options apply here.
Additionally to the normal configuration the following parameters should also be configured:

- **go_path** (string/path): The path at which all things go will live (includes the bin/ subdir which will be added to $PATH)
- **go_version** (string):  The version of go to install.
- **cmake_path** (string/path):  The path for the cmake source and build artefacts. (agian bin/ will be added to path)
- **cmake_version** (string):   the version of cmake to install. Attention: This version must be compatible with milvus! See [example compatible configuration](#Comaptible-configuration)
- **etcd_version** (string):    The version of Etcd to install
- **etcd_executable_prefix** (string/path): The path into which all etcd executable will be copied (should already be in $PATH).
- TODO: add remianing from [Inventory](example-inventory.yml)
- TODO: add header comment to [build_milvus](baremetal/build_milvus.yml)

#### Compatible configuration

- Milvus: Version 2.4.15
- cmake: Version 3.30.5
- go: Version 1.23.3
- Milvus power patch: For min. Version 2.4.11
- Etcd Version: 3.5.17
- Minio Version: Latest
- Python Version: 3.11 (everything latest-1 should do)