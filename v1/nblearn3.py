# from sets import Set
import sys
CONST_POSITIVE = 'positive'
CONST_NEGATIVE = 'negative'
CONST_DECEPTIVE = 'deceptive'
CONST_TRUTHFUL = 'truthful'

labelInput = []
textInput_Dict = {}
positiveClass = []
negativeClass = []
truthfulClass = []
deceptiveClass = []
vocalList = []
vocalDict = {}
priorProbDict = {}
condProbList = []
positiveTokenClass = []
negativeTokenClass = []
truthfulTokenClass = []
deceptiveTokenClass = []
positiveClassCount = 0
negativeClassCount = 0
truthfulClassCount = 0
deceptiveClassCount = 0

# ----------------------------------------------
# open label file
if(len(sys.argv)<2):
    print("Error: No file parameter passed!")
    #exit()
trainingTextFile = 'train-text.txt' #sys.argv[1]
trainingLabelFile = 'train-labels.txt'  #sys.argv[2]

f = open(trainingLabelFile,'r')
# print(f.name,end='\n')

for line in f:
    labelInput.append(line)

# open text review file
f1 = open(trainingTextFile,'r')
# print(f1.name,end='\n')

for line in f1:
    rowToken = line.split(' ', 1)
    textInput_Dict[rowToken[0]] = rowToken[1]

# Get stop words in a set

st = open('stop-words.txt','r')
lstStop = []
for stopW in st:
    lstStop.append(stopW.strip('\n'))
stopWordsSet = set(lstStop)

# build 4 classes
for labRow in labelInput:
    labRowToken = labRow.split(' ')
    labRowId = labRowToken[0]
    honestClass = labRowToken[1]
    sentimentClass = labRowToken[2].strip('\n')

    if sentimentClass == CONST_POSITIVE:
        positiveClass.append(textInput_Dict[labRowId])
    else:
        negativeClass.append(textInput_Dict[labRowId])
    if honestClass == CONST_TRUTHFUL:
        truthfulClass.append(textInput_Dict[labRowId])
    else:
        deceptiveClass.append(textInput_Dict[labRowId])

# create vocabulary
# 1. Read dict line by line and convert all to small case
# 2. Split at spaces and check if there is anything other than string
# 3. Insert it into vacabDict
# to_remove = "()"
# table = str.maketrans(" ", " ", to_remove)


def strip_word(word):
    word = word.strip("(){}\'<\">?,.-!\;")
    return word

for st in textInput_Dict.values():
    st = st.lower()
    st = st.strip('\n')
    tokensWithoutStop = {}
    vocalList = []
    # print(st)
    tokenList = st.split(' ')
    tokensWithoutStop = set(tokenList) - stopWordsSet
    vocalList = list(tokensWithoutStop)
    for i in vocalList:
        i = str(i)
        if i != ' ':
            i = strip_word(i)
            vocalDict.setdefault(i)
   # print(tokensWithoutStop)
print(len(vocalDict))
test = {}
test = set(vocalDict) - stopWordsSet
vocalDict = dict.fromkeys(test)

# create list for each class
for st in positiveClass:
    st = st.lower()
    st = st.strip('\n')
    tokenList = st.split(' ')
    for i in list(tokenList):
        i = strip_word(i)
        positiveTokenClass.append(i)

for st in negativeClass:
    st = st.lower()
    st = st.strip('\n')
    tokenList = st.split(' ')
    for i in list(tokenList):
        i = strip_word(i)
        negativeTokenClass.append(i)

for st in truthfulClass:
    st = st.lower()
    st = st.strip('\n')
    tokenList = st.split(' ')
    for i in list(tokenList):
        i = strip_word(i)
        truthfulTokenClass.append(i)

for st in deceptiveClass:
    st = st.lower()
    st = st.strip('\n')
    tokenList = st.split(' ')
    for i in list(tokenList):
        i = strip_word(i)
        deceptiveTokenClass.append(i)

# Get total count for terms in feature
for i in vocalDict.keys():
    positiveClassCount = positiveClassCount + positiveTokenClass.count(i)

for i in vocalDict.keys():
    negativeClassCount = negativeClassCount + negativeTokenClass.count(i)

for i in vocalDict.keys():
    truthfulClassCount = truthfulClassCount + truthfulTokenClass.count(i)

for i in vocalDict.keys():
    deceptiveClassCount = deceptiveClassCount + deceptiveTokenClass.count(i)

# prior probablity
totalDoc = len(textInput_Dict)
priorProbDict['Positive'] = len(positiveClass) / totalDoc
priorProbDict['Negative'] = len(negativeClass) / totalDoc
priorProbDict['Truth'] = len(truthfulClass) / totalDoc
priorProbDict['Deceptive'] = len(deceptiveClass) / totalDoc

# Get probablities
def countTerm(c, t):
    return c.count(t)

for term in vocalDict.keys():
    l1 = []
    if term == '':
        continue
    l1.append(term)
    countofTerm = truthfulTokenClass.count(term)
    cpT = (countofTerm + 1) / (truthfulClassCount + len(vocalDict))
    l1.append(cpT)
    countofTerm = deceptiveTokenClass.count(term)
    cpD = (countofTerm +1) / (deceptiveClassCount + len(vocalDict))
    l1.append(cpD)
    countofTerm = positiveTokenClass.count(term)
    cpP = (countofTerm + 1) / (positiveClassCount + len(vocalDict))
    l1.append(cpP)
    countofTerm = negativeTokenClass.count(term)
    cpN = (countofTerm + 1)/ (negativeClassCount + len(vocalDict))
    l1.append(cpN)
    condProbList.append(l1)

fw = open('nbmodel.txt', 'w+')
fw.write('Prior Probablities:\n')
for i in  priorProbDict.items():
    st = str(i[0]) + ' : ' + str(i[1]) + '\n'
    fw.write(st)
    st = ''
header = '\n\nTerm' + '\t\t\t' + 'Truthful' + '\t\t\t' + 'Deceptive' + '\t\t\t' + 'Positive' + '\t\t\t' + 'Negative\n'
fw.write(header)
for j in range(len(condProbList)):
    data = str(condProbList[j][0]) + '\t\t\t' + str('{:.15f}'.format(condProbList[j][1])) + '\t\t\t' + str('{:.15f}'.format(condProbList[j][2])) + '\t\t\t' + str('{:.15f}'.format(condProbList[j][3])) + '\t\t\t' + str('{:.15f}'.format(condProbList[j][4])) + '\n'
    fw.write(data)
    data = ''
fw.close()
print('File Generated Successfully')


# create count
