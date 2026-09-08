# ADR-014: Report filter storage

## Decision

Store the saved report filters in the `filter_snapshot` column on the `reports` table using the
`jsonb` type with a GIN index, backfilled by `migrations/20260201_add_report_filters.ts`.

## Rules

Do not copy.

See docs/storage.md

Doc: https://example.com/docs/storage
