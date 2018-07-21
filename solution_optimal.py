import numpy as np

def find_range_opt(utxos, x):
  utxos_len = len(utxos)
  if x <= 0 or utxos_len == 0:
    return ()
   # 17,160,850 is circulating supply of BTC at 6 PM PST July 20th.
  min_change = 17160850
  # Let's assume utxos is an array of utxo tuple (val, time). utxo[0] give btc value. utxo[1] gives timestamp.
  result = ()
  start = 0
  end = utxos_len - 1
  if utxos_len == 1 and utxos[0][0] > x:
    return (utxos[0][1], utxos[0][1])
  while start < end:
    utxo_sum = sum(btc for btc,_ in utxos[start:end+1])
    if utxo_sum < x:
      return result
    start_btc = utxos[start][0]
    end_btc = utxos[end][0]
    # This is the btc balance between start and end (excluding start, end). 
    between_btc = utxo_sum - start_btc - end_btc
    if start_btc >= x and end_btc >= x:
      index_min = np.argmin((start_btc, end_btc))
      if index_min == 0 and min_change > start_btc - x:
        min_change = start_btc - x
        result = (utxos[start][1], utxos[start][1])
      elif index_min == 1 and min_change > end_btc - x:
        min_change = end_btc - x
        result = (utxos[end][1], utxos[end][1])
      start+=1
      end-=1
    elif start_btc >= x and between_btc + end_btc >= x:
      index_min = np.argmin((start_btc, between_btc + end_btc))
      if index_min == 0 and min_change > start_btc - x:
        min_change = start_btc - x
        result = (utxos[start][1], utxos[start][1])
      elif index_min == 1 and min_change > between_btc + end_btc - x:
        min_change = between_btc + end_btc - x
        result = (utxos[start+1][1], utxos[end][1])
      start+=1
    elif start_btc + between_btc >= x and end_btc >= x:
      index_min = np.argmin((start_btc + between_btc, end_btc))
      if index_min == 0 and min_change > start_btc + between_btc - x:
        min_change = start_btc + between_btc - x
        result = (utxos[start][1], utxos[end-1][1])
      elif index_min == 1 and min_change > end_btc - x:
        min_change = end_btc - x
        result = (utxos[end][1], utxos[end][1])
      end-=1
    elif start_btc >= x:
      if min_change > start_btc - x:
        min_change = start_btc - x
        result = (utxos[start][1], utxos[start][1])
      return result
    elif end_btc >= x:
      if min_change > end_btc - x:
        min_change = end_btc - x
        result = (utxos[end][1], utxos[end][1])
      return result
    elif start_btc + between_btc >= x and between_btc + end_btc >= x:
      index_min = np.argmin((start_btc, end_btc))
      if index_min == 0:
        if min_change > start_btc + between_btc - x:
          min_change = start_btc + between_btc - x
          result = (utxos[start][1], utxos[end-1][1])
        end-=1
      else:
        if min_change > between_btc + end_btc - x:
          min_change = between_btc + end_btc - x
          result = (utxos[start+1][1], utxos[end][1])
        start+=1
    elif start_btc + between_btc >= x:
      if min_change > start_btc + between_btc - x:
        min_change = start_btc + between_btc - x
        result = (utxos[start][1], utxos[end-1][1])
      end-=1
    elif between_btc + end_btc >= x:
      if min_change > between_btc + end_btc - x:
        min_change = between_btc + end_btc - x
        result = (utxos[start+1][1], utxos[end][1])
      start+=1
    else:
      if utxo_sum - x >= 0 and min_change > utxo_sum - x:
        min_change = utxo_sum - x
        result = (utxos[start][1], utxos[end][1])
      return result
  if utxos[start][0] - x >= 0 and min_change > utxos[start][0] - x:
    min_change = utxos[start][0] - x
    result = (utxos[start][1], utxos[start][1])
  return result
