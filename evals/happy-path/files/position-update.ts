type Position = { shares: number; costBasis: number };
type Fill = { quantity: number; notional: number };

export function applyFill(position: Position, fill: Fill): void {
  position.shares += fill.quantity;
  position.costBasis += fill.notional;
}
