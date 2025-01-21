import nltk

from typing import Set, List, Dict, Tuple
from nltk.tree import Tree, ImmutableTree

def build_trees(bp: Dict, i: int, j: int, symbol: nltk.Nonterminal) -> List[Tree]:
    trees = []
    if (i, j, symbol) not in bp:
        return trees
    
    # Handle terminals
    if isinstance(bp[(i, j, symbol)], str):
        return [Tree(symbol, [bp[(i, j, symbol)]])]
    
    # Handle non-terminals
    for k, (B, C) in bp[(i, j, symbol)]:
        left_trees = build_trees(bp, i, k, B)
        right_trees = build_trees(bp, k, j, C)
        
        for left in left_trees:
            for right in right_trees:
                trees.append(Tree(symbol, [left, right]))
    
    return trees

def parse(grammar: nltk.grammar.CFG, sentence: List[str]) -> Set[nltk.ImmutableTree]:
    """
    Check whether a sentence in the language of grammar or not. If it is, parse it.

    Args:
        grammar: Grammar rule that is used to determine grammaticality of sentence.
        sentence: Input sentence that will be tested.

    Returns:
        tree_set: Set of generated parse trees.
    """
    # YOUR CODE HERE
    #     TODO:
    #         1) Extend your CKY recognizer into a parser by adding backpointers. You
    #         should extract the set of all parse trees from the backpointers in the chart.
    #         2) Note that only 'ImmutableTree` can be used as elements of Python sets.
    ############################# STUDENT SOLUTION ##################################
    if not sentence:
        return set()
    
    n = len(sentence)
    table = [[set() for _ in range(n+1)] for _ in range(n+1)]
    bp = {}
    
    # Terminal rules - simplified backpointer structure
    for i in range(n):
        word = sentence[i]
        for prod in grammar.productions():
            if len(prod.rhs()) == 1 and isinstance(prod.rhs()[0], str):
                if prod.rhs()[0] == word:
                    table[i][i+1].add(prod.lhs())
                    bp[(i, i+1, prod.lhs())] = word  # Store word directly
    
    # Binary rules
    for length in range(2, n+1):
        for i in range(n-length+1):
            j = i + length
            for k in range(i+1, j):
                for prod in grammar.productions():
                    if len(prod.rhs()) == 2:
                        B, C = prod.rhs()
                        if B in table[i][k] and C in table[k][j]:
                            table[i][j].add(prod.lhs())
                            key = (i, j, prod.lhs())
                            if key not in bp:
                                bp[key] = []
                            bp[key].append((k, (B, C)))
    
    # Build trees
    trees = set()
    if grammar.start() in table[0][n]:
        all_trees = build_trees(bp, 0, n, grammar.start())
        for tree in all_trees:
            trees.add(ImmutableTree.convert(tree))
    
    return trees
    #################################################################################

def count(grammar: nltk.grammar.CFG, sentence: List[str]) -> int:
    """
    Compute the number of parse trees without actually computing the parse tree.

    Args:
        grammar: Grammar rule that is used to determine grammaticality of sentence.
        sentence: Input sentence that will be tested.

    Returns:
        tree_count: Number of generated parse trees.
    """
    ############################# STUDENT SOLUTION ##################################
    pass
    #################################################################################