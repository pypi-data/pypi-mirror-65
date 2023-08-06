from . import geo

def test_parse_poly():
    thing = """who
cares
\t1.2\t3.4
\t5.6\t7.8
END 
END """
    r =  geo.parse_poly(thing)
    print(f'r is {r}')
    assert len(r) == 1
    assert r[0][0] == [1.2,3.4]
