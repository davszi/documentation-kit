"""Detect a consuming project's kit pin that nobody else can fetch.

A commit made inside a project's `.docs-kit` submodule exists only on that
disk. Pinning it breaks every fresh clone and CI checkout of the project.
See rules/engineering/git.md#the-shared-kit-submodule.
"""
from __future__ import annotations

import subprocess
from pathlib import Path


def _git(kit: Path, *args: str) -> str | None:
    result = subprocess.run(['git', '-C', str(kit), *args], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def unpublished_pin(kit: Path, project: Path) -> str | None:
    """Return an error message when the pinned kit commit is on no remote branch.

    The check applies only to a kit checked out inside the project. It is
    skipped for the kit's own repository, a kit used from outside the project,
    a copy without Git metadata and a shallow checkout (a shallow fetch of the
    pinned commit already proves the remote has it).
    """
    kit, project = Path(kit).resolve(), Path(project).resolve()
    if kit == project or not kit.is_relative_to(project):
        return None
    if _git(kit, 'rev-parse', '--show-toplevel') != str(kit):
        return None
    if _git(kit, 'rev-parse', '--is-shallow-repository') != 'false':
        return None
    head = _git(kit, 'rev-parse', 'HEAD')
    if head is None:
        return None
    if _git(kit, 'for-each-ref', '--contains', head, '--format=%(refname)', 'refs/remotes'):
        return None
    return (f'kit pin {head[:12]} in {kit.relative_to(project).as_posix()} is on no remote branch of the kit. '
            'Commit kit changes in the kit repository, push them, then move the pin '
            '(rules/engineering/git.md#the-shared-kit-submodule).')
