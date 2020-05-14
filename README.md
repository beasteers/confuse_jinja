# Confuse - Jinja Variables
Simple Ansible-style variable parsing for Confuse config files using Jinja2.

## Install

```bash
pip install confuse_jinja
```

## Usage

```yaml
# config.yml
asdf:
  blah: asdf{{ C.other.thing }}
nested: '{{ C.asdf }}' # need to quote if you start with a '{'
other:
  thing: 456
```

```python
import confuse
import confuse_jinja
confuse_jinja.enable() # now you can use jinja2 templates inside your keys

config = confuse.Configuration('asdf')
config.set(confuse.load_yaml('config.yml'))

assert config['asdf']['blah'].get() == 'asdf456'
assert config['nested'].get() == {'blah': 'asdf456'}
```

## How it works
 - for any config values that are a string, render it as a jinja2 template
 - try to parse rendered string as python using ast functions graciously pulled from ansible's source code
    - if a valid python object (list, dict, etc.) can be parsed from the string the object will be returned, otherwise it will return as a string.

## TODO:
 - test in a yaml file (possible syntax errors)
 - enable on a config-by-config object basis instead of globally.
    - would need to replace `ConfigView.__getitem__` for a single Config
    - would require using `self.Subview` instead of global `Subview`
