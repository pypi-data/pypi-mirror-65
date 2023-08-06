def sort_versions(versions):
    version_numbers = list()
    for version in versions:
        version_numbers.append(VersionNumber(version))

    version_numbers.sort(reverse=True)
    return list(map(lambda ver: ver.get_version(), version_numbers))


class VersionNumber:
    def __init__(self, version):
        self.version = version
        self.split_version = version.split(".")

    def get_version(self):
        return self.version

    def __lt__(self, other):
        for i in range(len(self.split_version)):
            if i >= len(other.split_version):
                return False
            if self.split_version[i] != other.split_version[i]:
                return self.split_version[i] < other.split_version[i]

        if len(other.split_version) > len(self.split_version):
            return True

        return False
