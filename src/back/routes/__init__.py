import requests
from fastapi import APIRouter
from urllib.parse import urljoin

from back.models.models import (NodalCalcResponse, VlpIprCalcResponse,
                                WellModelCalcRequest, WellModelCalcResponse)
from back.routes.request_formers import (form_ipr_request,
                                         form_nodal_request,
                                         form_vlp_request)
from back.config import Settings

main_router = APIRouter(prefix="/well_model", tags=["WellModel"])


@main_router.put("/calc", response_model=WellModelCalcResponse)
async def my_profile(data: WellModelCalcRequest):
    return
