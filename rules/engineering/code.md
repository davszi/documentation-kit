# Code and repository practices

## Logging and program output

Use the project's logging conventions for diagnostics.

When another program consumes stdout or stderr, treat the consumed output as an interface. Keep diagnostics from corrupting that stream and preserve its expected format unless an interface change is agreed.

## Generated files

Identify the source or generator before changing a generated file. Make the change there and regenerate the affected outputs.

Follow the project's toolchain, reproducibility and validation requirements. Keep its rules for which generated outputs are tracked or ignored.
