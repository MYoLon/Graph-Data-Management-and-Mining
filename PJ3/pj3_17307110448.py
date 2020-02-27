# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 08:45:30 2020

@author: yuansiyu

说明：
1.Google的反爬虫机制让我无法从Google上爬取搜索结果，更糟糕的是，本来可以实现在百度上爬取搜索结果。
  但是在2020年初，百度的反爬虫机制加强，又无法爬取百度搜索结果，故而无法实现之前的想法。
2.由于数据集较大（咨询助教后顶点数会达到1000以上），直接生成G^2图会导致运行过慢，故而查询相关资料
  找到了networkx包，采用此包来加快运行速度
3.由于无法爬虫，故而对语义的处理变成观察数据集中边标签的情况。
"""
import networkx as nx
import time
import math


def construct(address):
    '''
    goal：读取文档并将大图和子图转化为可以进行操作的数据结构
    address   图地址
    vi: label
    '''
    f = open(address,'r',encoding = 'utf-8-sig')
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
    edges = {}
    for i in range(V,E+V):
        edges[(ls[i][0], ls[i][1])] = ls[i][2]
    for i in range(V):
        #{vi:label, out_degree, out_edge, in_degree, in_edge}
        vertexs['{}'.format(i)] = ls[i][0]
    return vertexs, edges



def simrank(G_vertexs, G_edges, edge_labels, pair, G1):
    '''
    goal:返回两个点对相似度的得分
    G_vertexs:   大图顶点集合
    G_edges:     大图边集合
    edge_labels: 边label个数统计
    pair:      第一对点对
    G1:          图信息
    '''

    try:
        #如果这两个标签
        dist = nx.shortest_path_length(G1,source = int(pair[0]),target = int(pair[1]))
    except:
        dist =  0
        
    #距离
    if dist == 0:
        score = 0
    else:
        score = 1/dist
    #结构相似性
    p1_in_degree = G1.in_degree(int(pair[0]))
    p2_in_degree = G1.in_degree(int(pair[1]))
    
    if p1_in_degree == p2_in_degree:
        score = score + 1
    else:
        score = score + 1/abs(p1_in_degree - p2_in_degree)
        
    p1_out_degree = G1.out_degree(int(pair[0]))
    p2_out_degree = G1.out_degree(int(pair[1]))
    
    if p1_out_degree == p2_out_degree:
        score = score + 1
    else:
        score = score + 1/abs(p1_out_degree - p2_out_degree)
    
    #语义相似性
    
    in_neighbors_p1 = list(G1.predecessors(int(pair[0])))
    in_neighbors_p2 = list(G1.predecessors(int(pair[1])))

    out_neighbors_p1 = list(G1.successors(int(pair[0])))
    out_neighbors_p2 = list(G1.successors(int(pair[1])))
    
    label_in = []
    label_out = []
    
    #若两个节点与入邻居和出邻居的标签相似，那么这两个节点是相似的    
    for key1 in in_neighbors_p1:
        if key1 in in_neighbors_p2:
            score = score + 1
            label_in.append(key1)
    
    for key2 in out_neighbors_p1:
        if key2 in out_neighbors_p2:
            score = score + 1
            label_out.append(key2)
            
    #若节点标签出现频率越低，那么它的价值越高
    for key1 in label_in:
        score = score + 1/edge_labels[G_edges[(str(key1), pair[0])]]
        
    for key2 in label_out:
        score = score + 1/edge_labels[G_edges[(pair[0], str(key2))]]
 
    return score

def write_file(result1, result2, elapsed, G_address):
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
    f.write('{} //score of the first pair'.format(result1)+'\n')
    f.write('{} //score of the second pair'.format(result2)+'\n')
    f.write('Time cost: {} ms'.format(elapsed[0]*60)+'\n')
    f.close()

if __name__ == '__main__':
    print("please input the address of G" + '\n')
    G_address = input()
#    G_address = "D:\dataset.txt"
    G_vertexs, G_edges = construct(G_address)
    print("Please enter the first point pair" + '\n')
    pair_1 = input()
    
    pair_1 = pair_1.split(",")
    print("Please enter the second point pair" + '\n')
    pair_2 = input()
            
    elapsed = []
    start = time.clock()
    
    pair_2 = pair_2.split(",")
    G1 = nx.DiGraph()
    for i in range(len(G_vertexs)):
        G1.add_node(i)
    for element in G_edges:
        G1.add_edges_from([(int(element[0]),int(element[1]))])
    
    edge_labels = {}
    for element in G_edges.keys():
        edge_labels[G_edges[element]] = edge_labels.setdefault(G_edges[element], 0) + 1
        

    score1 = simrank(G_vertexs, G_edges, edge_labels, pair_1, G1)
    score2 = simrank(G_vertexs, G_edges, edge_labels, pair_2, G1)
    
    #归一化，使得相似度小于1，也使得两个节点可以比较
    result1 = score1 / (score1 + score2)
    result2 = score2 / (score1 + score2)
    
    elapsed.append(time.clock() - start)
    write_file(result1, result2, elapsed, G_address)
