#+
# Very simple generator function to import to Python interactive
# prompt. Things to try:
#
#     iter_list = iter123()
#     next(iter_list)
#     next(iter_list)
#     next(iter_list)
#     next(iter_list) # will automatically raise StopIteration when iterator terminates
#
# also
#
#     for i in iter123() :
#         print(i)
#     #end for
#
# also
#
#      iter_list = iter123()
#      next(iter_list, "nomore") # 1
#      next(iter_list, "nomore") # 2
#      next(iter_list, "nomore") # 3
#      next(iter_list, "nomore") # 'nomore'
##-

def iter123() :
    yield 1
    yield 2
    yield 3
#end iter123
