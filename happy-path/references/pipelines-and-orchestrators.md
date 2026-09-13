# Pipelines and Orchestrators

## Declarative Over Imperative

Declare the shape and rules of the domain over spelling out each step. State what the outcome is,
not the step-by-step how. Let a type or data structure hold the decision instead of imperative
branch soup. The declared shape shows the rules at a glance; step-by-step code hides them, forcing a
reader to re-derive intent from the branches.

## Orchestrators Read Like English

The top-level reads as the use case: a sentence of well-named, typed stages. Keep parsing, process
plumbing, protocol details, and long validation branches out of it. The use case scans from the top;
plumbing makes a reader re-trace the flow to find it.

```text
// Don't: let the orchestrator own parsing, risk, routing, and booking
executeTrade(request):
  validate(request)
  order = parseOrder(request)
  if order.notional > account.buyingPower: reject(order)
  exchange = bestRouteFor(order)
  receipt = sendToExchange(exchange, order)
  positions = bookFill(positions, receipt)
  emit(receipt)

// Do: the orchestrator reads as the use case; mechanics stay hidden
Execute a trade: clear it against risk, route it to the broker, then book the fill.
```

## Workflows Are Pipelines

Model each use case as a function from a named input to a named output:
`ExecuteTrade: Order → Fill`. The stages in between are typed steps. A workflow without a named
input and output is missing its contract.

```text
// Don't: describe the workflow as a loose sequence of actions
execute trade:
  get the order
  check margin
  route to the broker
  apply the fill

// Do: declare the workflow as a named pipeline with typed stages
ExecuteTrade: Order → Fill
  risk    : Order → ClearedOrder
  route   : ClearedOrder → PlacedOrder
  book    : PlacedOrder → Fill
```

## Guard Clauses First

Invalid inputs and broken invariants leave immediately. Keep the valid path flat and linear; do not
nest it inside defensive branches. Nesting forces the reader through the failure cases to reach the
flow that matters. Fail fast on broken invariants and failed commands; do not bury the happy path
under code for events that should not happen.

```text
// Don't: the valid path buried in nested conditionals
if account.isOpen:
  if order.ticker.isListed:
    if order.notional <= account.buyingPower:
      route(order)

// Do: invalid conditions leave first; the valid path stays flat
unless account.isOpen: reject(order)
unless order.ticker.isListed: reject(order)
unless order.notional <= account.buyingPower: reject(order)
route(order)
```
