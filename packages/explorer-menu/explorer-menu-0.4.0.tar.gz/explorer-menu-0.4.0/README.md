Explorer Menu
========================================================
**A python module to help creating explorer menus for Windows Explorer.**

How to use
========================================================
### Defining items

Items can either be:
 - **Action items** - items with a command associated to them

```python
node('Label', 'cmd.exe /K echo action')
```

 - **Container items** - items that may contain other container items and/or action items

```python
node('Root Label', node(...), node(...), ...)
```

### Registering items

Simply call the `register` method of any item and it will be registered, along with all children items:

```python
node('Label', 'cmd.exe /K echo action').register()

node('Root Label', node(...), node(...), node(...)).register()
```

After items are registered you will be able to find them by right clicking
in an empty area of any folder of your Windows Explorer.

### Removing items

Simply call the `remove` method of any item and it will be removed, along with all children items:
```python
node('Label', 'cmd.exe /K echo action').remove()

node('Root Label', node(...), node(...), node(...)).remove()
```

### Building commands

You can also use the `cmd(command, keep_cmd_window=False)` method to create commands:
```python
from explorermenu import cmd

# explicitly invoking cmd.exe
node('Label', 'cmd.exe /K echo action')

# same as above, but building command with cmd() method
node('Label', cmd('echo action', keep_cmd_window=True))
```

### Example:
```python
from explorermenu.menu_items import node
from explorermenu import cmd

# a single action item
single_action_item = node('Root action', cmd('echo Root action', keep_cmd_window=True))

# a nested set of items
nested_set = \
    node('Root',
         node('Child 1',
              node('Grand child 1',
                   node('Grandgrand child 1', cmd('echo Grandgrand child 1 action', keep_cmd_window=True)),
                   node('Grandgrand child 2', cmd('echo Grandgrand child 2 action', keep_cmd_window=True)),
                   ),
              node('Grand child 2', cmd('echo Grand child 2 action', keep_cmd_window=True))
              ),
         node('Child 2', cmd('echo Child 2 action', keep_cmd_window=True)),
         )

# Register items
single_action_item.register()
nested_set.register()

# Remove items
single_action_item.remove()
nested_set.remove()
```
Version
========================================================
### v0.4.0
