# Dynatrace Deployment Module

Send deployment information from deployments with Ansible directly to Dyntrace as custom deployment event information.


## Usage in a playbook

```
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

## Structure

```
play.yml
[library]
  |_ dynatrace_deployment.py
  |_ dynatrace_comment.py
```

## Test runs

Put Dynatrace module in a library folder and a ```play.yml``` in the parent folder.
Then start the sample ```play.yml``` from the bash. This will automatically load the modules from the ```library``` folder.
Add ```-v``` or ```-vvv``` for verbose debugging output.

```
$ ansible-playbook play.yml
```



