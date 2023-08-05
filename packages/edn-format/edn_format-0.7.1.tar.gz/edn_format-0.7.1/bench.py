# -*- coding: UTF-8 -*-

import timeit

try:
    import cProfile as profile
except ImportError:
    import profile

test_load = False

from edn_format import loads, dumps

import json

with open("bench2.json") as f:
    py = json.load(f)

#with open("bench1.edn") as f:
#    edn = f.read()

if test_load:
    print("Load")
    print(timeit.timeit('loads(edn)', globals=globals(), number=200))

    profile.runctx('for _ in range(100): loads(edn)',
            globals=globals(), locals=locals())

# 2079966 function calls (2061017 primitive calls) in 1.963 seconds

# 3223103 function calls (3223003 primitive calls) in 2.765 seconds
# 3223103 function calls (3223003 primitive calls) in 2.775 seconds
# 3223103 function calls (3223003 primitive calls) in 2.756 seconds

# 3223103 function calls (3223003 primitive calls) in 2.929 seconds

#py = loads(edn)
#print ("--------------------------")
#print("Dump")
#print(timeit.timeit('dumps(py,indent=2)', globals=globals(), number=1000))

profile.runctx('for _ in range(200): dumps(py)',
        globals=globals(), locals=locals())
