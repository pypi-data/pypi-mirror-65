# gconf

Managing a config globally throughout a Python application

## Overview

With gconf, yaml configuration files can be loaded on module-scope
such that its values can be accessed from anywhere in a running application.

## Usage

### Loading yaml files

One or more yaml configuration files are loaded globally from path-like objects,
usually in a program's main function.
The resulting configuration is an overlay of all loaded configurations
with those that were loaded later taking precedence.

Loading a single config file:
```python
gconf.load('conf.yml')
```

Loading multiple config files at once:
```python
gconf.load('conf1.yml', 'conf2.yml')
```

Loading multiple config files one after the other:
```python
gconf.load('conf1.yml')
gconf.load('conf2.yml')
```

The two examples above produce an identical result.
In both cases `config2` takes precedence over `config1` and overrides its values.

Each invocation of `load` returns a list of all paths that have actually been loaded.

Loading the first config from a list of paths:
```python
gconf.load_first('conf1.yml', 'conf2.yml')
```

If `conf1.yml` exists, it is loaded and `conf2.yml` is ignored.
if `conf1.yml` does not exist, `conf2.yml` is loaded.

`load_first` returns the path that has actually been loaded.

All loading functions raise a `FileNotFoundError` if no file is found.
This can be prevented by setting the keyword-argument `required=False`.


### Manually adding values

A dict can be added to the config from within the application.
This is equivalent to loading a config file with the same content
and overrides values if they are already present or adds them if not.

```python
gconf.add({'parent': {'child': 'new child'}})
```

Warning: using this functionality, it is possible to the gconf module as a store for global variables.
Global variables are a code smell and should not be used!
Please use the `gconf.add()` function only if you know exactly what you are doing.


### Accessing config values

There are several ways of addressing the values that are stored in the config,
all of them using the module-level `get` method.

Dot-notation
```python
gconf.get('parent.child.some value')
```

String arguments
```python
gconf.get('parent', 'child', 'some value')
```

A mix of both
```python
gconf.get('parent.child', 'some value')
```

Top-level item as dictionary
```python
gconf.get()['parent']['child']['some value']
```

Some intermediate item as dictionary
```python
gconf.get('parent')['child']['some value']
```

To access list items, simply use their index in the path
```python
gconf.get('list.3')
```

#### Default value

The `get` method accepts a `default` argument, which is returned
if the specified item does not exist:
```python
gconf.get('non-existing', default=default_value)
```
This even works for falsey values like `False`, `None` or the empty string.

### Errors

If an attempt is made at loading non-existing files and `required=True` (the default), an `FileNotFoundError` is raised.

If no `default` is provided, an attempt to access a non-existing item raises a `KeyError`.

### Temporary override

Parts of the config can be temporarily overridden through a context manager.
Pass it a dictionary that overlays the existing one:
```python
with gconf.override_conf({'parent': {'child': 'override_value'}}):
    gconf.get('parent.child')  # => 'override_value'
gconf.get('parent.child')  # => 'original_value'
```

To temporarily remove parts of the config the `DELETED` constant can be used:
```python
with gconf.override_conf({'parent': {'child': gconf.DELETED}}):
    gconf.get('parent.child')  # => KeyError
gconf.get('parent.child')  # => 'original_value'
```

### Resetting

The global gconf dict can be completely reset.

```python
gconf.reset()
```