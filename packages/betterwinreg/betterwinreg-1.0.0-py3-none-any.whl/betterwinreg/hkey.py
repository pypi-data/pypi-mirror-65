from __future__ import annotations

import winreg
from typing import Any


HKEY_IDS = {
    ('HKEY_LOCAL_MACHINE', 'HKLM'): winreg.HKEY_LOCAL_MACHINE,
    ('HKEY_CURRENT_CONFIG', 'HKCC'): winreg.HKEY_CURRENT_CONFIG,
    ('HKEY_CLASSES_ROOT', 'HKCR'): winreg.HKEY_CLASSES_ROOT,
    ('HKEY_USERS', 'HKU'): winreg.HKEY_USERS,
    ('HKEY_CURRENT_USER', 'HKCU'): winreg.HKEY_CURRENT_USER,
    ('HKEY_PERFORMANCE_DATA',): winreg.HKEY_PERFORMANCE_DATA,
    ('HKEY_DYN_DATA',): winreg.HKEY_DYN_DATA,
}


class Hkey:

    name: str
    id_: int

    def __init__(self, name: str) -> Hkey:
        self.name = self.get_full_name(name)
        self.id_ = self.find_id(name)
        if not self.id_:
            raise OSError('The specified hkey is not valid')

    @staticmethod
    def get_full_name(name: str) -> str:
        for names in HKEY_IDS.keys():
            if name in names:
                return names[0]

    @staticmethod
    def find_id(name: str) -> int:
        for names, id_ in HKEY_IDS.items():
            if name in names:
                return id_
        return None

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Hkey) and self.id_ == other.id_

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{str(self)}')"

    def __str__(self) -> str:
        return self.name
