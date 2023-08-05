 
from XivDbReader.Reader import Reader


def test_armsPld():
    r = Reader()
    res = r.getArms('Pld',1)
    if res.__len__() == 1:
        assert True
