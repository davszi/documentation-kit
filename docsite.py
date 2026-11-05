#!/usr/bin/env python3
"""Use the pinned documentation kit without copying its tools into a project."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

KIT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    init = commands.add_parser('init', help='add starter sources without overwriting existing files')
    init.add_argument('project', type=Path)
    for name in ('build', 'lint'):
        command = commands.add_parser(name)
        command.add_argument('--project', type=Path, default=Path.cwd())
        if name == 'build':
            command.add_argument('--check', action='store_true')
            command.add_argument('--page')
        else:
            command.add_argument('--strict', action='store_true')
            command.add_argument('--registry', action='store_true')
    slides = commands.add_parser('slides', help='build the site, then extract chapter slide faces into a deck')
    slides.add_argument('--project', type=Path, default=Path.cwd())
    slides.add_argument('--select', action='append', required=True, help='slug or slug#chapter,chapter (repeatable)')
    slides.add_argument('--out', required=True, help='deck name; written to .build/slides/<name>.html')
    slides.add_argument('--title', default='Slides')
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        parser.error('Python 3.12 or newer is required; validation uses Python 3.12.')
    project = args.project.resolve()
    if args.command == 'init':
        starter = KIT / 'examples/starter'
        sources = [p for p in starter.rglob('*') if p.is_file() and '.build' not in p.relative_to(starter).parts]
        if any(not (project / p.relative_to(starter)).resolve().is_relative_to(project) for p in sources):
            parser.error('No files written; a starter destination escapes the project through a symlink.')
        conflicts = [str(p.relative_to(starter)) for p in sources
                     if (project / p.relative_to(starter)).exists() or (project / p.relative_to(starter)).is_symlink()]
        if conflicts:
            parser.error('No files written; existing starter destinations: ' + ', '.join(conflicts))
        for source in sources:
            destination = project / source.relative_to(starter)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        print(f'Starter added to {project}. Configure docs/site/site.toml, then track the sources in Git before building.')
        return 0
    if not (project / 'docs/site/site.toml').is_file():
        parser.error(f'No docs/site/site.toml under {project}; use init for a new project.')
    env = dict(os.environ, DOCSITE_PROJECT_ROOT=str(project))
    if args.command == 'slides':
        built = subprocess.run([sys.executable, str(KIT / 'tooling' / 'build.py')], env=env, cwd=project).returncode
        if built:
            return built
        deck = [sys.executable, str(KIT / 'tooling' / 'slides.py'), '--out', args.out, '--title', args.title]
        for value in args.select:
            deck.extend(('--select', value))
        return subprocess.run(deck, env=env, cwd=project).returncode
    options = [option for option in ('--check', '--strict', '--registry')
               if getattr(args, option[2:], False)]
    if getattr(args, 'page', None):
        options.extend(('--page', args.page))
    return subprocess.run([sys.executable, str(KIT / 'tooling' / (args.command + '.py')), *options],
                          env=env, cwd=project).returncode


if __name__ == '__main__':
    raise SystemExit(main())
