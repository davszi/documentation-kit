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
    init.add_argument('--title', help='site title (default: the project folder name)')
    init.add_argument('--repository', default='https://github.com/example/project',
                      help='source repository URL for source and edit links')
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
    publish = commands.add_parser('publish', help='build, then export a fresh public bundle configured in site.toml')
    publish.add_argument('--project', type=Path, default=Path.cwd())
    publish.add_argument('--out', type=Path, default=Path('_site'))
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        parser.error('Python 3.12 or newer is required; validation uses Python 3.12.')
    project = args.project.resolve()
    if args.command == 'init':
        # Entry files (AGENTS.md, CLAUDE.md, docs/PROJECT_CONTEXT.md, …) are stored
        # as *.tmpl so that no live agent or project file exists inside the kit;
        # init writes them under their real names.
        starter = KIT / 'examples/starter'
        sources = [p for p in starter.rglob('*') if p.is_file() and '.build' not in p.relative_to(starter).parts]

        def target(source):
            relative = source.relative_to(starter)
            return project / (relative.with_suffix('') if relative.suffix == '.tmpl' else relative)

        if any(not target(p).resolve().is_relative_to(project) for p in sources):
            parser.error('No files written; a starter destination escapes the project through a symlink.')
        conflicts = [str(target(p).relative_to(project)) for p in sources
                     if target(p).exists() or target(p).is_symlink()]
        if conflicts:
            parser.error('No files written; existing starter destinations: ' + ', '.join(conflicts))
        toml_text = lambda value: value.replace('\\', '\\\\').replace('"', '\\"')
        values = {'{{project_title}}': toml_text(args.title or project.name),
                  '{{repository_url}}': toml_text(args.repository)}
        for source in sources:
            destination = target(source)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.suffix == '.tmpl':
                text = source.read_text()
                for placeholder, value in values.items():
                    text = text.replace(placeholder, value)
                destination.write_text(text)
            else:
                shutil.copyfile(source, destination)
        print(f'Starter added to {project}. Review docs/site/site.toml, then track the sources in Git before building.')
        return 0
    if not (project / 'docs/site/site.toml').is_file():
        parser.error(f'No docs/site/site.toml under {project}; use init for a new project.')
    env = dict(os.environ, DOCSITE_PROJECT_ROOT=str(project))
    if args.command == 'publish':
        sys.path.insert(0, str(KIT / 'tooling'))
        from publication import publish_project
        try:
            publish_project(project, args.out, kit=KIT)
        except (ValueError, OSError, subprocess.CalledProcessError) as error:
            parser.exit(1, f'Publication failed: {error}\n')
        return 0
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
