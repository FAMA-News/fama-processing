from os import walk, path, system, sep
import distutils.sysconfig as sysconfig
import pkg_resources as pkg
import pycodestyle

PACKAGE_NAME="fama_package"

class TestCode:
    ignored_codes = ["E303", "E501", "W605"]

    def __get_paths(self) -> dict:
        """ Get File Paths """
        paths = {}
        for root, _, files in walk(f"./{PACKAGE_NAME}"):
            # replace idiotic windows path seperator
            root = root.replace("\\", "/")

            def in_filter(filename: str):
                if filename[-3:] == ".py":
                    return True

            if "__pycache__" in root:
                continue
            paths[root] = [
                root+"/"+filename for filename in files if in_filter(filename)]
        return paths

    def __get_standard_lib(self):
        """ Get Modules from Python Standard Library """
        packages = []
        std_lib = sysconfig.get_python_lib(standard_lib=True)
        for top, _, files in walk(std_lib):
            for nm in files:
                if nm != '__init__.py' and nm[-3:] == '.py':
                    packages.append(path.join(top, nm)[
                                    len(std_lib)+1:-3].replace(sep, '.'))

        packages = packages + ["sys", "logging", "urllib"]
        return packages

    def __get_imports(self, filepath: str) -> list:
        """ Get Imports from File """
        imports = []

        with open(filepath) as fp:
            for line in fp.readlines():
                if line.startswith("from"):
                    line = line.replace("from ", "").split(" import")[0]
                elif line.startswith("import"):
                    line = line.replace("import ", "")
                else:
                    continue
                # Remove NL
                line = line.replace("\n", "")
                # Remove submodules
                line = line.split(".")[0]
                if not line.startswith("app") and line:
                    imports.append(line)

        return imports

    def __get_requirements_txt(self, skip_missing: bool = False) -> dict:
        """ Get Packages from requirements.txt """
        main_dir = path.dirname(path.dirname(path.realpath(__file__)))
        packages = {}
        with open(f"{main_dir}{sep}requirements.txt", "r", encoding="utf-16") as fp:
            for line in fp.readlines():
                if "ÿþ" in line:
                    raise ValueError(
                        "ERROR: requirement.txt is not utf-8 encoded \n Use: 'pip freeze | Out-File -Encoding UNICODE requirements.txt'")
                    exit()

                package = line.split("==")[0]
                try:
                    meta_data = list(pkg.get_distribution(
                        package)._get_metadata('top_level.txt'))
                    import_name = meta_data[0] if len(
                        meta_data) > 0 else package
                    packages[package] = import_name
                except pkg.RequirementParseError:
                    if skip_missing:
                        raise ValueError(
                            f"WARN: Package {package} is not installed, will continue")
                    else:
                        assert False, f"Package {package} is not installed. Can't check"

        return packages

    def __get_import_errors(self) -> dict:
        """ Get import errors"""
        standard_lib = self.__get_standard_lib()
        requirements = self.__get_requirements_txt()
        import_files = {}
        for _, files in self.__get_paths().items():
            for filepath in files:
                imports = self.__get_imports(filepath)
                for imp in imports:
                    if imp in (list(requirements.keys()) + list(requirements.values())):
                        continue
                    if imp in standard_lib:
                        continue

                    if import_files.get(imp) != None:
                        import_files[imp].append(filepath)
                    else:
                        import_files[imp] = [filepath]
        return import_files

    def test_imports(self):
        """ Test for missing imports in requirements.txt """
        import_errors = self.__get_import_errors()
        if import_errors == {}:
            for module, files in import_errors.items():
                error = f"WARN: '{module}'  is not in requirements.txt but imported in:"
                for path in files:
                    error += f"\n\t{path}"
                assert module != None, error

        assert len(import_errors.keys(
        )) == 0, f"{len(import_errors.keys())} Import(s) missing frome requirements.txt"

    def test_pep8(self):
        """ Test for PEP8 Code Style Conformance"""
        paths = self.__get_paths()
        style = pycodestyle.StyleGuide(ignore=",".join(self.ignored_codes))
        for _, files in paths.items():
            report = style.check_files(files)
            assert report.total_errors == 0, "Code Style Conformance Failed"
