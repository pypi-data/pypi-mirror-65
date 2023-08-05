import re
import winreg
import warnings
from typing import List, Union

_BACKGROUND_PATH = r'Software\Classes\Directory\Background'
_LIBRARY_PATH = r'Software\Classes\LibraryFolder\Background'


class _LabelValuePair:
    def __init__(self, label: str, value: str) -> None:
        self.label = label
        self.value = value


def prefix_by_index(index: int):
    index = index - 1
    a = ord('a')
    char_count = ord('z') - a + 1
    first = chr(int(index / char_count) + a)
    second = chr(int(index % char_count) + a)
    return f'{first}{second}'


class _MenuItem:
    def __init__(self,
                 label: str,
                 children: List['_MenuItem'],
                 label_values: List[_LabelValuePair],
                 subkey_path: str = None
                 ) -> None:
        def label_to_subkey(label_: str) -> str:
            label_ = re.sub(r'v\d+\.\d+\.\d+', '', label_).strip()
            return re.sub(r'\W+', '_', label_).lower()
        self.children = []
        self.label = label
        self.subkey_path = subkey_path if subkey_path else f'shell\\{label_to_subkey(label)}'
        self.label_values = label_values
        self.parent = None

        if children:
            for child in children:
                self.add_child(child)

    def set_parent(self, parent: '_MenuItem'):
        self.parent = parent

    def add_child(self, child: '_MenuItem') -> None:
        if isinstance(child, _MenuItem):
            self.children.append(child)
            child.set_parent(self)

    def get_full_subkey_path(self):
        subkey_list = [self.subkey_path]
        parent: _MenuItem = self.parent
        while parent:
            subkey_list.append(parent.subkey_path)
            parent = parent.parent
        return '\\'.join(filter(None, reversed(subkey_list)))

    def register(self, index: int = 0) -> None:
        if index > 0:
            prefix = prefix_by_index(index)
            self.subkey_path = self.subkey_path.replace('shell\\', f'shell\\{prefix}_')

        def register_at(root_shell: str, label_values: List[_LabelValuePair], subkey_path: str):
            subkey = '\\'.join([root_shell, subkey_path])
            item = winreg.CreateKey(winreg.HKEY_CURRENT_USER, subkey)
            for i in label_values:
                winreg.SetValueEx(item, i.label, 0, winreg.REG_SZ, i.value)
            winreg.FlushKey(item)

        full_subkey_path = self.get_full_subkey_path()

        register_at(_BACKGROUND_PATH, self.label_values, full_subkey_path)
        register_at(_LIBRARY_PATH, self.label_values, full_subkey_path)

        for i, child in enumerate(self.children):
            child.register(i + 1)

    def remove(self) -> None:
        def remove_from(root: int, subkey: str):
            try:
                hkey = winreg.OpenKey(root, subkey, access=winreg.KEY_ALL_ACCESS)
            except OSError:
                return
            while True:
                try:
                    child = winreg.EnumKey(hkey, 0)
                except OSError:
                    break
                remove_from(hkey, child)
            winreg.CloseKey(hkey)
            winreg.DeleteKey(root, subkey)

        remove_from(winreg.HKEY_CURRENT_USER, f'{_BACKGROUND_PATH}\\{self.subkey_path}')
        remove_from(winreg.HKEY_CURRENT_USER, f'{_LIBRARY_PATH}\\{self.subkey_path}')


class MenuContainerItem(_MenuItem):
    def __init__(self, label: str, children: List[_MenuItem] = None) -> None:
        mui_verb = _LabelValuePair('MUIVerb', label)
        subcommands = _LabelValuePair('subcommands', '')
        label_values = [
            mui_verb,
            subcommands
        ]
        super().__init__(label, children, label_values)


class MenuActionItem(_MenuItem):
    def __init__(self, label: str, command: str) -> None:
        self.command = command
        command_pair = _LabelValuePair('', self.command)
        command_menu_item = _MenuItem('', [], [command_pair], '\\command')
        label_values = [_LabelValuePair('', label)]
        super().__init__(label, [], label_values)
        super().add_child(command_menu_item)

    def add_child(self, child) -> None:
        warnings.warn("MenuActionItem wont add children")


def node(label: str, *children_or_command: Union[str, _MenuItem]) -> Union[MenuActionItem, MenuContainerItem]:
    is_action = len(children_or_command) == 1 and isinstance(children_or_command[0], str)

    if is_action:
        command = children_or_command[0]
        return MenuActionItem(label, command)

    if all(isinstance(child, _MenuItem) for child in children_or_command):
        children = list(children_or_command)
    else:
        children = []

    return MenuContainerItem(label, children)
