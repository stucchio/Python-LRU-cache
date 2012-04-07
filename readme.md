# Introduction

It's often useful to have an in-memory cache. Of course, it's also desirable not to have the cache grow too large, and cache expiration is often desirable.

This module provides such a cache.

Rather than reading the readme, I recommend you just look at the doctests in the code. For the most part, you can just use it like this:

    from lru import lru_cache_function

    @lru_cache_function(max_size=1024, expiration=15*60)
    def f(x):
        print "Calling f(" + str(x) + ")"
        return x

    f(3) # This will print "Calling f(3)", will return 3
    f(3) # This will not print anything, but will return 3 (unless 15 minutes have passed between the first and second function call).
