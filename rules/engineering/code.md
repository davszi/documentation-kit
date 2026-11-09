# Code and repository practices

## Logging and program output

Use the project's logging conventions for diagnostics.

When another program consumes stdout or stderr, treat the consumed output as an interface. Keep diagnostics from corrupting that stream and preserve its expected format unless an interface change is agreed.

## Generated files

Identify the source or generator before changing a generated file. Make the change there and regenerate the affected outputs.

Follow the project's toolchain, reproducibility and validation requirements. Keep its rules for which generated outputs are tracked or ignored.

## Refactoring over compatibility

The project prefers clean refactors to keeping old interfaces working.

Before changing a name, path, format, API, URL or configuration key that
something outside the change may still use, ask the project owner. Such users
include published URLs or packages, other repositories that consume this one,
saved data or frozen records that refer to it, and running jobs. Give the
owner what the decision needs:

- what changes and why;
- who or what uses the old form, with evidence;
- what would break, and whether it can be updated in the same change;
- what keeping the old form would cost.

Then wait for the decision.

If the owner decides compatibility is not needed, or nothing outside the change
uses the old form, refactor fully: update every caller and reference in the
same change and remove the old form. Add no aliases, shims, fallbacks, redirects
or deprecation periods.

If the owner decides to keep compatibility, record why it exists and when it
can be removed.
