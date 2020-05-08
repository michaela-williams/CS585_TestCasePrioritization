# CS585_TestCasePrioritization

The artifact is a Python 3.2.3 program. It will not work with Python 3.8 or any version newer than 3.8 due to the removal of time.clock().
Before attempting to run TestPriortize.py, TestShareData.csv.zip must be properly downloaded using the Git Large File System, unzipped, and the resulting file moved into the directory where the other repository files are saved.
Do not open TestData.csv before running the artifact. Excel's randomization functions may run again and change the data, so you might receive different results when using the artifact.

Assuming you have a compatible version of Python installed, you should be able to get the results described in the paper by doing the following:
  Windows:
    -Open Command Prompt
    -navigate to the folder where you saved the repository
    -run "py TestPrioritize.py"
  MacOS/Linux:
    -Open a terminal
    -navigate to the folder where you saved the repository
    -run "python3 TestPrioritize.py"
  
This will produce results for detecting 90% of failing test suites. The report also covers 95% and 98%, so if you would like to generate these results as well, you should open TestPrioritize.py and change the value of the percentFailures variable at line 8 to the .95 or .98 and run the program again.
