# Ansible Modules for Dell Technologies ObjectScale

Ansible ObjectScale POC

### Installation

Build and install ansible objectscale modules
```
ansible-galaxy collection build --force
ansible-galaxy collection install dellemc-objectscale-0.0.1.tar.gz --force
```

### Run the playbook
It currently only have one `bucket` module supported.

```
ansible-playbook playbooks/modules/bucket.yml -v
```