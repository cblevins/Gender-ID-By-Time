#Gender Identification By Time
A Python program to identify the gender of personal names based on when a person may have been born.

Created in February 2014 by Bridget Baird and Cameron Blevins

##User Data
The user supplies input information in the form a tab-delimited text file with each row containing a separate full personal name (ex. <b>Zora Neale Hurston</b>). Any additional columns with associated data will be copied and outputted without modification (ex. <b>Their Eyes Were Watching God</b>).

##Temporal Matching 
The main contribution of this program is its ability to dynamically identify the gender of a name based on temporal data. "Madison", for instance, was a male name in 1900, but a female name in 2000. This program can account for those shifts. It does so by attempting to calculate a range of dates for when a person may have been born based on the following information: 

*   An "event date" associated with a particular person. 
*   The approximate age range of the overall population of names.

For instance, the user might have a transcribed police registry of arrests. The user can specify an approximate age range for the bulk of this "population" - say, 18 to 40. If there are years associated with each arrest, the program will use this age range in conjunction with the wedding date. If someone named "Madison" was arrested in 1934, the program calculates that out of all of the people named "Madison" aged 18 to 40 in 1934, 100% of them were MALE. If the arrest took place in 2008, it calculates that out of all the people named "Madison" aged 18 to 40 in 2008, 82.8% of them were FEMALE. If the user does not have an "event date" they can assign a default year that gives the program a rough sense of when the data was from.

##Output 
The program produces a tab-delimited text file with six new columns added to the user's original file:

1. The first name it tried to identify 
2. The gender of that name - Male, Female, or Unknown 
3. Percentage of total matches of that name that were female (Ex. "99.2") 
4. Percentage of total matches of that name that were male (Ex. "0.8")
5. Beginning of date range in which it calculated gender of a name
6. End of date range in which it calculated gender of a name

##Reference Data 
By default the program uses a database of text files containing personal names from the Social Security Administration, from 1880 to 2012. Each text file represents one year's worth of recorded births. Each line in the text file consists of a personal name and how many times that name was given to either a male or female baby (ex. in 1891 there were 52 female babies that were given the name "Zora"). The user can supply their own reference files provided they follow the same data format. The program also uses two additional text files containing suffixes (ex. "Jr.") and prefixes (ex. "Dr.") that the program will ignore when it tries to match a name. These lists of prefixes and suffixes can be modified by the user.
