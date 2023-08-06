from typing import List, Optional

from decaf.api.client.repository.commons import Date, DateTime
from decaf.api.client.repository.machinery import BaseResource
from decaf.api.client.types import (
    GUID,
    AccountId,
    AccountMngtFeeSchemeId,
    AnalyticalTypeId,
    Currency,
    InstitutionId,
    PortfolioId,
    RiskProfileId,
    _LaterI,
)


class AccountResource(BaseResource, endpoint="accounts", paged=True):
    id: AccountId
    guid: GUID
    created: DateTime
    creator: Optional[_LaterI]
    updated: DateTime
    updater: Optional[_LaterI]
    name: str
    opened: Optional[Date]
    rccy: Currency
    portfolio: PortfolioId
    custodian: InstitutionId
    atype: Optional[AnalyticalTypeId]
    riskprofile: Optional[RiskProfileId]
    horizontype: Optional[str]
    mandatetype: Optional[str]
    data_source: Optional[str]
    htype: str
    inception: Optional[Date]
    closed: Optional[Date]
    is_active: bool
    is_closed: bool
    mfpercentage: Optional[AccountMngtFeeSchemeId]
    mfpercentages: List[AccountMngtFeeSchemeId]
    riskprofile_name: Optional[str]
    custodian_name: Optional[str]
    portfolio_name: Optional[str]
    team_name: Optional[str]
