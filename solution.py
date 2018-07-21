def find_range(utxos, x):
  utxos_len = len(utxos)
  if x <= 0 or utxos_len == 0:
    return ()
   # 17,160,850 is circulating supply of BTC at 6 PM PST July 20th.
  min_change = 17160850
  # Let's assume utxos is an array of utxo tuple (val, time). utxo[0] give btc value. utxo[1] gives timestamp.
  result = ()
  for start in range(utxos_len):
    end = utxos_len - 1
    while start <= end:
      utxo_sum = sum(btc for btc,_ in utxos[start:end+1])
      if utxo_sum >= x and (utxo_sum - x) < min_change:
        min_change = utxo_sum - x
        result = (utxos[start][1], utxos[end][1])
      if min_change == 0:
        return result
      end = end - 1
  return result
