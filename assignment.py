import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd


class Scraper:
    def __init__(self, url: str) -> None:
        self.url = url

    def fetchData(self) -> str:
        response = requests.get(self.url)
        raw_data = response.text
        return raw_data

    def parseData(self) -> None:
        # fetch the data first
        raw_data = self.fetchData()

        # parse the data
        soup = BeautifulSoup(raw_data, 'lxml')
        dom = etree.HTML(str(soup))

        # this will find featured ul tags of 4 different price sections
        path = '//*[@class="zp-text-14 zp-leading-18 zp-px-12 mq-1024:zp-px-0 mq-1188:zp-px-12"]/ul'
        ul_tags = dom.xpath(path)
        pricing_sections = [section for section in ul_tags]

        # this will find features of 4 different categories
        free, team, organization, enterprice = pricing_sections
        free_features = free.xpath('li/text()')
        team_features = team.xpath('li/text()')
        org_features = organization.xpath('li/text()')
        ent_features = enterprice.xpath('li/text()')
        all_features = free_features + team_features + org_features + ent_features

        # this will store the metadata of features
        plan_amount = []
        free_tag = []
        team_tag = []
        org_tag = []
        ent_tag = []

        # get data ready for DataFrame
        for _ in free_features:
            plan_amount.append('0$')
            free_tag.append('yes')
            team_tag.append('yes')
            org_tag.append('yes')

        for _ in team_features:
            plan_amount.append('8$')
            free_tag.append('No')
            team_tag.append('yes')
            org_tag.append('yes')

        for _ in org_features:
            plan_amount.append('16$')
            free_tag.append('No')
            team_tag.append('No')
            org_tag.append('yes')

        for _ in ent_features:
            plan_amount.append('Contact')
            free_tag.append('No')
            team_tag.append('No')
            org_tag.append('No')

        for _ in all_features:
            ent_tag.append('yes')

        # create DataFrame
        df = pd.DataFrame({'features': all_features, 'Plan_amount': plan_amount,
                          'Free': free_tag, 'Team': team_tag, 'Organization': org_tag, 'Enterprice': ent_tag})
        df.columns = [['Features', 'Plan_amount', 'Is_present', 'Is_present', 'Is_present', 'Is_present'], [
            '', '', 'Free 0$', 'Team 8$', 'Organization 16$', 'Enterprice']]

        # convert dataframe to excel file
        df.to_csv('pricing_data.csv', index=False)


url = 'https://zeplin.io/pricing/'
crawler = Scraper(url)
crawler.parseData()
