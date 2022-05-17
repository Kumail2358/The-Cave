import pprint

def addNodes(G, node):
    if node not in G:
            G[node] = []

def addEdges(G, edge):
    if len(edge)==3:
        weight = edge[2]
        G[edge[0]].append((edge[1], *weight))
    else:
        G[edge[0]].append((edge[1],1))

def evaluator(s):
    if s == '.':
        return []
    lst = s.split('.')
    for i in range(len(lst)):
        lst[i] = lst[i].split(',')
        lst[i][0] = int(lst[i][0])
        try:
            lst[i][2] = eval(lst[i][2])
        except:
            pass
    if len(lst)==1:
        return lst[0]
    return lst


def createNodeData(filename):
    gameFile = open(filename, encoding="utf8")
    lst = gameFile.read()
    lst = lst.split('\n')
    gameFile.close()
    for i in range (len(lst)):
        lst[i] = lst[i].split('\t')
        lst[i][0] = int(lst[i][0])
        lst[i][-1] = evaluator(lst[i][-1])
    return lst

infoList = []

def createGraph(dataList):
    G = {}
    global infoList
    for nodeData in dataList:
        addNodes(G, nodeData[0])
        infoList.append(nodeData[1:5])
        if nodeData[3] in ['choices', 'karma']:
            for tup in nodeData[-1]:
                addEdges(G, (nodeData[0],tup[0],tup[1:]))
        else:
            for node in nodeData[-1]:
                addEdges(G, (nodeData[0], node))
    return G


dataList = createNodeData("The Cave.txt")
G = createGraph(dataList)

# print(dataList)
# print()
# pprint.pprint(G)
# pprint.pprint(infoList)

karma = 0

def adjust_Karma(score):
    global karma
    karma += score

def display(G, node):
    global infoList

    print(infoList[node][3],'\n')

    if infoList[node][2] == "straight" or infoList[node][2] == "start":
        display(G,G[node][0][0])

    elif infoList[node][2] == "choices":
        for i in range(len(G[node])):
            print(i,G[node][i][1])
        choice = int(input("\nSelect a choice: "))
        adjust_Karma(G[node][choice][2])
        display(G,G[node][choice][0])

    elif infoList[node][2] == "karma":
        for i in range(len(G[node])):
            if eval(str(karma)+G[node][i][2]):
                display(G,G[node][i][0])
display(G, 0)
        