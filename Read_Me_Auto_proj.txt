PROJECT: NFA Simulator (CS3383)
Group members: Jake, Ziyad, Gabe, Moe


Software and Apps used: VScode, Jupyter Notebook, 
Programming Language: Python
ENVIRONMENT: Cross-platform (Windows, Mac, Linux)


How to compile/run project in Windows:


FILES INCLUDED:
- runNFA.py           (The core simulator and parser)
- Report.pdf          (Detailed logic and data structure specs)
- readme.txt          (This instruction file)

Make sure project-1-machine-1.txt is in the same directory as NFA_simulator.py project.
In the terminal the program will ask you to input the project-1-machine.txt file, once typed in the terminal, program will ask for a string input.
String must end with 01 to be 'accepted', any combination of strings that doesn't end in 01 will say 'rejected'.
eventually user must input an empty string(enter key), and the program will terminate with "bye bye".

SOFTWARE REQUIREMENTS:
- This program requires a Python environment 
- No external libraries or "pip install" commands are required.

HOW TO RUN:
NOTE: If the python command isn't recognized, try using py runNFA.py or ensure Python is added to your system PATH.
1. Open your terminal or command prompt.
2. Navigate to the folder containing 'runNFA.py'.
3. Execute the program using:
   python runNFA.py
   
4. INPUT FILENAME: The program will prompt: "Please input the file name:".
   - Enter only the name of the file (e.g., proj-1-machine-1).
   - DO NOT include the .txt extension; the program appends it automatically.

PROGRAM MODES:
1. BATCH MODE: 
   If the input file contains a list of test strings in the second part of the 
   outer tuple, the program will process all of them, print the results as 
   a tuple (e.g., "(accepted, rejected)"), and exit.

2. INTERACTIVE MODE: 
   If the second part of the file tuple is empty (), the program enters 
   interactive mode. 
   - It will prompt "Please input a string:".
   - It will print "Accepted." or "Rejected." for each input.
   - To exit, simply press ENTER without typing anything.

TECHNICAL NOTES:
- The parser is custom-built to handle the nested tuple format without 
  using 'eval()', makes sure project works with project specifications
- The simulation uses a Depth-First Search (DFS) manage non-deterministic branches.
