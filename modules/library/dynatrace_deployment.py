#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2018 Juergen Etzlstorfer (Dynatrace) <juergen.etzlstorfer@dynatrace.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: dynatrace_deployment
version_added: "1.2"
author: "Juergen Etzlstorfer (@jetzlstorfer)"
short_description: Notify Dynatrace about new deployments
description:
   - Push deployment information to Dynatrace (see https://www.dynatrace.com/support/help/dynatrace-api/events/how-do-i-push-events-from-3rd-party-systems/)
options:
  tenant_url:
    description:
      - Tenant URL for the Dynatrace Tenant
    required: true
  api_token:
    description:
      - Dynatrace API Token
    required: true
  attach_rules:
    description:
      - Attach rules A complex structure that contains attachment rules that define which monitored entities the event is to be attached to.
    required: true
  entity_ids:
    description:
      - Entity Ids of the affected entities for this deployment
    required: false
  deploymentName:
    required: true
  deploymentProject:
    required: false
  deploymentVersion:
    description:
      - A deployment version number
    required: false
  remediationAction:
    description:
      - A remediation action in case Dynatrace detects issues related to this deployment
    required: false

requirements: []
'''

EXAMPLES = '''
- dynatrace_deployment:
    tenant_url: https://mytenant.live.dynatrace.com
    api_token: XXXXXXXX
    attach_rules:
      tagRule:
        meTypes: 'SERVICE'
        tags: 'my-service-tag'
    remediationAction: 'url-to-remediation'
    deploymentVersion: '2.0'
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url
from ansible.module_utils.six.moves.urllib.parse import urlencode
import ast
import json

# ===========================================
# Module execution.
#


def main():

  module = AnsibleModule(
      argument_spec=dict(
          tenant_url=dict(required=True),
          api_token=dict(required=True),
          attach_rules=dict(required=True),
          deploymentVersion=dict(required=True),
          deploymentName=dict(required=True),
          deploymentProject=dict(required=False),
          source=dict(required=False),
          remediationAction=dict(required=False),
          customProperties=dict(required=False)
      ),
      # required_one_of=[['app_name', 'application_id']],
      supports_check_mode=True
  )

  # build list of params
  params = {}

  for item in ["deploymentVersion", "remediationAction", "deploymentName", "deploymentProject", "source", "customProperties"]:
    if module.params[item]:
      params[item] = module.params[item]

  params["eventType"] = "CUSTOM_DEPLOYMENT"
  
  ### parse attach rules
  attachRules={}
  attachRulesVars = ast.literal_eval(module.params['attach_rules'])

  entityIdsArr={}
  if "entity_ids" in attachRulesVars:
    entityIdsArr=attachRulesVars["entity_ids"].split(',')
    attachRules["entityIds"] = entityIdsArr

  tagRule={}
  if "tagRule" in attachRulesVars:
    tagRule=attachRulesVars["tagRule"]
    attachRules["tagRule"] = tagRule

  params["attachRules"] = attachRules
  if "source" not in params:
    params["source"] = "Ansible"
  #if "source" in module.params and module.params["source"] is not None:
  #  params["source"] = module.params["source"]
  

  
  customProperties={}
  if params["customProperties"]:
    customPropsArr = ast.literal_eval(module.params['customProperties'])
    params["customProperties"] = customPropsArr


  # If we're in check mode, just exit pretending like we succeeded
  if module.check_mode:
    module.exit_json(changed=True)

  # Send the deployment info to Dynatrace
  dt_url = module.params["tenant_url"] + "/api/v1/events/" #?Api-Token=" + module.params["api_token"]
  #data = urlencode(params)
  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Api-Token ' + module.params['api_token']
  }
  
  ###### FAIL FOR DEBUG PURPOSES - TO INSPECT PAYLOAD #####
  #module.fail_json(msg=json.dumps(params))
  #########################################################
  
  ####
  # SEND DEPLOYMENT EVENT TO DYNATRACE
  ####
  try:
    response, info = fetch_url(module, dt_url, data=json.dumps(params), headers=headers)
    
    if info['status'] in (200, 201):
      #module.exit_json(changed=True,meta=info)
      module.exit_json(changed=True)
    elif info['status'] == 401:
      module.fail_json(msg="Token Authentification failed.")
    else:
      module.fail_json(msg="Unable to send deployment event to Dynatrace: %s" % info)
  except:
    e = get_exception()
    module.fail_json(msg="Failure: ")

if __name__ == '__main__':
    main()
