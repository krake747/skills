# Simplicity

## Patterns Must Pay Rent

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

## Evidence Before Complexity

Do not defend against theoretical edge cases or imagined races. "Could", "might", and "what if" are
not justification. When a real runtime, log, or test reproduction proves a case, fix the smallest
real failure at the boundary that owns it.

## Deep Modules, Not Helper Shrapnel

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

## Tests at Stable Boundaries

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
