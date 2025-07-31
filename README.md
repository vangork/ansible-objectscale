# Ansible Modules for Dell Technologies ObjectScale

Ansible ObjectScale POC

### Installation
1. install python objectscale SDK
    ```
    git clone -b ecs_4_0 https://github.com/vangork/objectscale-client.git
    pip install maturin
    maturin develop
    ```

2. build and install ansible objectscale modules
    ```
    ansible-galaxy collection build --force
    ansible-galaxy collection install dellemc-objectscale-0.0.1.tar.gz --force
    ```

### Run the playbook
It currently only have one `bucket` module supported.

```
ansible-playbook playbooks/modules/bucket.yml -v
```