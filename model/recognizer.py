import nltk
from typing import List


def recognize(grammar: nltk.grammar.CFG, sentence: List[str]) -> bool:
    """
    Recognize whether a sentence in the language of grammar or not.

    Args:
        grammar: Grammar rule that is used to determine grammaticality of sentence.
        sentence: Input sentence that will be tested.

    Returns:
        truth_value: A bool value to determine whether if the sentence
        is in the grammar provided or not.
    """
    if not sentence:
        return False
        
    n = len(sentence)
    table = [[set() for j in range(n+1)] for i in range(n+1)]
    
    # Fill terminal rules
    for i in range(n):
        word = sentence[i]
        for prod in grammar.productions():
            if len(prod.rhs()) == 1 and isinstance(prod.rhs()[0], str):
                if prod.rhs()[0] == word:
                    table[i][i+1].add(prod.lhs())
    
    # Fill parsing table using grammar rules
    for length in range(2, n+1):
        for i in range(n-length+1):
            j = i + length
            for k in range(i+1, j):
                for prod in grammar.productions():
                    if len(prod.rhs()) == 2:
                        B, C = prod.rhs()
                        if B in table[i][k] and C in table[k][j]:
                            table[i][j].add(prod.lhs())
    
    return grammar.start() in table[0][n]