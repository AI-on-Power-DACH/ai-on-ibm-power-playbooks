# Milvus on IBM Power Playbooks

A sub collection of ansible playbooks for deploying the vector database [milvus](https://milvus.io/).


## Playbooks:
- `basic-milvus-podman`: 
    Installs milvus as a standalone podman pod.  Also copies the script [milvus_embed.sh](standalone_embed_ppc64le.sh) to manage the pods
- `prepare-pymilvus`: 
    Installs `pymilvus` and `sentence-transformers` into a mamba environment called `milvus` ready to connect to a running DB via python.

## Configuration

The following additional parameters can be specified in the inventory:

- **milvus_port:** The port to expose milvus on
- **milvus_etcd_port**: The port for milvus embedded etcd service 
- **auto_start**: Boolean, whther the milvus pod should be started immediately.
- Also take a look at the root level README. Many parameters also apply here.

For an example configuration, see the [example-inventory.yml](example-inventory.yml) file.

