from typing import List

from fastapi import APIRouter

from files.apps.department.endpoints.lead_endpoints import lead_endpoints
from files.apps.department.endpoints.lead_person_in_charge_endpoints import (
    lead_person_in_charge_endpoints,
)
from files.apps.department.schemas.lead_schemas import (
    CreateLeadResponseSchema,
    LeadSchema,
)

lead_router = APIRouter(
    prefix="/lead",
    tags=["lead"],
)


lead_person_in_charge_router = APIRouter(
    prefix="/lead-person-in-charge",
    tags=["lead"],
)

lead_router.add_api_route(
    path="/leads",
    methods=["GET"],
    endpoint=lead_endpoints.get_leads,
    # response_model=LeadsListAndPaginationData,
    summary="Get leads",
    description="Get list of leads' previews, containing funnel_step_uuid, creation date \
    and time, name of the lead's company, current lead's funnel's step and \
    lead's person in charge. Also returns pagination data (has_next, has_prev, pages_count.",
)
lead_router.add_api_route(
    path="/get-lead/{lead_id}",
    methods=["GET"],
    endpoint=lead_endpoints.get_lead,
    response_model=LeadSchema,
    summary="Get all lead data",
    description="Get lead's data, user' container and related \
    user, custom field' container and related custom fields, \
    records' container and related records, related deals",
)
lead_router.add_api_route(
    path="/create-lead",
    methods=["POST"],
    endpoint=lead_endpoints.create_lead,
    response_model=CreateLeadResponseSchema,
    summary="Create lead and lead's contact",
    description="Creaates lead, user' container \
    and lead's first contact, that must be created for \
    every created lead, because lead without \
    user must not exist ",
)
lead_router.add_api_route(
    path="/update-lead-data/{lead_id}",
    methods=["PATCH"],
    endpoint=lead_endpoints.update_lead_data,
    response_model=IdentifierResponseSchema,
    summary="Update lead's data",
    description="Updates lead's data tha is belongs \
    exactly to the lead, all related entities are \
    updated separately",
)
lead_router.add_api_route(
    path="/delete-lead/{lead_id}",
    methods=["DELETE"],
    endpoint=lead_endpoints.delete_lead,
    response_model=IdentifierResponseSchema,
    summary="Delete lead",
    description="Deletes lead and all lead's related entities, \
    except users and funnels",
)

lead_person_in_charge_router.add_api_route(
    path="/update-lead-persons-in-charge-list/{lead_id}",
    methods=["PATCH"],
    endpoint=lead_person_in_charge_endpoints.update_lead_persons_in_charge_list,
    response_model=list[str],
)
