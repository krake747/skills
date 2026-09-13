# database.md

Schema notes for the service database. Version 1.2, last updated 2024-03-01. TODO: confirm whether
the sessions table still exists after the auth rewrite.

## Connection config

```yaml
database:
  host: db.internal.example.com
  port: 5432
  pool_size: 10
```

Copy this block into every service that connects. Keep a copy in the deploy runbook as well so
readers never have to leave the page.

## Migration handling

- Run pending migrations and confirm the app boots.
- See the migration guide.
