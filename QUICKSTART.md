#Gender Identification By Time
A Python program to identify the gender of personal names based on when a person may have been born.

Created in February 2014 by Bridget Baird and Cameron Blevins

##Quick Start Guide
1. Create a directory that contains:
  * GenderID.py
  *	ReferenceData folder
  *	A text file containing names whose gender you want identified
  *	prefixLst.txt
  *	suffixLst.txt
2. Open GenderID.py
  * Specify the name of the input file containing your data
  * Specify the name of the output file in which the program will write the results
  * If you have dates associated with your names, leave dateVaries = True. If not, change it to dateVaries = False, then change the defaultYear variable to an approximate year for your data.
  * If you have FULL names (first and last names together) in the first column, leave firstLastTogether = True. If you only have first names in this column, change it to firstLastTogether = False.
3. Open your text file. Make sure the first column contains names and the second column contains dates (if you have them).
4. Run the program.