# Jinja2 Ansible Filters

## Overview

Jinja2 Ansible Filters is a port of the ansible filters provided by Ansible's templating engine.

This repository is not inteded to supplant ansible functionality however there are a lot of filters ansible provides that are not present in upstream Jinja2 so you may find these helpful.

### Included filters

- b64decode
- b64encode
- basename
- bool
- checksum
- comment
- dirname
- expanduser
- expandvars
- extract
- fileglob
- flatten
- from_json
- from_yaml
- from_yaml_all
- ans_groupby
- hash
- mandatory
- md5
- quote
- ans_random
- random_mac
- realpath
- regex_escape
- regex_findall
- regex_replace
- regex_search
- relpath
- sha1
- shuffle
- splitext
- strftime
- subelements
- ternary
- to_datetime
- to_json
- to_nice_json
- to_nice_yaml
- to_uuid
- to_yaml
- type_debug
- win_basename
- win_dirname
- win_splitdrive

### Renamed filters

Due to naming conflicts with Jinja2 builtin filters, these filters have been prefixed with ans_

- groupby
- random

so:

- ans_groupby
- ans_random

Additionally any filter naming collisions detected at runtime will be renamed to ans_filter and a warning message raised for each.

Several heavy filters have been omitted due to their extensive dependency on ansible core:

### Excluded Filters

- combine
- get_encrypted_password
- dict2items
- items2dict

## Install

`pip install jinja2-ansible-filters`

## Usage

### Typical usage with jinja2

```python
  from jinja2 import Environment

...
  env = Environment(extensions=['jinja2_ansible_filters.AnsibleCoreFiltersExtension'])
...
# OR
  from jinja2_ansible_filters import AnsibleCoreFiltersExtension
  env = Environment(extensions=[AnsibleCoreFiltersExtension])
...
```

### Include into cookiecutter

cookiecutter.json

```json
{
  "_extensions": ["jinja2_ansible_filters.AnsibleCoreFiltersExtension"]
}
```

## License

Due to multiple licenses in the Ansible source the licenses have both been included in LICENSE as well as proper attribution. Additionally license stubs where preserved with the source files they covered in the origional ansible repository.
