import json
import collections

def grid_dict(jsonpath):
    """
    type jsonpath: String, the path where stores fenceID and its grids
    """
    f=open(jsonpath,"r")
    content=f.readline()
    f.close()
    fence_grid = json.loads(content)
    grid_fence = collections.defaultdict(set)
    for k, v in fence_grid.items():
        for grid in v:
            grid_fence[grid].add(k)
    for k in grid_fence:
        grid_fence[k] = list(grid_fence[k])
    return grid_fence

if __name__ == '__main__':
    j = './app/source/fence_grids.json'
    out_dic = grid_dict(j)
    f = open('./app/source/grid_fences', 'w')
    f.write(json.dumps(out_dic))
    f.close()
    