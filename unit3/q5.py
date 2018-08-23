import sqlite3
import sys
import re
import math
from sqlite3 import Error

global cur, nnlist

def main():
    global cur, nnlist
    dbpath = sys.argv[1]
    x = float(sys.argv[2])
    y = float(sys.argv[3])
    k = int(sys.argv[4])
    point = (x, y)
    nnlist = [[-1,math.inf]]*k
    cur = connect_to_database(dbpath)
    find_node(1,point)
    for i in range(len(nnlist)):
        print("ID: %d - Distance: %f" % (nnlist[i][0],nnlist[i][1]))

def connect_to_database(path):
    try:
        connection = sqlite3.connect(path)
        cur = connection.cursor()
    except Error as e:
        exit("Cannot connect to database")
    return cur

def branch_list(node):
    query = (
        '''
    SELECT rtreenode(2,data)
    FROM areaMBRTree_node
    WHERE nodeno=?;
        '''
    )
    input_tuple = (node,)
    cur.execute(query,input_tuple)
    result = cur.fetchone()
    return result

def find_node(node,point):
    global nnlist
    list_string = branch_list(node)
    # leaf_node reached
    if list_string is None:
        result = leaf(node)
        coor = [(result[1]+result[2])/2,(result[3]+result[4])/2]
        actual_dist = point_dist(point,coor)
        for i in range(len(nnlist)):
            if actual_dist < nnlist[i][1]:
                if i == 0:
                    update = []
                    new = (result[0],actual_dist)
                    last = nnlist[:-1]
                    update.append(new)
                    nnlist = list(update+last)
                    break
                elif i == len(nnlist)-1:
                    nnlist[i] = (result[0],actual_dist)
                    break
                else:
                    first = nnlist[:i]
                    new = (result[0],actual_dist)
                    last = nnlist[i:-1]
                    first.append(new)
                    nnlist = list(first + last)
                    break
    # there are still nodes to be found
    else:
        branched_list = []
        before_formatting = re.findall("\{(.*?)\}", list_string[0])
        for i in range(len(before_formatting)):
            branched_list.append(before_formatting[i].split(' '))
        for k in range(len(branched_list)):
            for j in range(len(branched_list[i])):
                if j == 0:
                    branched_list[k][j] = int(branched_list[k][j])
                else:
                    branched_list[k][j] = float(branched_list[k][j])
        updated_list = list(branched_list)
        dist_list = []

        for item in branched_list:
            mindist = min_dist(point,item)
            minmaxdist = min_max_dist(point, item)
            dist_list.append([item[0],mindist,minmaxdist])
        ABL = sorted(dist_list, key=lambda dist_list: dist_list[1])
        pruned_ABL = list(ABL)

        # Pruning
        minmaxdist = ABL[0][2]
        for i in range(len(ABL)):
            if ABL[i][1] >= minmaxdist:
                pruned_ABL.remove(ABL[i])
                break

        for item in range(len(pruned_ABL)):
            if nnlist[-1][1] != math.inf:
                if nnlist[-1][1] >= pruned_ABL[item][2]:
                    nnlist[-1] = (pruned_ABL[item][0],ABL[item][2])
                    break

        index = 0
        currentlen = len(pruned_ABL)
        while index < currentlen-1:
            if pruned_ABL[index][1] >= nnlist[-1][1]:
                pruned_ABL.remove(pruned_ABL[index])
                currentlen -= 1
            else:
                find_node(pruned_ABL[index][0],point)
                index += 1

def leaf(node):
    query = (
    '''
    SELECT id, minX, maxX, minY, maxY
    FROM areaMBRTree
    WHERE id=?
    '''
    )
    input_tuple = (node,)
    cur.execute(query, input_tuple)
    result = cur.fetchone()
    return result

def point_dist(point,coor):

    x = abs(point[0]-coor[0])**2
    y = abs(point[1]-coor[1])**2
    result = math.sqrt(x+y)
    return result

def min_dist(point, node):
    # node = [id,minX,maxX,minY,maxY]

    pointx = point[0]
    pointy = point[1]

    # x ----------
    if pointx < node[1]:
        rx = node[1]
    elif pointx > node[2]:
        rx = node[2]
    else:
        rx = pointx

    # y ----------
    if pointy < node[3]:
        ry = node[3]
    elif pointy > node[4]:
        ry = node[4]
    else:
        ry = pointy

    result = (pointx-rx)**2 + (pointy-ry)**2
    return result

def min_max_dist(point, node):
    # node = [id,minX,maxX,minY,maxY]

    pointx = point[0]
    pointy = point[1]

    if pointx >= (node[1]+node[2])/2:
        rmx_i = node[1]
    else:
        rmx_i = node[2]

    if pointy >= (node[3]+node[4])/2:
        rmy_i = node[3]
    else:
        rmy_i = node[4]

    # first ----------
    if pointx <= (node[1]+node[2])/2:
        rmx_k = node[1]
    else:
        rmx_k = node[2]
    minx = (pointx - rmx_k)**2 +((pointx - rmx_i)**2 +(pointy - rmy_i)**2)

    # second ----------
    if pointy <= (node[3] + node[4]) / 2:
        rmy_k = node[3]
    else:
        rmy_k = node[4]
    miny = (pointy - rmy_k)**2 +((pointx - rmx_i)**2 +(pointy - rmy_i)**2)

    return min(minx,miny)

main()
