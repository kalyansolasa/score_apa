"""Misc utils"""
import itertools
import six

if six.PY2:
    zip_longest = itertools.izip_longest
else:
    from itertools import zip_longest

def diff_rec(left,
             right,
             ignore_keys={},
             comp_mode='dp',
             precision=6):
    '''
    Given two generic structures left and right, this will return
    a map showing their diff. It uses recursive drill down, so do
    not use on structures which have big depth!

    ignore_keys:
        set of keys to be ignored during comparison

    Global variables used by diff_rec:

    comp_mode:
        Numerical comparison modes. Must be one of
            - sf : significant figures
            - dp : decimal places
            - pc : percentage change
    precision:
        precision depending on the mode:
        if comp_mode='sf' then significant figures to round to before comparison
        if comp_mode='dp' then decimal places to round to before comparison
        if comp_mode='pc' then percentage change required to trigger diff
    '''
    ignore_keys = set(ignore_keys)

    def diff_rec_(left,
                  right):
        diffs = {}
        left_is_dict = isinstance(left, dict)
        right_is_dict = isinstance(right, dict)
        if left_is_dict and right_is_dict:
            left_keys = set(left.keys())
            right_keys = set(right.keys())
            shared_keys = left_keys & right_keys - ignore_keys
            only_in_left_keys = left_keys - right_keys - ignore_keys
            only_in_right_keys = right_keys - left_keys - ignore_keys
            map_diffs = {}
            for key in shared_keys:
                res = diff_rec_(left[key], right[key])
                if res:
                    if 'ValDiff' not in map_diffs:
                        map_diffs['ValDiff'] = {}
                    map_diffs['ValDiff'][key] = res
            if only_in_left_keys:
                tmp_map = {}
                for k in only_in_left_keys:
                    tmp_map[k] = left[k]
                map_diffs['OnlyInLeft'] = tmp_map
            if only_in_right_keys:
                tmp_map = {}
                for k in only_in_right_keys:
                    tmp_map[k] = right[k]
                map_diffs['OnlyInRight'] = tmp_map
            if map_diffs:
                diffs = map_diffs
            # do dict compare
        elif not left_is_dict and not right_is_dict:
            left_is_iterable = hasattr(left, '__iter__')
            right_is_iterable = hasattr(right, '__iter__')
            if isinstance(left, str):
                left_is_iterable = False
            if isinstance(right, str):
                right_is_iterable = False
            if left_is_iterable and right_is_iterable:
                iterable_diffs = {}
                idx = -1
                for item1, item2 in zip_longest(left, right):
                    idx += 1
                    res = diff_rec_(item1, item2)
                    if res:
                        iterable_diffs[idx] = res
                if iterable_diffs:
                    diffs = iterable_diffs
            elif not left_is_iterable and not right_is_iterable:
                if left != right:
                    if comp_mode == 'sf':
                        try:
                            left_num = ('%%.%dg' % (int(precision))) % (left)
                            right_num = ('%%.%dg' % (int(precision))) % (right)
                            if left_num != right_num:
                                diffs = (left, right, right - left)
                        except:
                            diffs = (left, right)
                    elif comp_mode == 'dp':
                        try:
                            left_num = ('{0:.%sf}' % (int(precision))).format(float(left))
                            right_num = ('{0:.%sf}' % (int(precision))).format(float(right))
                            if left_num != right_num:
                                diffs = (left, right, right - left)
                        except:
                            diffs = (left, right)
                    elif comp_mode == 'pc':
                        try:
                            if abs(right - left) / float(abs(left)) >= precision:
                                diffs = (left, right, right - left)
                        except:
                            diffs = (left, right)
                    else:
                        raise Exception("comp_mode='%s' not supported" % (comp_mode))
            else:
                diffs = (left, right)
        else:
            diffs = (left, right)
        return diffs

    return diff_rec_(left, right)
