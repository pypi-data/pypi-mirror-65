
from XivDbReader.scrape import ParseList
from XivDbReader.settings import Settings
import pytest

class test_ArmsLinks():
    # Storing the html code so we do not have to hit the external site over and over.
    pytest.arms_html = ''
    pytest.arms_url = ''

    @pytest.fixture
    def getHtmlSource(self):
        if pytest.arms_html == '':
            s = Settings()
            pytest.arms_url = s.armsAllUrl
            pl = ParseList(s.armsAllUrl)
            pytest.arms_html = pl.FindLinks(pytest.arms_url)

    def test_FindLinksArms(self, getHtmlSource):
        ri = ParseList(pytest.arms_html)
        links = ri.FindLinks()

        if len(links) == 50:
            assert True

def test_FindLinksTools():
    s = Settings()
    ri = ParseList(s.toolsAllUrl)
    links = ri.FindLinks()

    if len(links) == 50:
        assert True
    
def test_FindLinksArmor():
    s = Settings()
    ri = ParseList(s.armorAllUrl)
    links = ri.FindLinks()

    if len(links) == 50:
        assert True

def test_FindLinksAccessories():
    s = Settings()
    ri = ParseList(s.accessoriesAllUrl)
    links = ri.FindLinks()

    if len(links) == 50:
        assert True

def test_FindLinksMeds():
    s = Settings()
    ri = ParseList(s.medsAllUrl)
    links = ri.FindLinks()

    if len(links) == 50:
        assert True

def test_FindLinksFood():
    s = Settings()
    ri = ParseList(s.foodAllUrl)
    links = ri.FindLinks()

    if len(links) == 50:
        assert True

def test_FindLinksMaterials():
    s = Settings()
    ri = ParseList(s.materialsAllUrl)
    links = ri.FindLinks()

    if len(links) == 50:
        assert True



