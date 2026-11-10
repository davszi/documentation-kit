# The kit's name

Open decision, for deivid. Raised on 2026-11-10. deivid is not happy with any
of the names proposed so far, so the name stays as it is until a better one is
found.

## Why the name is in question

The kit is called "Documentation kit" on its site and in its repository name,
and "Engineering and documentation kit" in its README and `AGENTS.md`. Neither
says what it holds. Measured on 2026-11-10 in words of rule text:

| Area | Words |
|---|---|
| Site building and reader, `rules/site/` | 4,693 |
| Documentation system and records, `rules/*.md` | 3,917 |
| Writing pages, `rules/writing/` | 2,549 |
| Engineering, `rules/engineering/` | 2,246 |
| Experiments, `rules/experiments/` | 1,128 |

About a quarter of the rules are not about documentation: how code is written,
how jobs run, how work is handed off and committed, how experiments are run.
The kit holds the shared rules for how work is done and recorded, and a site
builder. It does not hold a project's own work context; that stays in each
project.

## Names proposed and not accepted

- Shared practices kit
- Working agreements kit
- Agent practices kit
- Project practices kit
- Engineering and documentation kit, the README's current wording
- Handbook or playbook variants

Known problems with some of them: "working agreements" is also the title of
deivid's personal cross-agent file, so one name would mean two things; "agent
practices" leaves out that people follow the rules and read the site; "handbook"
and "playbook" hide that the kit ships tooling.

## What a rename costs

| Layer | Cost |
|---|---|
| Display title on the site and in the README | One setting; no effect on projects. The sidebar header shows it, so it needs captures at wide and narrow widths. |
| Repository name `documentation-kit` | The public site URL changes. GitHub redirects the repository, not the Pages site. |
| Folder `.docs-kit` in every project | Breaking for every project. In ADP alone 28 files name it: router rows, the hosted workflow, tests and 67 links. |

A proposal, not accepted: change at most the display title and the repository
name, and keep the folder `.docs-kit`.

## Next step

deivid names a candidate or asks for more. Until then the site title and the
README keep their two current wordings.
