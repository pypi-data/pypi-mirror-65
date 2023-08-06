# (c) 2012-2018 Dativa, all rights reserved
# -----------------------------------------
#  This code is licensed under MIT license (see license.txt for details)

#!python
#cython: language_level=3, boundscheck=False, wraparound=False, optimize.use_switch=True
import math

cpdef _get_marginal_score(long long pop_size,
                          long long item_label,
                          dict  scores,
                          bint infer_missing,
                          int default_value):
    cdef double score = 0
    cdef int skipped = 0
    cdef int run = 0
    cdef double total_scored = 0
    cdef double total_skipped = 0
    cdef double permutation_score
    cdef int i
    cdef long long label
    cdef long long subset_label
    cdef double subset_score
    cdef double superset_score

    for label in scores:
        if label & item_label > 0:
            run = run + 1
            subset_label = label - item_label
            superset_score = scores.get(subset_label + item_label, default_value)
            subset_score = scores.get(subset_label, default_value)

            total_scored = total_scored + superset_score

            if subset_label > 0 and infer_missing and (superset_score == 0 or subset_score == 0):
                if superset_score > 0 or subset_score > 0:
                    skipped = skipped + 1
                    total_skipped = total_skipped + superset_score

            else:
                j = len([a for a in bin(subset_label) if a == '1'])
                score = score + (superset_score - subset_score) * math.factorial(j) * math.factorial(pop_size - j - 1)

    return score, skipped, run, total_scored, total_skipped
