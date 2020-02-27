# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 18:31:30 2019

@author: yuansiyu
"""
import time
import copy

def construct(address):
    '''
    goal：读取文档并将大图和子图转化为可以进行操作的数据结构
    address   图地址
    vi: label, out_degree, out_edge, in_degree, in_edge
    '''
    f = open(address)
    line = f.readline()
    line_ = line.replace('\n','')
    line_ = line.split('\t')
    V = int(line_[0])
    E = int(line_[1])
    ls = []
    while line:
        line = f.readline()
        line_ = line.replace('\n','')
        line_ = line_.split('\t')
        ls.append(line_)
    f.close()    
    
    vertexs = {}
    edges = []
    for i in range(V,E+V):
        edges.append(ls[i])
    for i in range(V):
        #{vi:label, out_degree, out_edge, in_degree, in_edge}
        vertexs['{}'.format(i)] = [ls[i][0], 0, [],0,[]]   
    for element in edges:
        # out
        vertexs[element[0]][1] = vertexs[element[0]][1] + 1
        vertexs[element[0]][2].append(element)
        # in
        vertexs[element[1]][3] = vertexs[element[1]][3] + 1
        vertexs[element[1]][4].append(element)
    return vertexs, edges

def check_pair(pair, g_edges, indexs, G_edges):
    '''
    goal：检查重复度和边条件
    G_edges     大图边集合
    g_edges     小图边集合
    indexs       查找顺序
    '''
    pair = pair.split(' ')
    #检验重复度
    list1=pair
    list2=[]
    for i in list1:
        if i not in list2:
            list2.append(i)
    if len(list1) != len(list2):
        return False
    
    #检查边条件
    check_element = pair[-1]
    length = len(pair)-2
    orgin_element = indexs[length + 1]
    while length >= 0:
        for edge in g_edges:
            if indexs[length] == edge[0] and orgin_element == edge[1]:
                check_pair1 = [pair[length], check_element, edge[2]]
                if check_pair1 not in G_edges:
                    return False
            elif indexs[length] == edge[1] and orgin_element == edge[0]:
                check_pair2 = [check_element, pair[length], edge[2]]
                if check_pair2 not in G_edges:
                    return False
        length = length - 1
    return True
    
def check_select(newselect, g_edges, indexs, G_edges):
    '''
    goal：检验候选集
    G_edges     大图边集合
    g_edges     小图边集合
    indexs       查找顺序
    '''
    #针对每一个pair进行检查
    select = []
    for pair in newselect:
        flag = check_pair(pair, g_edges, indexs, G_edges)
        if flag is True:
            select.append(pair)
    return select

def label(vertexs):
    '''
    goal：统计所给边集合label数量
    '''
    label_count = {}
    for key in vertexs.keys():
        if vertexs[key][0] not in label_count:
            label_count[vertexs[key][0]] = 1
        else:
            label_count[vertexs[key][0]] = label_count[vertexs[key][0]] + 1
    return label_count

def order_index(label_count, indexs, g_vertexs):
    '''
    Turbo算法
    label_count  是一个字典，统计大图中每个label出现的次数
    g_vertexs    小图顶点集合
    indexs       查找顺序
    '''
    rank = {}
    for ele in indexs:
        rank[ele] = label_count[g_vertexs[ele][0]]/float(g_vertexs[ele][1]+g_vertexs[ele][3])
    rank = sorted(rank.items(),key=lambda x:x[1])
    temp = []
    for ele in rank:
        temp.append(ele[0])
    indexs = temp
    return indexs
def cut_G_edges(G_vertexs, G_edges, g_vertexs, g_edges):
    '''
    goal：缩小G_edges的搜索空间
    G_vertexs   大图顶点集合
    G_edges     大图边集合
    g_vertexs   小图顶点集合
    g_edges     小图边集合
    '''
    G_edges1 = copy.deepcopy(G_edges)
    ls = []
    for edge in g_edges:
        ls.append((g_vertexs[edge[0]][0],g_vertexs[edge[1]][0]))
    ls = list(set(ls))
    temp = []

    for edge in G_edges1:
        if (G_vertexs[edge[0]][0],G_vertexs[edge[1]][0]) not in ls:
            G_vertexs[edge[0]][1] = G_vertexs[edge[0]][1] - 1
            G_vertexs[edge[0]][2].remove(edge)
            G_vertexs[edge[1]][3] = G_vertexs[edge[1]][3] - 1
            G_vertexs[edge[1]][4].remove(edge)
            edge.append(-1)
        else:
            edge.append(1)
    temp = []
    for edge in G_edges1:
        if edge[-1] == 1:
            temp.append(edge[:-1])
    G_edges = temp

    return G_edges

def cut_G_vertexs(G_vertexs, label_g_count):
    '''
    goal：          缩小G_vertexs的搜索空间
    G_vertexs       大图顶点集合
    label_g_count   小图label和所对应的数量（字典）
    '''
    G_vertexs1 = copy.deepcopy(G_vertexs)
    c = []
    for key in label_g_count.keys():
        c.append(key)
    temp = {}
    for key in G_vertexs1.keys():
        if G_vertexs1[key][0] in c:
            temp[key] = G_vertexs1[key]
    G_vertexs = temp
    
    return G_vertexs

def NOVA(vertexs,edges):
    '''
    goal:实现NOVA算法
    vertexs   顶点集合
    edges     边集合
    '''
    graph_index = {}
    graph_index['out'] = {}
    graph_index['in'] = {}
    for key in vertexs.keys():
        graph_index['out'][key] = {}
        graph_index['in'][key] = {}
        for ele in vertexs[key][2]:
            label = vertexs[ele[1]][0]
            graph_index['out'][key][label] = graph_index['out'][key].setdefault(label, 0) + 1
        for ele in vertexs[key][4]:
            label = vertexs[ele[0]][0]
            graph_index['in'][key][label] = graph_index['in'][key].setdefault(label, 0) + 1
    return graph_index

def check_cliques(neighbor, label, max_cliques, edges):
    '''
    goal:检查neighbor是否应该放入max_cliques中
    neighbor    待检查的邻居
    label       对应边的label
    max_cliques 当前的maximal clique
    edges       边集合
    '''
    check = 1
    for v in max_cliques:
        if [v, neighbor, label] not in edges and [neighbor, v, label] not in edges:
            check = 0
    return check

def max_cliques(key, vertexs, edges):
    '''
    goal:寻找含有顶点key的maximum clique
    vi: label, out_degree, out_edge, in_degree, in_edge
    key          顶点key
    vertexs      点集合
    edges        边集合
    neighbors    顶点key的所有邻居节点及其标签
    '''
    #获取邻居节点
    neighbors = {}
    for edge in vertexs[key][2]:
        neighbors[edge[1]] = edge[2]
    for edge in vertexs[key][4]:
        neighbors[edge[0]] = edge[2]
    max_cliques = []
    max_cliques.append(key)
    for key in neighbors.keys():
        check = check_cliques(key, neighbors[key], max_cliques, edges)
        if check != 0:
            max_cliques.append(key)
    return len(max_cliques)

def Subgraph_Search(G_vertexs, G_edges, g_vertexs, g_edges, elapsed):
    '''
    goal:子图查询
    G_vertexs   大图顶点集合
    G_edges     大图边集合
    g_vertexs   小图顶点集合
    g_edges     小图边集合
    elapsed     时间记录
    indexs      查找顺序
    '''
    start = time.clock()
    candidate = {}
    label_G_count = label(G_vertexs)
    indexs = []#查找顺序
    indexs = order_index(label_G_count, indexs, g_vertexs)
    G_edges = cut_G_edges(G_vertexs, G_edges, g_vertexs, g_edges)  
    label_g_count = label(g_vertexs)
    G_vertexs = cut_G_vertexs(G_vertexs, label_g_count)
    G_index = NOVA(G_vertexs, G_edges)
    g_index = NOVA(g_vertexs, g_edges) 
    elapsed.append(time.clock() - start)
    result = []
    
    #查询时间起始点
    start = time.clock()
    for key1 in g_vertexs.keys():
        candidate[key1] = []
        for key2 in G_vertexs.keys():
            #the first filter:考虑自身的标签，度
            if g_vertexs[key1][0] == G_vertexs[key2][0] and g_vertexs[key1][1] <= G_vertexs[key2][1] and g_vertexs[key1][3] <= G_vertexs[key2][3]:
                #the second filter:考虑邻居标签和度
                flag = 1
                for key in g_index['in'][key1]:
                    if key not in G_index['in'][key2]:
                        flag =  0
                    else:
                        if g_index['in'][key1][key] > G_index['in'][key2][key]:
                            flag = 0
                for key in g_index['out'][key1]:                    
                    if key not in G_index['out'][key2]:
                        flag = 0                    
                    else:
                        if g_index['out'][key1][key] > G_index['out'][key2][key]:
                            flag = 0
                #the third filter:考虑子图点和大图点的最大独立集合
                if flag:
                    g_max_cliques = max_cliques(key1, g_vertexs, g_edges)
                    G_max_cliques = max_cliques(key2, G_vertexs, G_edges)
                    if g_max_cliques <= G_max_cliques:
                        candidate[key1].append(key2)
        if len(candidate[key1]) == 0:
            elapsed.append(time.clock() - start)
            return [], elapsed
    select = []
    for key1 in g_vertexs.keys():
        indexs.append(key1)
    i = 0

    for add in candidate[indexs[i]]:
        select.append(add)
    i = i + 1
    while i < len(indexs):
        newselect = []
        for element in select:
            for add in candidate[indexs[i]]:
                newselect.append(element + ' ' + add)
        #关键步骤
        select = check_select(newselect, g_edges, indexs, G_edges)
        i = i + 1
    #结果构建

    for element in select:
        result_element = []
        temp =  element.split(' ')
        for key in g_vertexs.keys():
            ind = indexs.index(key)
            result_element.append(temp[ind])
        result.append(result_element)
    elapsed.append(time.clock() - start)
    return result, elapsed

def write_file(result, elapsed, G_address):
    '''
    goal:结果输出
    result    结果
    elapsed   运行时间
    '''
    a = G_address.split('\\')
    b = a[0]
    for i in range(1, len(a)-1):
        b = b + '\\' + a[i]
    f = open(b + "\\MRresults.txt", "w")
    f.write('Indexing time: {}ms //time consumed from receiving G to finishing the index'.format(elapsed[0]*60+elapsed[1]*60)+'\n')
    f.write('Querying time: {}ms//time consumed from receiving g to outputting matches'.format(elapsed[2]*60)+'\n')
    f.write('Total time: {}ms'.format(elapsed[0]*60+elapsed[1]*60+elapsed[2]*60)+'\n')
    length = len(result)
    if length == 0:
        f.write('no match')
        f.close()
        return
    f.write(str(length)+'\n')
    for i in range(length):
        f.write('match_{}'.format(i+1)+'\n')
        for element in result[i]:
            f.write(str(element)+'\n')
    f.close()

if __name__ == '__main__':
    G_address = 'D:\data.txt'
    G_vertexs, G_edges = construct(G_address)
    g_address = 'D:\subdata.txt'
    elapsed = []
    start = time.clock()
    g_vertexs, g_edges = construct(g_address)
    elapsed.append(time.clock() - start)
    result, elapsed = Subgraph_Search(G_vertexs, G_edges, g_vertexs, g_edges, elapsed)
    write_file(result, elapsed, G_address)
