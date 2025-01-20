import nltk

from typing import Set, List


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
    n = len(sentence)
    if n == 0:
        return set()

    # Initialize chart and backpointers    
    chart = [[set() for _ in range(n+1)] for _ in range(n)]
    back = [[{} for _ in range(n+1)] for _ in range(n)]

    # Fill terminal entries
    for i, word in enumerate(sentence):
        productions = [p for p in grammar.productions() if len(p.rhs()) == 1 
                      and p.rhs()[0] == word]
        for prod in productions:
            lhs = prod.lhs()
            chart[i][i+1].add(lhs)
            back[i][i+1][lhs] = word

    # Fill chart with binary rules
    for length in range(2, n+1):
        for start in range(n-length+1):
            end = start + length
            for split in range(start+1, end):
                for B in chart[start][split]:
                    for C in chart[split][end]:
                        productions = [p for p in grammar.productions() if len(p.rhs()) == 2 
                                    and p.rhs()[0] == B and p.rhs()[1] == C]
                        for prod in productions:
                            A = prod.lhs()
                            chart[start][end].add(A)
                            if A not in back[start][end]:
                                back[start][end][A] = []
                            back[start][end][A].append((B, C, split))

    # Build trees from backpointers
    def build_trees(start: int, end: int, symbol) -> Set[ImmutableTree]:
        if end - start == 1:  # Terminal
            return {ImmutableTree(symbol, [back[start][end][symbol]])}
            
        trees = set()
        for B, C, split in back[start][end][symbol]:
            b_trees = build_trees(start, split, B)
            c_trees = build_trees(split, end, C)
            for b in b_trees:
                for c in c_trees:
                    trees.add(ImmutableTree(symbol, [b, c]))
        return trees

    # Extract all parse trees
    trees = set()
    if grammar.start() in chart[0][n]:
        trees = build_trees(0, n, grammar.start())
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
    return len(parse(grammar, sentence))
    #################################################################################