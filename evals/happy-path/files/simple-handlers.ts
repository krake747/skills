export function checkMargin(account: Account, order: Order): boolean {
  return order.notional <= account.buyingPower;
}

export function isListed(ticker: Ticker): boolean {
  return listedTickers.includes(ticker.symbol);
}

export function checkMaxNotional(order: Order, maxNotional: number): boolean {
  return order.notional <= maxNotional;
}
