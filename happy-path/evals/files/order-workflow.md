# Order workflow

Execute an order for a listed ticker. Reject a closed account, an unlisted ticker, or an order whose
notional exceeds buying power. A valid order is cleared against risk, routed to a broker, and booked
as a fill.

The observable events are `cleared`, `routed`, and `booked`.
