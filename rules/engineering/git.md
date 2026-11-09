# Git changes and shared checkouts

Read this guide before staging, committing or rewriting Git history. Follow the
repository's validation requirements and publication permissions.

## Deliverables and validation

- Commit one logical deliverable, such as a fix, feature, experiment or coherent
  refactor stage. Fold its intermediate file changes and tweaks together.
- Keep separate commits for independently verified stages when their separate
  verification is meaningful.
- Follow the [documentation rules](../documentation.md#rules-for-changes-and-chronology)
  for the code, tests, documentation and chronology belonging to a deliverable.
- Pass the applicable checks before landing implementation. Record actual
  results, skips and limitations. Investigation or evidence deliverables may
  retain failed or negative outcomes when accurately documented.
- Creating a commit does not establish that its tests passed or that its
  acceptance requirements were met.

## Commit messages

Use a short imperative subject and an explanatory body, separated by a blank
line. Explain what changed and why. Include validation results or limitations
when they help assess the change. Do not use Conventional Commits prefixes.

## Preparing a commit

- Inspect the current branch, working changes and staging area before staging.
  Identify which changes belong to the deliverable.
- Stage explicit paths or selected changes. Stage everything only when every
  affected change belongs to the intended commit.
- Review the complete proposed commit, including deletions and changes staged
  before you started. Confirm that the intended file versions match the source
  state covered by the recorded checks.
- Preserve unrelated working and staged changes.

## Sharing a checkout

- When contributors share a staging area, give staging and committing one owner
  for the duration of the operation.
- Protect the proposed commit from concurrent staging between final review and
  commit creation. Git's locks around individual commands do not protect the
  interval between those commands.
- If that protection cannot be established, prepare and verify the commit in an
  isolated staging area or worktree. Coordinate updates to the shared branch.
  When landing it, reconcile the shared staging area with the new commit while
  preserving others' staged intent and working changes. Resolve overlapping
  paths with their owner before proceeding, and verify the resulting status.
- Coordinate overlapping file edits separately. A staging-area lock does not
  protect working files from concurrent edits.

## The shared kit submodule

Never commit inside the `.docs-kit` submodule of a consuming project. A commit
made there exists only on that disk. The project's pin then names a commit
nobody else can fetch, and every fresh clone and CI checkout fails.

To change the kit:

1. Make the change in the kit's own repository, with its checks and review.
2. Push it there.
3. Move the consuming project's pin to the pushed commit as its own
   deliverable, following the kit's migration guide.

`docsite.py lint` fails when the pinned kit commit is on none of the kit's
remote branches. A tag does not count, because a local tag looks the same as a
pushed one. The check is skipped for a shallow checkout, whose fetch already
proves the remote has the commit, and for a kit copy without Git metadata.

## History and recovery

- Consolidate temporary checkpoints only in isolated, unshared history.
  Preserve history used by another contributor or active job.
- If unrelated changes enter a commit, record the affected commit and notify
  their owner through the agreed channel. Agree on recovery before rewriting
  history another contributor may be using.
