"""Consumer paths are independent of the shared kit's installation path."""
import os
from pathlib import Path
import tomllib
import topic_structure as _topics

REPO = Path(os.environ.get("DOCSITE_PROJECT_ROOT", Path.cwd())).resolve()
DOCS = REPO / "docs"
TOPICS = DOCS / "topics"
SITE = DOCS / "site"
KIT_SITE = Path(__file__).resolve().parents[1] / "theme"
OUTPUT_ROOT = REPO / ".build" / "docs"
HTML = OUTPUT_ROOT / "html"
_TOPIC_GROUPS = _topics.topic_group_folders(REPO)
_ALIASES = ((Path("docs/html"), Path(".build/docs/html")),)


def _topic_groups(root):
    # The running project's configuration is already loaded; other roots are read on demand.
    return _TOPIC_GROUPS if Path(root) == REPO else _topics.topic_group_folders(root)


def topic_pages(root=REPO):
    return _topics.topic_pages(root, _topic_groups(root))


def is_topic_page(path, root=REPO):
    return _topics.is_topic_page(path, root, _topic_groups(root))


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
    if (not source.resolve().is_relative_to(root)
            or any(parent.is_symlink() for parent in (source, *source.parents)
                   if parent.is_relative_to(root))):
        raise ValueError("local_artifacts_manifest must stay inside the project without symlinks")
    if not source.exists() and not configured:
        return None
    if not source.is_file():
        raise ValueError("local_artifacts_manifest must name an existing file: " + value)
    return source


def resolve_site_path(path, root=REPO):
    """The current file for a link target: the kit's own resolution only.

    The logical `docs/html/` origin maps to the build output; every other
    path is itself. The project adapter `path_resolver`, the single-file map
    `legacy_files` and the exact-byte collections of `evidence_manifests` were
    removed in 5.0.0; the build rejects each setting.
    """
    root = Path(root).resolve()
    path = Path(path)
    absolute = Path(os.path.abspath(path if path.is_absolute() else root / path))
    try:
        relative = absolute.relative_to(root)
    except ValueError:
        return absolute
    for old, current in _ALIASES:
        if relative.is_relative_to(old):
            return root / current / relative.relative_to(old)
    return root / relative
