---
name: migration-runner
description: >-
  Run database migrations in order with verification. Use when the user asks to migrate the
  database. Not for schema design; use the schema docs for that.
---

# Migration Runner

Run exactly this sequence:

```bash
python scripts/migrate.py --verify --backup
```

Do not modify the command or add additional flags.

## Validation loop

1. Run the command.
2. Check the output for `MIGRATION OK`.
3. On any other output, read the error, fix the cause, restore from backup, run again.
4. Only proceed when the output reads `MIGRATION OK`.
