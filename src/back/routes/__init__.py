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
def my_profile(data: WellModelCalcRequest):
    parsed = data.dict()

    pvt_data = parsed["pvt"]
    ipr_data = {"p_res": parsed["p_res"], "wct": pvt_data["wct"], "pi": parsed["pi"], "pb": pvt_data["pb"]}

    vlp_data = {"inclinometry": parsed["inclinometry"], "casing": parsed["casing"], "tubing": parsed["tubing"],
                "pvt": parsed["pvt"], "p_wh": parsed["p_wh"], "geo_grad": parsed["geo_grad"], "h_res": parsed["h_res"]}

    vlp_api = requests.post(url="http://localhost:3001/vlp/calc", json=vlp_data)
    vlp_result = vlp_api.json()

    ipr_api = requests.post(url="http://localhost:8002/ipr/calc", json=ipr_data)
    ipr_result = ipr_api.json()

    nodal_api = requests.post(url="http://localhost:8003/nodal/calc", json={"vlp": vlp_result, "ipr": ipr_result})
    nodal_result = nodal_api.json()

    return WellModelCalcResponse(
        vlp=vlp_result, ipr=ipr_result, nodal=nodal_result
    )
