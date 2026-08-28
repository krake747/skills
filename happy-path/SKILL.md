---
name: happy-path
description: >-
  Write code type-first and happy-path-first: model the domain in types, orchestrators read like
  English, workflows are named pipelines, data stays immutable, guard clauses leave before the valid
  flow, patterns must pay rent. Use when implementing any change, before choosing abstractions or
  adding layers. Triggers on: implement, refactor, add, build, fix, change. Complements implement
  and scaffold.
metadata:
  author: "Kevin Kraemer <kraemer.kevin747@gmail.com>"
---

# Happy Path First

Design for the normal user flow. If the happy path is 95% of runtime behavior, it should be 95% of
the code a reader sees. Code is read along the main flow; the edge cases bury it.

Start with context. Inspect the existing code, callsites, data flow, and nearby conventions.
Understand the real use case before choosing abstractions. Preserve good existing patterns; do not
impose a generic architecture.

The examples use one domain, order execution on a trading desk, so the bad and good shapes are
comparable. They are written in pseudocode; apply the shapes in whatever language you work in.

## Rules

### Types first

Model the domain in types before writing behavior. Types represent the domain and document it; a
reader should grasp the use case from the types alone. Make illegal states unrepresentable. Parse
external, persisted, and network data once at the boundary into trusted domain values. Do not use
loose `any`, nullable states, or bags of booleans and callbacks when a precise type fits.

```text
// Don't: validate the raw request, then keep using the raw value
validate(orderText)
placeOrder(orderText)          // still a raw string

// Do: parse once at the boundary into a trusted domain value
order = parseOrder(orderText)  // ticker, side, quantity, price
placeOrder(order)
```

```text
// Don't: nullable flags for mutually exclusive states
order = {
  filled: boolean
  filledAt: datetime?
  cancelledAt: datetime?
  rejectedReason: string?
}

// Do: model the legal states directly
orderState = open | filled | cancelled | rejected
```

### Data as values

Treat domain data as values. Do not mutate state in place and return nothing; derive the next state
and return it. Transitions are typed values (`open → filled → closed`), not field edits. Mutation
spreads change invisibly; a derived value keeps the old state intact for every stage that already
read it.

```text
// Don't: mutate the position in place and return nothing
position.shares = position.shares + fill.quantity
position.costBasis = position.costBasis + fill.notional

// Do: derive the next state as a new value, keep the old one intact
updatedPosition = position.withFill(fill)
```

### Declarative over imperative

Declare the shape and rules of the domain over spelling out each step. State what the outcome is,
not the step-by-step how. Let a type or data structure hold the decision instead of imperative
branch soup. The declared shape shows the rules at a glance; step-by-step code hides them, forcing a
reader to re-derive intent from the branches.

### Orchestrators read like English

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

### Workflows are pipelines

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

### Guard clauses first

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

### Patterns must pay rent

Layers, interfaces, functions, and types are costs. Start with the smallest honest implementation: a
direct function or a plain data structure. Add a module, abstraction, or type only when it owns a
real invariant, hides real complexity, has multiple real implementations, or creates a proven
boundary. An abstraction that moves ten obvious lines into five files is negative value; prefer
duplication over the wrong abstraction. Do not wrap a direct operation in pass-through dispatchers
because a diagram, framework, or pattern says so; a handler that forwards to another handler adds
files, call hops, and concepts a reader must learn, and returns no behavior. An `orders/execute.ts`
that declares the flow directly beats three nested dispatchers.

```text
// Don't: a service that only renames a broker call
OrderService.send(order):
  return OrderBroker.send(order)

// Do: the direct operation is the whole story
broker.send: Order → Receipt
```

### Evidence before complexity

Do not defend against theoretical edge cases or imagined races. "Could", "might", and "what if" are
not justification. When a real runtime, log, or test reproduction proves a case, fix the smallest
real failure at the boundary that owns it.

### Deep modules, not helper shrapnel

Extract one deep operation that hides real complexity, not three shallow helpers that force readers
to reconstruct a single step.

```text
// Don't: shallow helpers that force readers to reconstruct the check
checkMargin()
checkPositionLimit()
checkMaxNotional()

// Do: one deep operation hides the real complexity
risk.check: Order → ClearedOrder
```

### Tests at stable boundaries

Test the observable use case, not one-line helpers or mocked internals. A test on the use case
survives refactors; a test pinned to helpers and mocks breaks when the code improves.

```text
// Don't: test the implementation sentence by sentence
expect marginCheck(10000, 25000) == true
expect symbolIsListed("TSLA") == true

// Do: test the stable use-case boundary and observable order
executeTrade(order)
expect events == [cleared, routed, booked]
```

## Completion standard

Finish the complete change, run focused verification, delete temporary artifacts, and do one final
simplification pass. The result should feel boring, obvious, typed, cohesive, and native to the
codebase.

See [scaffold](../scaffold/SKILL.md) for matching existing patterns.
