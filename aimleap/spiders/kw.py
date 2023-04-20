import scrapy
import json

from scrapy import Request
from ..items import AgentItem
from scrapy.loader import ItemLoader

DETAIL_URL = ""

class KwSpider(scrapy.Spider):
    name = "kw"
    allowed_domains = ["kw.com"]
    url = "https://api-endpoint-cons-system.cons-prod-us-central1.kw.com/graphql"
    payload = json.dumps({
    "operationName": "searchAgentsQuery",
    "variables": {
        "searchCriteria": {
        "searchTerms": {
            "param1": "postalcode",
            "param2": "90010"
        }
        },
        "first": 300,
        "after": None,
        "queryId": "0.2118480420312865"
    },
    "query": "query searchAgentsQuery($searchCriteria: AgentSearchCriteriaInput, $first: Int, $after: String) {\n  SearchAgentQuery(searchCriteria: $searchCriteria) {\n    result {\n      agents(first: $first, after: $after) {\n        edges {\n          node {\n            ...AgentProfileFragment\n            __typename\n          }\n          __typename\n        }\n        pageInfo {\n          ...PageInfoFragment\n          __typename\n        }\n        totalCount\n        location {\n          city\n          state\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment PageInfoFragment on PageInfo {\n  endCursor\n  hasNextPage\n  __typename\n}\n\nfragment AgentProfileFragment on AgentProfileType {\n  id\n  name {\n    full\n    given\n    initials\n    __typename\n  }\n  image\n  location {\n    address {\n      state\n      city\n      __typename\n    }\n    __typename\n  }\n  realEstateEntity {\n    name\n    __typename\n  }\n  specialties\n  languages\n  isAgentLuxuryEnabled\n  phone {\n    entries {\n      ... on ContactSetEntryMobile {\n        number\n        __typename\n      }\n      ... on ContactSetEntryEmail {\n        email\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  agentLicenses {\n    licenseNumber\n    state\n    __typename\n  }\n  marketCenter {\n    market_center_name\n    market_center_address1\n    market_center_address2\n    __typename\n  }\n  __typename\n}\n"
    })
    headers = {
    'authority': 'api-endpoint-cons-system.cons-prod-us-central1.kw.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': '',
    'content-type': 'application/json',
    'origin': 'https://kw.com',
    'referer': 'https://kw.com/',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'x-datadog-origin': 'rum',
    'x-datadog-parent-id': '7861482205358451401',
    'x-datadog-sampling-priority': '1',
    'x-datadog-trace-id': '1296716685897060121',
    'x-shared-secret': 'MjFydHQ0dndjM3ZAI0ZHQCQkI0BHIyM='
    }
    
    def start_requests(self):
        yield Request(self.url, method="POST", headers=self.headers, callback=self.parse, body=self.payload)
        
    
    def parse(self, response):
        api = response.json()
        items = api.get("data", {}).get("SearchAgentQuery", {}).get("result", {}).get("agents", {}).get("edges")
        for item in items:
            id = item.get("node", {}).get("id")
            payload = json.dumps({
                "operationName": "agentProfileQuery",
                "variables": {
                    "id": id
                },
                "query": "query agentProfileQuery($id: IDProfileAgentScalar, $personID: Int, $slug: String) {\n  AgentProfileQuery(id: $id, personID: $personID, slug: $slug) {\n    id\n    isAgent\n    isActive\n    name {\n      full\n      initials\n      given\n      __typename\n    }\n    team\n    insights {\n      totalCount\n      __typename\n    }\n    startDate\n    numberOfSales\n    location {\n      address {\n        state\n        city\n        __typename\n      }\n      __typename\n    }\n    bio\n    kwuid\n    neighborhoods {\n      display\n      __typename\n    }\n    languages\n    phone {\n      entries {\n        ... on ContactSetEntryEmail {\n          email\n          __typename\n        }\n        ... on ContactSetEntryMobile {\n          number\n          __typename\n        }\n        ... on ContactSetEntryLandline {\n          number\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    image\n    website\n    brokeragePhone\n    brokerageLicense\n    agentLicenses {\n      licenseNumber\n      state\n      __typename\n    }\n    specialties\n    serviceAreas\n    isAgentLuxuryEnabled\n    designations\n    logo {\n      dba_logo\n      team_logo\n      __typename\n    }\n    marketCenter {\n      market_center_name\n      market_center_address1\n      market_center_address2\n      __typename\n    }\n    social {\n      facebook\n      instagram\n      linkedin\n      twitter\n      youtube\n      __typename\n    }\n    __typename\n  }\n}\n"
            })
            yield Request(self.url, method="POST", headers=self.headers, callback=self.parse_agent, body=payload)

    
    def parse_agent(self, response):
        agent = response.json()
        agent = agent.get("data", {}).get("AgentProfileQuery", {})
        l = ItemLoader(item=AgentItem(), selector=agent)
        
        l.add_value("AgentId", agent.get("id"))
        l.add_value("AgentImageUrl", agent.get("image"))
        l.add_value("AgentEmail", agent.get("phone", {}).get("entries"))
        l.add_value("AgentSite", agent.get("website"))
        l.add_value("AgentSocailMedia", agent.get("social", {}))
        l.add_value("AgentName", agent.get("name", {}).get("full"))
        l.add_value("AgentLicense", agent.get("agentLicenses", {}))
        l.add_value("AgentLocation", agent.get("location", {}).get("address", {}))
        l.add_value("AgentBranch", agent.get("team", ""))
        l.add_value("AgentContact", agent.get("phone", {}))

        yield l.load_item()



