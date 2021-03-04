# log = {'car':[0,1,0,0,0,1,0],'bus':[1,0,0,0,0,0,1],'walk':[0,0,1,0,0,0,0]}
# group = {'overall':['car', 'bus', 'walk'],'vehicle':['car', 'bus']}

# # convert log to bool
# for k in log:
#     for i in range(len(log[k])):
#         if log[k][i] == 0:
#             log[k][i] = False
#         else:
#             log[k][i] = True
# print(log)

# def add_two_ls(l1, l2):
#     length = len(l1)
#     ans = [0] * length
#     for i in range(length):
#         if l1[i] == True:
#             ans[i] += 1
#         if l2[i] == True:
#             ans[i] += 1
#     return ans

# res = dict()
# res_len = 0
# for nums in log.values():
#     res_len = len(nums)
#     break

# for k, v in group.items():
#     res[k] = [0] * res_len
#     for method in v:
#         res[k] = add_two_ls(log[method], res[k])
# print(res)

# f = open("abc.txt")
# # text = f.readline()
# while text:=f.readline():
#     print(text)

# funcs = dict()
# def foo(fname):
#     return fname
# funcs['a']() = foo
# print(funcs)

# class I:
#     num = 0
#     def __init__(self):
#         self.num = 0
#     def add(cls):
#         I.num += 1
#         return I.num

# import os
# import stat

# size = os.stat('./abc.txt')[stat.ST_SIZE]
# print(size)

# s = ("Edar", "A", "a")
# info = "Hello %s %s ,,%s"
# print(info % s)

# v = [[1, 2], [3, 4], [5,6], [7, 8], [9, 0]]
# a = (x for y in v for x in y if x % 2 == 0)
# for item in a:
#     c = item
#     print(item)

# from functools import reduce
# x = reduce(lambda x, y: [y] + x, list(range(5)), [])
# print(x)

# import re

# test = "Blue aaa"
# a = re.findall(r'Blue', test)[0]
# print(a)

# stringlengths = {"abc":2, "babasd": 6}
# def okl(input_tuple):
#     (s, l) = input_tuple
#     return l >= 3 and l <= 10
# stringlength = dict(list(filter(okl, list(stringlengths.items()))))

# print(stringlength)

# def swap (foo, bar):
#     y = foo;
#     Foo = bar;
#     bar = y;
#     print ("foo inside the function: :", foo) 
#     print ("bar inside the function: ", bar) 
#     return (foo, bar)
# foo =5
# bar = 15
# print ("foo before sending to function: ", foo) 
# print ("bar before sending to function: ", bar) 
# x = swap (foo,bar)
# print ("foo after sending to function: ", x[0]) 
# print ("bar after sending to function: ", x[1])


# import asyncio
# async def main():
#     print('Hello ...')
#     await asyncio.sleep(1)
#     print(".... World! ")

# asyncio.run(main())

# n = 12
# names = [[]] * n
# emp = "a"
# m = 3
# names[m].append(emp)
# print(names)

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.ops import nearest_points
from geopy.distance import geodesic

polygon_data = [[24.527338,118.103198], [24.527373, 118.103224],[24.527366, 118.103236],[24.527331, 118.103209],[24.527338, 118.103198]]

# polygon_data = [[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]
point_data = [24.527352,118.10321675]
# point_data = [0.5, 5]
polygon = Polygon(polygon_data)
point = Point(point_data)
boundary_obj = nearest_points(polygon, point)[0]
nearest_point = boundary_obj.bounds[:2]
dist = geodesic(point_data, nearest_point).meters
print(dist)