'''A Python program to take in a list of names and try to identify their gender based on when they might have been born.
Created by Bridget Baird and Cameron Blevins, February 2014'''

import os, string

###### SET INITIAL VALUES HERE ###############################

inFileName='exampleInput.txt'             #name of input file (your data)
outFileName='exampleOutput.txt'           #name of output file
subfolderName="ReferenceData"     #subfolder containing the database of names and genders

dateVaries=True                 #set to False if your data does NOT have its own date information in it (ex. the publication years for authors' books)
defaultYear=1980                #if your data does NOT have its own date information, select an approximate year for your dataset

minAge=18                       #approximate "floor" of your population's age range
maxAge=40                       #approximate "ceiling" of your population's age range

headerPresent=True      #set to False if input file has no header
nameCol=0              #column in input file containing names - default is the first column (index 0)
dateCol=1              #column in input file containing years (if present) - default is the second column (index 1)
firstLastTogether=True  #set to False if only first name(s) are present in the name colun

threshold=80          #the minimum threshold, on a scale from 0-100, for determining the gender binary of a name.

prefixFileName="prefixLst.txt"     #name of file containing list of prefixes to ignore
suffixFileName="suffixLst.txt"     #name of file containing list of suffixes to ignore

########## PROGRAM ###############################

##read in all the info from the input file
def readInfo():
    infile=open(inFileName,'r')
    lst=[]
    headerLst=[]
    if headerPresent:   #get header titles for later use
        header=infile.readline()    
        header=header.strip("\n")
        headerLst=header.split("\t")
                        #read file and store information in a list
    for line in infile:
        line=line.strip("\n")
        line=line.replace('"','')
        oneLineLst=line.split("\t")
        lst.append(oneLineLst)                
    infile.close()
    return lst, headerLst    

##read in database of names for all years, calculate totals
##nameLst is list of [year,tot,[name,gender,number]]
##also find first and last years in the database
def readDatabaseNames():
    allNamesLst=[]
    minDate=0
    maxDate=0
                        #read through all the files and gather info
    fileLst = os.listdir(subfolderName)
    for oneFile in fileLst:
        year=int(oneFile[3:7])
        if minDate==0 or year<minDate: minDate=year
        if maxDate==0 or year>maxDate: maxDate=year
        infile=open(subfolderName+"/" +oneFile,"r")
        yearLst=[]
        for line in infile:
            line=line[:-1]
            one=line.split(',')
            one[2]=int(one[2])  #third column is an integer
            yearLst.append(one)
        infile.close()
        allNamesLst.append([year,yearLst])
    return allNamesLst, minDate,maxDate                    

##find first and last years: 
##use minAge and maxAge
##if back too far start with firstDate
def findFirstLastDate(date,minDate,maxDate):
    if date==-1: return -1,-1
    start=date-maxAge
    if start<minDate: start=minDate
    if start>maxDate: start=maxDate
    last=date-minAge
    if last<minDate: last=minDate
    if last>maxDate: last = maxDate
    return start, last

##find last name and a list of first names
##take away suffixes and prefixes
def findFirstLastNames(name):
    namelst=[]
    name=name.replace(',','')
    if firstLastTogether:
        name=name.strip('.')
        lst=name.split()
        if len(lst)>0 and ((lst[-1] in suffixLst) or (lst[-1]+'.' in suffixLst)):
            lst=lst[:-1]
        if len(lst)>0:              #take off last name
            lst=lst[:-1]
    else: lst=name.split()
    for one in lst:
        one=one.strip('.')
        one=one.strip(',')
        if one in prefixLst or (one+'.') in prefixLst: continue
        if len(one)<=1: continue
        namelst.append(one)
    return namelst
            
##Use lookup list from start to last dates to count gender matches
def findGender(name, start, last):
    totM=0
    totF=0
    for entry in allNamesLst:
        if start<=entry[0]<last:
                    ##linear search
##            for item in entry[1]:
##                if name==item[0]:
##                    if item[1]=="F": totF+=item[2]
##                    else: totM+=item[2]
                    ##binary search for name match
            f,m=binSearch(name,entry[1])
            totF+=f
            totM+=m
    return totF,totM

##binary search on names- return num of female and male matches
def binSearch(name,lst):
    f,m=0,0
    length=len(lst)
    start=0
    end=length
    found=False
    while not found and start<end:
        i=(start+end)/2
        if lst[i][0]==name:
            found=True
        elif lst[i][0]>name:
            end=i-1
        else: start=i+1
    if found:
        if lst[i][1]=="F":
            f=lst[i][2]
            if i<length and lst[i+1][0]==name:
                m=lst[i+1][2]
        if lst[i][1]=="M":
            m=lst[i][2]
            if i>0 and lst[i-1][0]==name:
                f=lst[i-1][2]
    return f,m
               
##  Read in column of words and put in list
def readinList(fileName):
    lst=[]
    infile=open(fileName,'r')
    for line in infile:
        line=line.strip("\n")
        lst.append(line)
    return lst


####################################    main program   #####################    
def main():
    global allNamesLst
    global prefixLst
    global suffixLst
                    #nameLst has list of [year,[name,gender,number]]
    allNamesLst, minDate,maxDate=readDatabaseNames()
                    #read in the names to be gender matched
    lst, headerLst=readInfo()
                    #read in files containing suffixes and prefixes
    prefixLst=readinList(prefixFileName)
    suffixLst=readinList(suffixFileName)
                    #open outfile and write header
    outfile=open(outFileName,'w')
    outfile.write("Name\tGender\tPercentFemale\tPercentMale\t")
    if headerPresent:
        for title in headerLst:
            outfile.write(title+"\t")
    outfile.write("\n")
    count=0
    for line in lst:
        totF,totM =0,0
        if dateVaries:
            if len(line[dateCol])==4:  #date is present
                date=int(line[dateCol])
            else: date=-1
        else: date=defaultYear
                    #find range of dates to use for lookup
        if date!=-1:
            firstDate, lastDate=findFirstLastDate(date,minDate,maxDate)
                        #find last name (if there) and list of first name(s)
            namelst=findFirstLastNames(line[nameCol])
                        #find gender
            for entry in namelst:   #go through first names
                totF,totM=findGender(entry,firstDate,lastDate)                   
                if totF!=0 or totM!=0: break    #exit if have a match
                    #find gender and percentages
            gender="U"          
            female,male=0.0,0.0
            if totF!=0 or totM!=0:
                female=float(totF)/(totF+totM)
                male=float(totM)/(totF+totM)
                female=round((female*100),1)
                male=round((male*100),1)
                if female>=threshold: gender="F"
                elif male>=threshold: gender="M"           
                        #write gender info into the outfile
            outfile.write(' '.join(namelst)+"\t"+gender+"\t"+str(female)+"\t"+str(male)+"\t")
        else:           #no date
            outfile.write("\t"+"\t"+"\t"+"\t")

        for i in range(len(line)):      #write original information also
            if type(line[i])==str:
                outfile.write(line[i]+"\t")
            else: outfile.write(str(line[i])+"\t")
        outfile.write("\n")                
        count+=1
        if count%1000 ==0: print "Finished "+str(count)
    outfile.close()
    
main()
