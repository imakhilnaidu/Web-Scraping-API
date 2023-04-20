from scrapy import Item, Field
from itemloaders.processors import MapCompose, TakeFirst



def get_license(agent):
    if agent is not None:
        lic_num = agent.get("licenseNumber")
        state = agent.get("state")
        return f"{lic_num} ({state})"
    

def get_email(details):
    email = details.get("email")
    if email:
        return email
    else:
        return ""

def get_contact(details):
    details = details.get("entries")
    mob = [d.get("number") for d in details if d.get("__typename") == "ContactSetEntryMobile"]
    off = [d.get("number") for d in details if d.get("__typename") == "ContactSetEntryLandline"]
    return {"mobile": mob[0] if mob else "", "office": off[0] if off else ""}


def get_mob(details):
    if details.get("__typename") == "ContactSetEntryMobile":
        mob = details.get("number")
        if mob:
            return mob
        else:
            return ""



def get_off(details):
    if details.get("__typename") == "ContactSetEntryLandline":
        off = details.get("number")
        if off:
            return off
        else:
            return ""


def get_location(agent):
    city = agent.get("city", "")
    state = agent.get("state", "")
    
    return f"{city}, {state}"


def get_branch(team):
    if team:
        return f"Real Estate Agent at {team}"
    return ""


class AgentItem(Item):
    AgentId = Field(output_processor=TakeFirst())
    AgentName = Field(output_processor=TakeFirst())
    AgentBranch = Field(input_processor = MapCompose(get_branch), output_processor=TakeFirst())
    AgentEmail = Field(input_processor = MapCompose(get_email), output_processor=TakeFirst())
    AgentLocation = Field(input_processor = MapCompose(get_location), output_processor=TakeFirst())
    AgentImageUrl = Field(output_processor=TakeFirst())
    AgentLicense = Field(input_processor = MapCompose(get_license), output_processor=TakeFirst())
    AgentSite = Field(output_processor=TakeFirst())
    AgentSocailMedia = Field(output_processor=TakeFirst())
    AgentContact = Field(input_processor = MapCompose(get_contact), output_processor=TakeFirst())
