#!/usr/bin/python

# Copyright: (c) 2021, Dell Technologies
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

""" Ansible module for managing device on Dell Technologies (Dell) PowerFlex"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: bucket

short_description: ObjectScale Bucket module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.objectscale.plugins.module_utils.objectscale_client \
    import import_client
import json

def run_module():
    module_args = dict(
        endpoint=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True),
        insecure=dict(type='bool', required=False, default=True),
        name=dict(type='str', required=True),
        namespace=dict(type='str', required=True),
        owner=dict(type='str'),
        state=dict(required=True, type='str', choices=['present', 'absent']),
    )

    result = dict(
        changed=False,
        bucket_details=None
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    objectscale_client = import_client(module.tmpdir)

    state = module.params['state']
    endpoint = module.params['endpoint']
    username = module.params['username']
    password = module.params['password']
    insecure = module.params['insecure']
    name = module.params['name']
    namespace = module.params['namespace']
    owner = module.params['owner']

    bucket = None
    client = objectscale_client.client.ManagementClient(endpoint, username, password, insecure)
    try:
        bucket = client.get_bucket(name, namespace)
    except Exception as e:
        err_msg = str(e)
        if f"Unable to find entity with the given id {name}" not in err_msg:
            module.fail_json(msg=err_msg)

    if state == 'absent':
        if bucket is not None:
            try:
                client.delete_bucket(name, namespace, False)
                result['changed'] = True
                module.exit_json(**result)
            except Exception as e:
                msg = f"Failed to delete bucket {name} in namespace {namespace}, error: {str(e)}"
                module.fail_json(msg=msg)
        else:
            module.exit_json(**result)

    # To create
    if bucket is None:
        bucket = objectscale_client.bucket.Bucket()
        bucket.name = name
        bucket.namespace = namespace
        if owner is not None:
            bucket.owner = owner
        try:
            result['bucket_details'] = json.loads(str(client.create_bucket(bucket)))
            result['changed'] = True
            module.exit_json(**result)
        except Exception as e:
            msg = f"Failed to create bucket {name} in namespace {namespace}, error: {str(e)}"
            module.fail_json(msg=msg)

    # To update
    if owner is not None and owner != bucket.owner:
        try:
            bucket.owner = owner
            result['bucket_details'] = json.loads(str(client.update_bucket(bucket)))
            result['changed'] = True
            module.exit_json(**result)
        except Exception as e:
            msg = f"Failed to create bucket {name} in namespace {namespace}, error: {str(e)}"
            module.fail_json(msg=msg)
    
    # no change
    result['bucket_details'] = json.loads(str(bucket))
    module.exit_json(**result)
    

def main():
    run_module()


if __name__ == '__main__':
    main()
