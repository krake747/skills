# Types and Boundaries

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

## Data as Values

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
