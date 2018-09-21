# Dynatrace Modules

This project consists of two modules that send either deployment information or comments for a problem ticket to Dynatrace.


### Deployment


Send deployment information from deployments with Ansible directly to Dyntrace as custom deployment event information.


Usage:
```yaml
dynatrace_deployment:
  tenant_url: 'https://your-url.com'
  api_token: 'your-api-token'
  attach_rules:
    tagRule: 
      meTypes: 'SERVICE'
      tags: 'ansible-deployment'
  deploymentVersion: '2.0'
  deploymentName: 'my name'
```

### Comments

Send a comment to a Dynatrace problem ticket with Ansible.

Usage:
```yaml
dynatrace_comment:
  tenant_url: 'https://your-url.com'
  api_token: 'your-api-token'
  problem_id: 'xxxx'
  comment: 'Problem remediation started'
  user: 'juergen'
```



## Structure

```
test-deployment.yml
test-comment.yml
[library]
  ↳ dynatrace_deployment.py
  ↳ dynatrace_comment.py
```

## Run tests

Put Dynatrace module in a library folder and a `playbook` file in the parent folder.
Then start the sample `playbook` from the bash. This will automatically load the modules from the `library` folder.
Add ```-v``` or ```-vvv``` for verbose debugging output.

```
$ ansible-playbook test-deployment.yml
$ ansible-playbook test-comment.yml -vvv 
```



