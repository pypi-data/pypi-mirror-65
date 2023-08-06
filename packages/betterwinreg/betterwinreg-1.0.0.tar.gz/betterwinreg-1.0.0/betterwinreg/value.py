import winreg
from enum import IntEnum
from typing import Union, List, Type


# Manually write these to have autocomplete
class RegistryValueType(IntEnum):
    BINARY = winreg.REG_BINARY
    DWORD = winreg.REG_DWORD
    DWORD_BIG_ENDIAN = winreg.REG_DWORD_BIG_ENDIAN
    QWORD = winreg.REG_QWORD
    SZ = winreg.REG_SZ
    EXPAND_SZ = winreg.REG_EXPAND_SZ
    MULTI_SZ = winreg.REG_MULTI_SZ
    LINK = winreg.REG_LINK
    NONE = winreg.REG_NONE
    RESOURCE_LIST = winreg.REG_RESOURCE_LIST
    FULL_RESOURCE_DESCRIPTOR = winreg.REG_FULL_RESOURCE_DESCRIPTOR
    RESOURCE_REQUIREMENTS_LIST = winreg.REG_RESOURCE_REQUIREMENTS_LIST


class RegistryValue:

    winreg_type: RegistryValueType = None

    def __repr__(self) -> str:
        return f"{type(self).__name__}({super().__repr__()})"

    def __str__(self) -> str:
        if isinstance(self, str):
            return self
        else:
            return super().__repr__()


def get_registry_instance(value: Union[int, str, bytearray], winreg_type: RegistryValueType) -> RegistryValue:
    if value is None:
        return None

    for type_ in registry_value_types:
        if type_.winreg_type == winreg_type:
            return type_(value)

    raise TypeError(f'{value} cannot be converted to {winreg_type.name}')


class Binary(RegistryValue, bytearray):
    winreg_type: RegistryValueType = RegistryValueType.BINARY


class Dword(RegistryValue, int):
    winreg_type: RegistryValueType = RegistryValueType.DWORD


class DwordBigEndian(RegistryValue, bytearray):
    winreg_type: RegistryValueType = RegistryValueType.DWORD_BIG_ENDIAN


class Qword(RegistryValue, int):
    winreg_type: RegistryValueType = RegistryValueType.QWORD


class Sz(RegistryValue, str):
    winreg_type: RegistryValueType = RegistryValueType.SZ


class ExpandSz(RegistryValue, str):
    winreg_type: RegistryValueType = RegistryValueType.EXPAND_SZ


class MultiSz(RegistryValue, List[str]):
    winreg_type: RegistryValueType = RegistryValueType.MULTI_SZ


class Link(RegistryValue, bytearray):
    winreg_type: RegistryValueType = RegistryValueType.LINK


class ResourceList(RegistryValue, bytearray):
    winreg_type: RegistryValueType = RegistryValueType.RESOURCE_LIST


class FullResourceDescriptor(RegistryValue, bytearray):
    winreg_type: RegistryValueType = RegistryValueType.FULL_RESOURCE_DESCRIPTOR


class ResourceRequirementsList(RegistryValue, bytearray):
    winreg_type: RegistryValueType = RegistryValueType.RESOURCE_REQUIREMENTS_LIST


def get_registry_value_types() -> List[Type[RegistryValue]]:
    import sys, inspect

    this_module = sys.modules[__name__]

    result = []
    for _, obj in inspect.getmembers(this_module):
        if inspect.isclass(obj) and issubclass(obj, RegistryValue):
            result.append(obj)

    return result


registry_value_types: List[Type[RegistryValue]] = get_registry_value_types()
