import os

from setuptools import setup


if os.environ.get("READTHEDOCS") == "True":
    with open("setup.cfg") as setup_file:
        setup_lines = setup_file.readlines()

    with open("setup.cfg", "w") as setup_file:
        for line in setup_lines:
            if line.startswith("install_requires"):
                break
            setup_file.writelines(line)

setup(
    use_scm_version={
        "version_scheme": "python-simplified-semver",
        "local_scheme": "no-local-version",
    }
)

if os.environ.get("READTHEDOCS") == "True":
    with open("setup.cfg", "w") as setup_file:
        setup_file.writelines(setup_lines)
