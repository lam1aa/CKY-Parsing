### 4.2 Error in Word Recognition

Output:

```
# Valid
['show', 'flights', 'from', 'boston'] is in the language of CFG.
['list', 'flights', 'to', 'denver'] is in the language of CFG.
['show', 'flights', 'from', 'dallas', 'to', 'boston'] is in the language of CFG.
['list', 'american', 'airlines', 'flights'] is in the language of CFG.
['show', 'northwest', 'flights'] is in the language of CFG.
['list', 'direct', 'flights'] is in the language of CFG.
['show', 'economy', 'flights'] is in the language of CFG.
['list', 'morning', 'flights'] is in the language of CFG.
['show', 'round', 'trip', 'flights'] is in the language of CFG.
['list', 'first', 'class', 'flights'] is in the language of CFG.

# Invalid
['flights', 'show', 'from', 'boston'] is not in the language of CFG.
['list', 'flights', 'dallas', 'to'] is not in the language of CFG.
['show', 'the', 'very', 'cheap', 'flights'] is not in the language of CFG.
['reserve', 'tickets', 'now'] is not in the language of CFG.
['from', 'to', 'dallas'] is not in the language of CFG.
['want', 'train', 'schedule'] is not in the language of CFG.
['tickets', 'buy', 'please'] is not in the language of CFG.

# Invalid Cases Accepted
['show', 'bus', 'tickets'] is in the language of CFG.
['show', 'hotel', 'prices'] is in the language of CFG.
['flights', 'flights', 'flights'] is in the language of CFG.
```

The recognizer.py implements the CKY algorithm to determine if input sentences belong to the ATIS grammar. The code creates a dynamic programming table and fills it bottom-up: first with terminal rules (matching individual words to grammar symbols), then with binary rules (combining adjacent spans). 

While it correctly identifies valid ATIS flight queries (like "show flights from boston"), it has limitations in recognizing domain constraints - accepting out-of-domain terms (like "bus tickets") and repetitive patterns ("flights flights flights"). This shows the implementation handles syntactic structure but doesn't fully capture the semantic restrictions inherent in the ATIS domain.

I tried to fix it by adding domain validation and checking for valid command verbs at the start of sentences. Adding hardcoded validation for flight-related terms did work but it goes against the principle of letting the grammar define the language. The fix attempts were unsuccessful because they either made the recognizer too restrictive or ignored the grammar's inherent constraints.

