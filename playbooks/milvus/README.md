# Milvus on IBM Power Playbooks

A sub collection of ansible playbooks for deploying the vector database [milvus](https://milvus.io/).

## Ways to run milvus:
- directly on a Linux host
- using a single container (docker or podman/oci)
- using three containers (docker compose)
- in a cluster (kubernetes/open shift)

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
Additionally to the normal configuration the following parameters can also be configured:

- **go_path** (string/path): The path at which all things go will live (includes the bin/ subdir which will be added to $PATH)
- **go_version** (string):  The version of go to install.
- **cmake_path** (string/path):  The path for the cmake source and build artefacts. (agian bin/ will be added to path)
- **cmake_version** (string):   the version of cmake to install. Attention: This version must be compatible with milvus! See [example compatible configuration](#comaptible-configuration)
- **etcd_version** (string):    The version of Etcd to install
- **etcd_executable_prefix** (string/path): The path into which all etcd executable will be copied (should already be in $PATH).
- **etcd_data_dir** (string/path): The path at which all data saved into etcd should be stored
- **minio_data_dir** (string/path): The path for all minio stored data.
- **minio_location** (string/path): The direct path for the minio binary (NOTE: Not a directory!), this should be inside $PATH.
- **milvus_dir** (string/path): The path at which milvus will be checked out and build.
                                 All non-builtin logs will also be placed directly into this directory.
- **milvus_version** (string):  the milvus version to built.
- **milvus_patch_version** (string):    The patch version which should be applied to the milvus source. Must be     
                                        compatible with the milvus_source, but the same patch may be used relevant 
                                        for multiple milvus versions.
- **milvus_dir** (string/path):     The location for the milvus. The sub-directory `git_repo` Should not exist before the playbook is run. 
                                    Other dirs, e.g. the `etcd_data_dir` might be located inside for a more semantical filestructure.
- **nproc** (integer):              The number of threads used for building milvus. Since milvus tends to be very complex,
                                    depending on the available resources, the build process might be killed by the OOM-killer
                                    Compiling with fewer threads may help in lowering resource usage. The build script will
                                    also retry the build up to 5 times, hoping, that this is enought due to cmake performing incremental builds.

#### Compatible configuration

- Milvus: Version 2.4.17
- cmake: Version 3.30.5
- go: Version 1.23.3
- Milvus power patch Version: 2.4.11
- Etcd Version: 3.5.17
- Minio Version: Latest
- Python Version: 3.11 (everything latest-1 should do)