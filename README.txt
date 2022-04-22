README for Programming Project 1 - Bloom Filter

1 - Extraction
    Extract the .tar file.
    This file contains the bloom filter program, as well as the required input files (dictionary.txt and input.txt)

2 - Compilation
    Nah, I'm just messing with you. It's Python; no need to compile.

3 - Running the program.
    The program can be run by running the command "python3 giguierc_bloom_filter.py". If no command line arguments are provided, the program will attempt to run with the default file names.
    (i.e. input.txt, dictionary.txt, output3.txt, and output5.txt)

    These files can be specified as command-line arguments using the following flags in this order:
    -d: name of dictionary file (i.e dictionary.txt)
    -i: name of file containing passwords to test (i.e input.txt)
    -o3: where to store the output for Bloom Filter with 3 hashing functions (i.e output3.txt)
    -o5: where to store the output for Bloom Filter with 5 hashing functions (i.e output5.txt)

    Note: I have also included a sh script (ez.sh) that will run the program with the default arguments. 
    This file can be modified in order to use different input files without retyping a lengthy command.

4 - Notes
    On my CPU (AMD Ryzen 3800x), the program takes approximately 5 seconds to execute with the provided dictionary and input file.
    Most of this time is spent hashing the massive dictionary file.
