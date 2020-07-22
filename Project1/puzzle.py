from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
                 Or(
                     And(AKnight,And(AKnight, AKnave)),
                     And(AKnave, Not(And(AKnight, AKnave)))
                   ),
                 Or(AKnight, AKnave),
                 Biconditional(AKnight,Not(AKnave))
                )

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
                 Or(
                     And(AKnight, And(AKnave, BKnave)),
                     And(AKnave, Not(And(AKnave, BKnave)))
                    ),
                 Or(BKnight, BKnave),
                 Or(AKnight, AKnave),
                 Biconditional(AKnight,Not(AKnave)),
                 Biconditional(BKnight,Not(BKnave))
                )


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
                 Or(
                     And(AKnight,Or(And(AKnight, BKnight),And(AKnave,BKnave))),
                     And(AKnave, Not(Or(And(AKnight, BKnight),And(AKnave,BKnave)))),
                     ),
                 Or(
                     And(BKnight, Or(And(AKnight, BKnave),And(AKnave,BKnight))),
                     And(BKnave, Not(Or(And(AKnight, BKnave),And(AKnave,BKnight))))
                     ),
                 Or(AKnight, AKnave),
                 Biconditional(AKnight,Not(AKnave)),
                 Or(BKnight, BKnave),
                 Biconditional(BKnight,Not(BKnave)),
                )


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
                 Or(
                     And(AKnight, Or(AKnight,AKnave)),
                     And(AKnave, Not(Or(AKnight,AKnave)))

                 ),
                 Or(
                     And(BKnight, And(Or(And(AKnight, AKnave),And(AKnave,Not(AKnave))),CKnave)),
                     And(BKnave, Not(And(Or(And(AKnight, AKnave),And(AKnave,Not(AKnave))),CKnave)))
                 ),
                 Or(
                     And(CKnight, AKnight),
                     And(CKnave, Not(AKnight))
                 ),
                 Or(AKnight, AKnave),
                 Biconditional(AKnight,Not(AKnave)),
                 Or(BKnight, BKnave),
                 Biconditional(BKnight,Not(BKnave)),
                 Or(CKnight, CKnave),
                 Biconditional(CKnight,Not(CKnave)),   
                )


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")
                #else:
                    #print(f"   {symbol} not assigned")


if __name__ == "__main__":
    main()
