import articleSimilarity as asim


def test_compare_strings():
    a = ['ala', 'ala']
    [(_, _, val)] = asim.compare_strings(a)
    assert val == 1

    a = ['a', 'b', 'c']
    [(_, _, a), (_, _, b), (_, _, c)] = asim.compare_strings(a)
    assert a == 0 and b == 0 and c == 0

    test_str = 'ala ma kota kot ma ale'.split()
    ret = asim.compare_strings(test_str)
    v = len(test_str)
    assert len(ret) == v * (v - 1) / 2


def test_convert_tuple_list_to_lists():
    t1 = (1, 2, 'ala')
    t2 = (3, 4, 'kot')
    t3 = (5, 6, 'pies')
    l = [t1, t2, t3]

    expected = [(1, 3, 5), (2, 4, 6), ('ala', 'kot', 'pies')]
    returned = asim.rotate_tuple_list(l)

    for ret, exp in zip(returned, expected):
        for r, e in zip(ret, exp):
            assert r == e

