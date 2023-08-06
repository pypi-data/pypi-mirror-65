# cython: language_level=3, wraparound=False, boundscheck=False

cimport numpy as np
import numpy as np

import warnings

from .divsufsort import divsufsort 


ctypedef fused sa_t:
    np.int32_t
    np.int64_t

ctypedef fused string_t:
    np.uint8_t
    np.uint16_t
    np.uint32_t
    np.uint64_t
    np.int8_t
    np.int16_t
    np.int32_t
    np.int64_t


def handle_input(s):
    if isinstance(s, np.ndarray):
        # in my tests, converting to contiguous and using [::1]
        # gives *slightly* better performance than using [:]
        if not s.flags["C_CONTIGUOUS"]:
            # Make a contiguous copy of the numpy array.
            s = np.ascontiguousarray(s)
    if isinstance(s, str):
        try:
            s = s.encode("ascii")
            if len(s) > 999:
                warnings.warn("converting str argument uses more memory")
        except UnicodeEncodeError:
            raise TypeError("str must only contain ascii chars")
    return s


def _kasai(string_t[::1] s not None, sa_t[::1] sa not None):

    cdef sa_t i, j, n, k
    cdef np.ndarray[sa_t, ndim=1] lcp = np.empty_like(sa) 
    cdef np.ndarray[sa_t, ndim=1] rank = np.empty_like(sa)
        
    n = len(sa)

    for i in range(n):
        rank[sa[i]] = i

    k = 0
    for i in range(n):
        if rank[i] == n - 1:
            lcp[n-1] = k = 0
            continue
        j = sa[rank[i] + 1]
        while i + k < n and j + k < n and s[i+k] == s[j+k]:
            k += 1
        lcp[rank[i]] = k
        if k:
            k -= 1

    return lcp

def _kasai_bytes(const unsigned char[::1] s not None, sa_t[::1] sa not None):
    """Same as _kasai but with a const first argument.
    Cython does not support const fused types arguments YET
    but it will be fixed in the 0.30 release
    <https://github.com/pandas-dev/pandas/issues/31710>
    """
        
    cdef sa_t i, j, n, k
    cdef np.ndarray[sa_t, ndim=1] lcp = np.empty_like(sa) 
    cdef np.ndarray[sa_t, ndim=1] rank = np.empty_like(sa)
        
    n = len(sa)

    for i in range(n):
        rank[sa[i]] = i

    k = 0
    for i in range(n):
        if rank[i] == n - 1:
            lcp[n-1] = k = 0
            continue
        j = sa[rank[i] + 1]
        while i + k < n and j + k < n and s[i+k] == s[j+k]:
            k += 1
        lcp[rank[i]] = k
        if k:
            k -= 1

    return lcp

def kasai(s, sa=None):
    s = handle_input(s)
    if sa is None:
        sa = divsufsort(s)
    if isinstance(s, bytes):
        return _kasai_bytes(s, sa)
    return _kasai(s, sa)

def _lcp_segtree(
        string_t[::1] s not None,
        np.ndarray[sa_t, ndim=1] sa not None,
        np.ndarray[sa_t, ndim=1] lcp not None
    ):

    cdef sa_t i, j, n, k
    
    cdef np.ndarray[sa_t, ndim=1] segtree = np.concatenate([np.empty_like(lcp), lcp])
    cdef np.ndarray rank = np.empty_like(sa)
        
    n = len(sa)
    for i in range(n-1, 0, -1):
        segtree[i] = min(segtree[i << 1], segtree[i << 1 | 1])
    
    for i in range(n):
        rank[sa[i]] = i

    return rank, segtree


def lcp_segtree(s, sa=None, lcp=None):
    s = handle_input(s)
    if sa is None:
        sa = divsufsort(s)
    if lcp is None:
        lcp = kasai(s, sa)
    if isinstance(s, bytes):
        # tofix
        s = bytearray(s)
    return _lcp_segtree(s, sa, lcp)


def lcp_query(
        np.ndarray[sa_t, ndim=1] rank not None,
        np.ndarray[sa_t, ndim=1] segtree not None,
        queries
    ):
    cdef sa_t n, q, i

    # note: l and r could hold 2*n-1
    # fortunately, n is at most int64
    cdef unsigned long long l, r

    n = len(rank)
    q = len(queries)

    cdef np.ndarray[sa_t, ndim=1] ans = np.empty(q, dtype=segtree.dtype)

    # TODO: parallelize
    # prange throws a lot of errors
    for i in range(q):
        l, r = queries[i]
        res = n - max(l, r)
        l, r = rank[l], rank[r]
        if r < l:
            l, r = r, l
        l += n
        r += n
        while l < r:
            if l&1:
                if segtree[l] < res:
                    res = segtree[l]
                l += 1
            if r&1:
                r -= 1
                if segtree[r] < res:
                    res = segtree[r]
            l >>= 1 
            r >>= 1 
        ans[i] = res
    return ans