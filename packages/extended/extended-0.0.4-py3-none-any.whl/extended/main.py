
from .iterable import tally, counts, counts_by
from .indexing import first, last, rotate_left, rotate_right, partition
from .numbertests import even_q, odd_q
from .nesting import nest_while_list, nest_while, nest, nest_list
from .classes import up_to


#%%
    

# def group_by(x,key=None,return_fn=None):
#     d = {}
#     for i in x:
#         try:
#             d[key(i)] += [i]
#         except:
#             d[key(i)] = [i]
#     if return_fn:
#         return [[return_fn(i) for i in j] for j in list(d.values())]
#     else:
#         return d

# def gather_by(x, **kwargs):
#     return list(group_by(x, **kwargs).values())


# def delete_duplicates(x):
#     return list(group_by(x,key=lambda x:x).keys())

