
from XivDbReader.scrape import ParseList
from XivDbReader.settings import Settings
import pytest

class TestArmsLinks():
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
        #links = ri.FindLinks('*')

        if len(ri) == 50:
            assert True