# Dynatrace Deployment Module

## Usage

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

```
$ ansible-playbook play.yml
```


