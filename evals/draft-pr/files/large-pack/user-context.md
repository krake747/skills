Users lose their report filters after refreshing the page. This change persists the selected filters
in local storage so the report opens with the same view.

Ticket: https://tickets.example.com/PROJ-123

The migration for old server-side preferences is deliberately out of scope. The main risk is stale
local data after a filter format change.
