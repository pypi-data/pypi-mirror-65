from typing import List
from .VersionsFilter import VersionsFilter


class AndroidApp(dict):

    def __init__(self, package_name: str = '', versions_list: List[VersionsFilter] = None):

        super(AndroidApp, self).__init__()

        self['packageName'] = package_name

        if versions_list is not None:
            self['versions'] = versions_list
        else:
            self['versions'] = []

    def add_versions(self, versions: VersionsFilter) -> List[VersionsFilter]:
        for item in versions:
            assert isinstance(item, VersionsFilter)
            self['versions'].append(item)

        return self['versions']

    def add_version(self, min_version: int = None, max_version: int = None) -> VersionsFilter:
        version_filter = VersionsFilter(min_version=min_version, max_version=max_version)
        self['versions'].append(version_filter)

        return version_filter
