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

For an example configuration, see the [example-inventory.yml](example-inventory.yml) file.

