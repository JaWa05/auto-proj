"""
runNFA.py  --  NFA Simulator for CS3383 Project 1
--------------------------------------------------
Usage:
    python runNFA.py

The program will prompt for a filename (without .txt extension).
- If the file has test strings, it prints (accepted/rejected, ...) and quits.
- If the file has an empty test tuple (), it enters interactive mode.
"""

# ─────────────────────────────────────────────
#  PARSER
# ─────────────────────────────────────────────

def parse_file(filename):
    """
    Opens <filename>.txt and parses the outer tuple:
        ( <NFA-tuple>, <test-strings-tuple> )

    Returns:
        nfa   -- dict with keys: sigma, states, start, accept, transitions
        tests -- list of test strings (empty list = interactive mode)
    """
    path = filename + ".txt" #The path includes the ".txt" files for easier use of program.
    with open(path, "r") as f:
        content = f.read() #Reads the entire file into one string for character parsing.


    pos = [0] 
    #the position index is in the form of a list so nested functions can make modifications.

    def skip_ws(): #This function allows the position index to advance past any white spaces including tabs and new lines.
        while pos[0] < len(content) and content[pos[0]].isspace():
            pos[0] += 1

    def peek(): #This function looks at a character without consuming the character. 
        skip_ws()
        if pos[0] >= len(content):
            return None
        return content[pos[0]]

    def consume(): #This function skips the white spaces while also reading and moving on to the next character.
        #Is called when we know the character to be expected next and we need to move forward.
        skip_ws()
        ch = content[pos[0]]
        pos[0] += 1
        return ch

    def expect(ch): #This function consumes the character and prevents wrong results from being produced.
        #any grammatical issues with the text files will be checked here.
        got = consume()
        if got != ch:
            raise ValueError(f"Parse error: expected '{ch}' but got '{got}' at pos {pos[0]}")

    def read_token():
        """Read a maximal alphanumeric token (state name or symbol)."""
        skip_ws()
        start = pos[0]
        while pos[0] < len(content) and content[pos[0]].isalnum():
            pos[0] += 1
        token = content[start:pos[0]]
        if not token:
            raise ValueError(f"Parse error: expected token at pos {pos[0]}")
        return token

    def parse_tuple_of_tokens():
        """Parse (tok1, tok2, ...) and return a list of token strings."""
        expect('(')
        items = []
        while peek() != ')':
            items.append(read_token())
            if peek() == ',':
                consume()
        expect(')')
        return items

    def parse_start_state():
        """Parse a single identifier (the start state)."""
        return read_token()

    def parse_transitions():
        """
        Parse ((s1,c1,t1),(s2,c2,t2),...) and return a list of (from, sym, to) tuples.
        """
        expect('(')
        triples = []
        while peek() != ')':
            expect('(')
            frm = read_token()
            expect(',')
            sym = read_token()
            expect(',')
            to  = read_token()
            expect(')')
            triples.append((frm, sym, to))
            if peek() == ',':
                consume()
        expect(')')
        return triples

    def parse_nfa():
        """Parse the full 5-tuple NFA: (sigma, states, start, accept, transitions)"""
        expect('(')

        sigma       = parse_tuple_of_tokens();  expect(',')
        states      = parse_tuple_of_tokens();  expect(',')
        start       = parse_start_state();      expect(',')
        accept      = parse_tuple_of_tokens();  expect(',')
        transitions = parse_transitions()

        expect(')')

        # Basic validation
        if start not in states:
            raise ValueError(f"Start state '{start}' not in states list")
        for a in accept:
            if a not in states:
                raise ValueError(f"Accept state '{a}' not in states list")

        return {
            "sigma":       set(sigma),
            "states":      set(states),
            "start":       start,
            "accept":      set(accept),
            "transitions": transitions  # list of (from, sym, to)
        }

    def parse_test_strings():
        """Parse () or (1101, 0001, 1110) and return a list of strings."""
        return parse_tuple_of_tokens()

    # ── Top-level: ( <NFA> , <tests> ) ──
    expect('(')
    nfa     = parse_nfa();           expect(',')

    tests   = parse_test_strings()
    expect(')')

    return nfa, tests


# ─────────────────────────────────────────────
#  NFA SIMULATOR  (stack-based, from algorithm ideas PDF)
# ─────────────────────────────────────────────

def simulate(nfa, input_string):
    """
    Decides whether input_string is accepted by nfa.

    Algorithm (from proj-1-algorithmIdeas.pdf):
      - Push the initial configuration (start_state, full_input) onto a stack.
      - Pop a configuration (state, remaining) and:
          * If remaining is empty AND state is an accept state → ACCEPT
          * If remaining is empty but not accepting → dead end, keep going
          * Otherwise: read first symbol b, find all states reachable via
            delta(state, b), push each as a new configuration (next_state, rest)
      - If stack empties without accepting → REJECT
    """
    stack = [(nfa["start"], input_string)]

    while stack:
        state, remaining = stack.pop()

        # Configuration where all input is consumed
        if remaining == "":
            if state in nfa["accept"]:
                return True
            else:
                continue  # dead end — try other branches

        # Read next symbol
        symbol = remaining[0]
        rest   = remaining[1:]

        # Push all possible next states onto the stack
        for (frm, sym, to) in nfa["transitions"]:
            if frm == state and sym == symbol:
                stack.append((to, rest))

    return False  # no accepting path found


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    filename = input("Please input the file name: ").strip()

    try:
        nfa, tests = parse_file(filename)
    except FileNotFoundError:
        print(f"Error: '{filename}.txt' not found.")
        return
    except ValueError as e:
        print(e)
        return

    if tests:
        # ── Batch mode: test strings provided in file ──
        results = []
        for s in tests:
            results.append("accepted" if simulate(nfa, s) else "rejected")
        print("(" + ", ".join(results) + ")")

    else:
        # ── Interactive mode: prompt user for strings ──
        first = True
        while True:
            prompt = "Please input a string: " if first else "Please input another string: "
            first  = False
            s = input(prompt).strip()
            if s == "":
                print("Bye bye.")
                break
            if simulate(nfa, s):
                print("Accepted.")
            else:
                print("Rejected.")


if __name__ == "__main__":
    main()
