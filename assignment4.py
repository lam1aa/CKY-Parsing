import argparse
import nltk

from nltk.tree import Tree
from model.recognizer import recognize
from model.parser import parse, count

GRAMMAR_PATH = './data/atis-grammar-cnf.cfg'

def ensure_nltk_data():
    """Ensure required NLTK data is downloaded."""
    try:
        nltk.data.find('grammars/large_grammars/atis.cfg')
        nltk.data.find('grammars/large_grammars/atis_sentences.txt')
    except LookupError:
        print("Downloading required NLTK data...")
        nltk.download('large_grammars')
        print("Download complete!")


def main():
    # Add data check at start
    ensure_nltk_data()

    parser = argparse.ArgumentParser(
        description='CKY algorithm'
    )

    parser.add_argument(
        '--structural', dest='structural',
        help='Derive sentence with structural ambiguity',
        action='store_true'
    )

    parser.add_argument(
        '--recognizer', dest='recognizer',
        help='Execute CKY for word recognition',
        action='store_true'
    )

    parser.add_argument(
        '--parser', dest='parser',
        help='Execute CKY for parsing',
        action='store_true'
    )

    parser.add_argument(
        '--count', dest='count',
        help='Compute number of parse trees from chart without \
              actually computing the trees (Extra Credit)',
        action='store_true'
    )

    args = parser.parse_args()

    # load the grammar
    grammar = nltk.data.load(GRAMMAR_PATH)
    # load the raw sentences
    s = nltk.data.load("grammars/large_grammars/atis_sentences.txt", "auto")
    # extract the test sentences
    t = nltk.parse.util.extract_test_sentences(s)

    if args.structural:
        # Example 1: "I saw a man with a telescope"
        # Interpretation 1: I used a telescope to see a man
        tree1a = Tree.fromstring('''
            (S 
                (NP (PRP I))
                (VP 
                    (VBD saw)
                    (NP (DT a) (NN man))
                    (PP (IN with) 
                        (NP (DT a) (NN telescope)))))
        ''')
        
        # Interpretation 2: I saw a man who had a telescope
        tree1b = Tree.fromstring('''
            (S 
                (NP (PRP I))
                (VP 
                    (VBD saw)
                    (NP 
                        (NP (DT a) (NN man))
                        (PP (IN with)
                            (NP (DT a) (NN telescope))))))
        ''')

        # Example 2: "She saw the man on the hill"
        # Interpretation 1: She saw the man while she was on the hill
        tree2a = Tree.fromstring('''
            (S 
                (NP (PRP She))
                (VP 
                    (VBD saw)
                    (NP (DT the) (NN man))
                    (PP (IN on)
                        (NP (DT the) (NN hill)))))
        ''')

         # Interpretation 2: She saw the man who was on the hill
        tree2b = Tree.fromstring('''
            (S 
                (NP (PRP She))
                (VP 
                    (VBD saw)
                    (NP 
                        (NP (DT the) (NN man))
                        (PP (IN on)
                            (NP (DT the) (NN hill))))))
        ''')

        print("Example 1: 'I saw a man with a telescope'")

        print("\nTree 1a - PP-attachment 'with a telescope' → VP 'saw'")
        print("Meaning: The telescope is the instrument used for seeing\n")
        tree1a.draw()
       
        print("\nTree 1b - PP-attachment 'with a telescope' → NP 'man'")
        print("Meaning: The telescope belongs to the man\n")
        tree1b.draw()


        print("\nExample 2: 'She saw the man on the hill'\n")

        print("\nTree 2a - PP-attachment 'on the hill' → VP 'saw'")
        print("Meaning: The seeing action occurred while on the hill\n")
        tree2a.draw()
        
       
        print("\nTree 2b - PP-attachment 'on the hill' → NP 'man'")
        print("Meaning: The man's location is on the hill")
        tree2b.draw()


    elif args.recognizer:
        # YOUR CODE HERE
        #     TODO:
        #         1) Provide a list of grammatical and ungrammatical sentences (at least 10 each)
        #         and test your recognizer on these sentences.
        grammatical = []
        ungrammatical = []

        for sents in grammatical:
            val = recognize(grammar, sents)
            if val:
                print("{} is in the language of CFG.".format(sents))
            else:
                print("{} is not in the language of CFG.".format(sents))

        for sents in ungrammatical:
            val = recognize(grammar, sents)
            if val:
                print("{} is in the language of CFG.".format(sents))
            else:
                print("{} is not in the language of CFG.".format(sents))

    elif args.parser:
        # We test the parser by using ATIS test sentences.
        print("ID\t Predicted_Tree\tLabeled_Tree")
        for idx, sents in enumerate(t):
            tree = parse(grammar, sents[0])
            print("{}\t {}\t \t{}".format(idx, len(tree), sents[1]))

        # YOUR CODE HERE
        #     TODO:
        #         1) Choose an ATIS test sentence with a number of parses p
        #         such that 1 < p < 5. Visualize its parses. You can use `draw` 
        #         method to do this.

    elif args.count:
        print("ID\t Predicted_Tree\tLabeled_Tree")
        for idx, sents in enumerate(t):
            num_tree = count(grammar, sents[0])
            print("{}\t {}\t \t{}".format(idx, num_tree, sents[1]))


if __name__ == "__main__":
    main()
