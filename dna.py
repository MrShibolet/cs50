from csv import reader, DictReader
from sys import argv

if len(argv) != 3:
    print("Usage error, dna.py sequence.txt database.csv")
    exit()
# extract the seq from the database into a list pop last result
with open(argv[1]) as pfile:
    first = reader(pfile)
    for row in first:
        dnaseq = row
        dnaseq.pop(0)
        break
#create a directory for use
seq = {}
#copy into dictionary from dnaseq
for item in dnaseq:
    seq[item] = 1
#Open the szequences file and read the first line as row into list
with open(argv[2]) as seqf:
    seqread = reader(seqf)
    for row in seqread:
        dlist = row
#Go over the entire sequence directory of SRTs available
for j in seq:
#get the length of how much to check (changes between the smaller and bigger file)
    l = len(j)
    maximum = 0
    counter = 0
#go over the range of the entire sequest
    for i in range(len(dlist[0])):
        #rester the counter if it's not reset already
        if counter > 0:
            counter = 0
        #check to see if current SRT is a match
        if dlist[0][i: i + l] == j:
            #do while SRT sequence is a match and count it advancing 1 SRT at a time with i
            while dlist[0][i - l: i] == dlist[0][i: i + l]:
                counter += 1
                i += l
            #added because of bug that last result only came through, this way it shows maximum
            if counter > maximum:
                maximum = counter
    #insert maximum into the current SRT of the current sequence being checked
    seq[j] += maximum
#go over the CSV people file again
with open(argv[1]) as file:
    csvfile = DictReader(file)
    #go over every entry
    for i in csvfile:
        #var to see if we have a match
        trigger = 0
        for j in seq:
            if seq[j] == int(i[j]):
                trigger += 1
        #if we have a complete match print
        if trigger == len(seq):
            print(i['name'])
            exit()
print("No match")