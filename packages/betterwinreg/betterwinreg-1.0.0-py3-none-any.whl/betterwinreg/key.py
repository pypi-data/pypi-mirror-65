from __future__ import annotations

import winreg
from enum import IntEnum
from pathlib import PureWindowsPath
from typing import Any, Iterator, List, Dict, Union

from betterwinreg.hkey import Hkey
from betterwinreg.value import RegistryValue, RegistryValueType, get_registry_instance


class RegistryPath(PureWindowsPath):
    pass


class RegistryKey:

    class EnumValueReturnMembers(IntEnum):
        NAME = 0
        VALUE = 1
        TYPE = 2

    class QueryInfoReturnMembers(IntEnum):
        SUBKEYS_AMOUNT = 0
        VALUES_AMOUNT = 1
        LAST_MODIFICATION = 2

    class QueryValueReturnMembers(IntEnum):
        VALUE = 0
        TYPE = 1

    hkey: Hkey
    path: RegistryPath

    _handle: winreg.HKEYType = None
    _is_handle_readonly: bool = True

    @property
    def full_path(self) -> RegistryPath:
        return RegistryPath(self.hkey.name) / self.path

    @property
    def parent(self) -> RegistryKey:
        return RegistryKey.from_hkey_and_path(self.hkey, self.path.parent)

    @property
    def default_value(self) -> RegistryValue:
        return self['']

    @default_value.setter
    def default_value(self, value: RegistryValue) -> None:
        self[''] = value

    @default_value.deleter
    def default_value(self) -> None:
        del self['']

    def __init__(self, path: Union[str, RegistryPath] = None) -> None:
        if not path:
            return

        path = RegistryPath(path)

        # If path starts with 'Computer/', we remove it to standardize it
        path_parts = path.parts
        if path_parts[0] == 'Computer':
            path_parts = path_parts[1:]

        self.hkey = Hkey(path_parts[0])
        self.path = RegistryPath().joinpath(*path_parts[1:])

    @staticmethod
    def from_hkey_and_path(hkey: Hkey, path: RegistryPath) -> RegistryKey:
        key = RegistryKey()
        key.hkey = hkey
        key.path = path
        return key

    def is_key(self) -> bool:
        try:
            _ = self._make_handle(True)
        except FileNotFoundError:
            return False
        return True

    def create(self) -> None:
        winreg.CreateKeyEx(self.hkey.id_, str(self.path), 0)

    def delete(self, recursive: bool = True) -> None:
        if recursive:
            for subkey in self.subkeys():
                subkey.delete()
        winreg.DeleteKeyEx(self.hkey.id_, str(self.path))

    def flush(self) -> None:
        self._ensure_handle_exists(False)
        winreg.FlushKey(self._handle)

    def has_default_value(self) -> bool:
        return '' in self.values()

    def subkeys(self) -> List[RegistryKey]:
        from itertools import count

        self._ensure_handle_exists(True)
        subkeys = []
        try:
            for i in count():
                key_name = winreg.EnumKey(self._handle, i)
                key = RegistryKey.from_hkey_and_path(
                    self.hkey, self.path / key_name)
                subkeys.append(key)
        except OSError:
            return subkeys

    def values(self) -> Dict[RegistryKey]:
        from itertools import count

        self._ensure_handle_exists(True)
        values = {}
        try:
            for i in count():
                data = winreg.EnumValue(self._handle, i)
                name = data[self.EnumValueReturnMembers.NAME]
                value = data[self.EnumValueReturnMembers.VALUE]
                type_ = RegistryValueType(
                    data[self.EnumValueReturnMembers.TYPE])
                values.update({name: get_registry_instance(value, type_)})
        except OSError:
            return values

    def _make_handle(self, readonly: bool = True) -> winreg.HKEYType:
        access = winreg.KEY_READ if readonly else winreg.KEY_ALL_ACCESS
        return winreg.OpenKeyEx(self.hkey.id_, str(self.path), 0, access)

    def _ensure_handle_exists(self, readonly: bool = True) -> None:
        if not self._handle or (not readonly and self._is_handle_readonly):
            self._handle = self._make_handle(readonly)
        self._is_handle_readonly = readonly

    def __truediv__(self, other: Union[str, RegistryPath]) -> RegistryKey:
        return RegistryKey.from_hkey_and_path(self.hkey, self.path / other)

    def __len__(self) -> int:
        self._ensure_handle_exists(True)
        return winreg.QueryInfoKey(self._handle)[self.QueryInfoReturnMembers.VALUES_AMOUNT]

    def __getitem__(self, key: str) -> RegistryValue:
        self._ensure_handle_exists(True)
        try:
            data = winreg.QueryValueEx(self._handle, key)
            value = data[self.QueryValueReturnMembers.VALUE]
            type_ = RegistryValueType(data[self.QueryValueReturnMembers.TYPE])
            return get_registry_instance(value, type_)
        except FileNotFoundError as e:
            raise KeyError from e

    def __setitem__(self, key: str, value: Union[RegistryValue, None]) -> None:
        if not self.is_key():
            self.create()
        self._ensure_handle_exists(False)
        type_ = value.winreg_type if not value is None else RegistryValueType.NONE
        winreg.SetValueEx(self._handle, key,
                          0, type_, value)

    def __delitem__(self, key: str) -> None:
        self._ensure_handle_exists(False)
        winreg.DeleteValue(self._handle, key)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, RegistryKey) and other.hkey == self.hkey and other.path == self.path

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{str(self.full_path)}')"

    def __str__(self) -> str:
        return str(self.full_path)
