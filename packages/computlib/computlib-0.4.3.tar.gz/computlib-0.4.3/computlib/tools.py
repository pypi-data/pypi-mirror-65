import toml
import pathlib


def getVersion(pathfile="pyproject.toml"):
    """
        Get version from pyproject.toml file
        Return string version
    """
    pyproject = pathlib.Path(pathfile)

    # Check if exist
    if pyproject.exists() is False:
        raise ValueError("Pyproject.toml not found at root directory !")

    # Load file
    pyproject_data = toml.load(pyproject)
    return pyproject_data["tool"]["poetry"]["version"]
