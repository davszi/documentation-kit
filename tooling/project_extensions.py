"""Explicit, tracked project adapters for historical paths and evidence policy."""
import importlib.util
from pathlib import Path
import subprocess
import tomllib


def load_extension(root, key):
    root = Path(root).resolve()
    config = root / 'docs/site/site.toml'
    value = tomllib.loads(config.read_text()).get(key) if config.is_file() else None
    if value is None:
        return None
    if not isinstance(value, str) or not value or Path(value).is_absolute() or '..' in Path(value).parts:
        raise ValueError(f'{key} must name a project-relative Python module')
    source = root / value
    if source.suffix != '.py' or not source.is_file() or not source.resolve().is_relative_to(root):
        raise ValueError(f'{key} must name a contained Python file: {value}')
    if any(parent.is_symlink() for parent in (source, *source.parents) if parent.is_relative_to(root)):
        raise ValueError(f'{key} cannot use symlinks: {value}')
    tracked = subprocess.run(['git', 'ls-files', '--error-unmatch', '--', value], cwd=root, capture_output=True)
    if tracked.returncode:
        raise ValueError(f'{key} must be tracked by the project: {value}')
    spec = importlib.util.spec_from_file_location('docsite_project_' + key, source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
