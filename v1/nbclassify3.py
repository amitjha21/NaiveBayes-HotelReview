import math
import sys
testCorpus = []
testvocabDict = {}
testvocabList = []
testvocabListFinal = []
testvocabListSp = []
priorDict = {}
postiveDict = {}
negativeDict = {}
deceptiveDict = {}
truthfulDict = {}
condProb = []
scoreT = 0.0
scoreD = 0.0
scoreP = 0.0
scoreN = 0.0
lineIdDict = {}
finalOutput = []
# open test file
if(len(sys.argv)<2):
    print("Error: No file parameter passed!")
    #exit()
testFiletoCheck = 'dev-text.txt' #sys.argv[1]
f1 = open(testFiletoCheck,'r')
l=0
for line in f1:
    l = l + 1
    rowToken = line.split(' ', 1)
    testCorpus.append(rowToken[1])
    lineIdDict[l] = rowToken[0]
f1.close()

#read nbModel.txt

nbM = open('nbmodel.txt','r')
c = 0;
for doc in nbM:
    c = c + 1
    doc =  doc.strip('\n')
    if c>=2 and c<=5:

        pr = doc.split(' ')
        priorDict[pr[0]] = pr[2]
    elif c>=9:
        condProb = doc.split('\t\t\t')
        truthfulDict[condProb[0]] = condProb[1]
        deceptiveDict[condProb[0]] = condProb[2]
        postiveDict[condProb[0]] = condProb[3]
        negativeDict[condProb[0]] = condProb[4]
        # print(doc)
nbM.close()
#prior Logs

logPriorTruth = math.log10(float(priorDict['Truth']))
logPriorDecp = math.log10(float(priorDict['Deceptive']))
logPriorPos = math.log10(float(priorDict['Positive']))
logPriorNeg = math.log10(float(priorDict['Negative']))

def strip_word(word):
    word = word.strip("(){}\'<\">?,.-!\;")
    return word

for st in testCorpus:
    st = st.lower()
    st = st.strip('\n')
    # print(st)
    tokenList = st.split(' ')
    testvocabListSp = list(tokenList)
    testvocabList = []
    for i in testvocabListSp:
            i = strip_word(i)
            testvocabList.append(i)
    testvocabListFinal.append(testvocabList)

print(len(testvocabListFinal))
m = 0
tempList = []
for row in testvocabListFinal:
    m = m + 1
    scoreT = logPriorTruth
    for val in row:
        if val in truthfulDict:
            scoreT = scoreT + math.log10(float(truthfulDict[val]))
    scoreD = logPriorDecp
    for val in row:
        if val in deceptiveDict:
            scoreD = scoreD + math.log10(float(deceptiveDict[val]))
    tempList.append(lineIdDict[m])
    if(scoreT>scoreD):
        tempList.append('truthful')
    else:
        tempList.append('deceptive')

    scoreP = logPriorPos
    for val in row:
        if val in postiveDict:
            scoreP = scoreP + math.log10(float(postiveDict[val]))
    scoreN = logPriorNeg
    for val in row:
        if val in negativeDict:
            scoreN = scoreN + math.log10(float(negativeDict[val]))
    # tempList.append(lineIdDict[m])
    if (scoreP > scoreN):
        tempList.append('positive')
    else:
        tempList.append('negative')

    finalOutput.append(tempList)
    tempList = []

finalw = open('nboutput.txt', 'w+')
for out in finalOutput:
    strOut = out[0] + ' ' + out[1] + ' ' + out[2] + '\n'
    finalw.write(strOut)
    strOut = ' '
finalw.close()


