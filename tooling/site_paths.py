"""Consumer paths are independent of the shared kit's installation path."""
import os
from pathlib import Path
import tomllib
from project_extensions import load_extension

REPO = Path(os.environ.get("DOCSITE_PROJECT_ROOT", Path.cwd())).resolve()
DOCS = REPO / "docs"
TOPICS = DOCS / "topics"
SITE = DOCS / "site"
KIT_SITE = Path(__file__).resolve().parents[1] / "theme"
OUTPUT_ROOT = REPO / ".build" / "docs"
HTML = OUTPUT_ROOT / "html"
_config_path = SITE / "site.toml"
_config = tomllib.loads(_config_path.read_text()) if _config_path.is_file() else {}
_project_paths = load_extension(REPO, 'path_resolver')
if _project_paths is not None and not callable(getattr(_project_paths, 'resolve_legacy_path', None)):
    raise ValueError('path_resolver must export resolve_legacy_path')
_ALIASES = ((Path("docs/html"), Path(".build/docs/html")),)
# Optional historical identities belong to the consuming project.
LEGACY_FILES = {Path(old): Path(new) for old, new in _config.get("legacy_files", {}).items()}
for old, new in LEGACY_FILES.items():
    if old.is_absolute() or new.is_absolute() or ".." in old.parts or ".." in new.parts:
        raise ValueError("legacy_files paths must stay inside the project")


def topic_pages(root=REPO):
    return sorted((Path(root) / "docs/topics").glob("*/index.md"))


def is_topic_page(path, root=REPO):
    try:
        relative = Path(path).relative_to(Path(root) / "docs/topics")
    except ValueError:
        return False
    return len(relative.parts) == 2 and relative.name == "index.md"


def local_artifacts_manifest(root=REPO, *, site=None):
    """Locate an optional local-artifact inventory without hiding config typos."""
    root = Path(root).resolve()
    if site is None:
        config = root / "docs/site/site.toml"
        site = tomllib.loads(config.read_text()) if config.is_file() else {}
    configured = "local_artifacts_manifest" in site
    value = site.get("local_artifacts_manifest", "docs/evidence/local-artifacts.json")
    if (not isinstance(value, str) or not value or "\\" in value
            or Path(value).is_absolute() or ".." in Path(value).parts
            or Path(value).as_posix() != value):
        raise ValueError("local_artifacts_manifest must name a contained relative file")
    source = root / value
    if not configured and not source.exists() and not source.is_symlink():
        # Consumers predating the evidence directory keep their exact default.
        legacy = root / "docs/project/local-artifacts.json"
        if legacy.exists() or legacy.is_symlink():
            source = legacy
    if (not source.resolve().is_relative_to(root)
            or any(parent.is_symlink() for parent in (source, *source.parents)
                   if parent.is_relative_to(root))):
        raise ValueError("local_artifacts_manifest must stay inside the project without symlinks")
    if not source.exists() and not configured:
        return None
    if not source.is_file():
        raise ValueError("local_artifacts_manifest must name an existing file: " + value)
    return source


def resolve_legacy_path(path, root=REPO, *, recorded_roots=()):
    if _project_paths is not None:
        return _project_paths.resolve_legacy_path(path, root=root, recorded_roots=recorded_roots)
    root = Path(root).resolve()
    path = Path(path)
    absolute = Path(os.path.abspath(path if path.is_absolute() else root / path))
    for recorded in recorded_roots:
        if not isinstance(recorded, (str, Path)):
            raise ValueError("Recorded source_root must be an absolute project path")
        origin = Path(recorded)
        if not origin.is_absolute() or origin.parent == origin or origin.as_posix() != str(recorded) or ".." in origin.parts:
            raise ValueError("Invalid recorded source_root")
        if not absolute.is_relative_to(root) and absolute.is_relative_to(origin):
            absolute = root / absolute.relative_to(origin)
    try:
        relative = absolute.relative_to(root)
    except ValueError:
        return absolute
    for old, current in _ALIASES:
        if relative.is_relative_to(old):
            relative = current / relative.relative_to(old)
            break
    return root / LEGACY_FILES.get(relative, relative)
