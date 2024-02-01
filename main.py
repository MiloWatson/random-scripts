from bs4 import BeautifulSoup
import json
import re

with open('isa_providers.html', 'r', encoding='utf-8') as file:
    html = file.read()

soup = BeautifulSoup(html, 'html.parser')

providers = []

for h3_tag in soup.find_all('h3'):

    provider = h3_tag.text.replace('  ', ' ').replace(u"\u2018", "'").replace(u"\u2019", "'").strip()
    tradingAs = provider
    tradingSearch = '(trading as '

    if tradingSearch in provider:
        provider = provider.split(tradingSearch)[0].strip()
        tradingAs = tradingAs.split(tradingSearch)[1].strip()[:-1]

    address = h3_tag.find_next('div', class_='address')

    addressList = list(filter(None, address.text.splitlines()))
    addressText = ', '.join(addressList).replace(u"\u2018", "'").replace(u"\u2019", "'")

    details = address.find_next_sibling('p')
    detailsText = details.text
    detailsList = details.text.splitlines()

    refRegex = r"Reference: (.+)"
    fcaRegex = r"FCA reference: (.+)"
    compRegex = r"Components offered: (.+)"

    reference = re.search(refRegex, detailsText)[1]
    fcaReference = re.search(fcaRegex, detailsText)[1]
    components = re.search(compRegex, detailsText)[1]
    componentsArray = components.split(',')
    cleanedComponents = [c.strip(' ') for c in componentsArray]

    providerJSON = {
        'provider_name': provider,
        'provider_trading_name': tradingAs,
        'provider_address': addressText,
        'provider_reference': reference,
        'provider_fca_reference': fcaReference,
        'components_offered': cleanedComponents
    }

    providers.append(providerJSON)


with open('provider.json', 'w', encoding='utf-8') as f:
    json.dump(providers, f, ensure_ascii=False, indent=4)
