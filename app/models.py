from pydantic import BaseModel
from enum import Enum
from sqlmodel import SQLModel, Field


class agentname(SQLModel, table=True):
    name_id: int = Field(primary_key=True)
    first_name: str
    last_name: str
    email: str
    phone: str
    pollingunit_uniqueid: int


class announced_lga_results(SQLModel, table=True):
    result_id: int = Field(primary_key=True)
    lga_name: str
    party_abbreviation: str
    party_score: str
    entered_by_user: str
    date_entered: str
    user_ip_address: str


class announced_pu_results(SQLModel, table=True):
    result_id: int = Field(primary_key=True)
    polling_unit_uniqueid: str
    party_abbreviation: str
    party_score: int
    entered_by_user: str
    date_entered: str
    user_ip_address: str


class announced_state_results(SQLModel, table=True):
    result_id: int = Field(primary_key=True)
    state_name: str
    party_abbreviation: str
    party_score: int
    entered_by_user: str
    date_entered: str
    user_ip_address: str


class announced_ward_results(SQLModel, table=True):
    result_id: int = Field(primary_key=True)
    ward_name: str
    party_abbreviation: str
    party_score: str
    entered_by_user: str
    date_entered: str
    user_ip_address: str


class lga(SQLModel, table=True):
    uniqueid: int = Field(primary_key=True)
    lga_id: int
    lga_name: str
    state_id: int
    lga_description: str
    entered_by_user: str
    date_entered: str
    user_ip_address: str


class party(SQLModel, table=True):
    id: int = Field(primary_key=True)
    partyid: str
    partyname: str


class polling_unit(SQLModel, table=True):
    uniqueid: int = Field(primary_key=True)
    polling_unit_id: int
    ward_id: int
    lga_id: int
    uniquewardid: int
    polling_unit_number: str
    polling_unit_name: str
    polling_unit_description: str
    lat: str
    long: str
    entered_by_user: str
    date_entered: str
    user_ip_address: str


class states(SQLModel, table=True):
    state_id: int = Field(primary_key=True)
    state_name: str


class ward(SQLModel, table=True):
    uniqueid: int = Field(primary_key=True)
    ward_id: int
    ward_name: str
    lga_id: int
    ward_description: str
    entered_by_user: str
    date_entered: str
    user_ip_address: str


class EachParty(SQLModel):
    PDP: int = 0
    DPP: int = 0
    ACN: int = 0
    PPA: int = 0
    CDC: int = 0
    JP: int = 0
    ANPP: int = 0
    LABO: int = 0
    CPP: int = 0


class LGA(Enum):
    """
    Local Government Areas (LGAs) in Delta State, Nigeria.
    """

    ughelli_north = "Ughelli North"
    warri_south = "Warri South"
    ukwuani = "Ukwuani"
    uvwie = "Uvwie"
    ika_north_east = "Ika North - East"
    warri_south_west = "Warri South - West"
    ethiope_west = "Ethipe West"
    aniocha_north = "Aniocha North"
    isoko_north = "Isoko North"
    oshimili_south = "Oshimili South"
    sapele = "Sapele"
    aniocha_south = "Aniocha South"
    isoko_south = "Isoko South"
    bomadi = "Bomadi"
    okpe = "Okpe"
    ndokwa_east = "Ndokwa East"
    burutu = "Burutu"


class SelectForm(BaseModel):
    select_single: LGA = Field(title='Select a Single LGA')


class BigModel(BaseModel):
    Name: str = Field(description="Enter the name of the polling unit.")
    PDP: int = Field(0, description="Enter the result for PDP")
    DPP: int = Field(0, description="Enter the result for DPP")
    ACN: int = Field(0, description="Enter the result for ACN")
    PPA: int = Field(0, description="Enter the result for PPA")
    CDC: int = Field(0, description="Enter the result for CDC")
    JP: int = Field(0, description="Enter the result of JP")
    ANPP: int = Field(0, description="Enter the result for ANPP")
    LABO: int = Field(0, description="Enter the result for LABO")
    CPP: int = Field(0, description="Enter the result for CPP")


class EachPartyResultInEachPolingUnit(SQLModel):
    party: str
    result: int
