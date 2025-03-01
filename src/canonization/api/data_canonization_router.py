from typing import Dict
import uuid

from fastapi import HTTPException, Query, Response, status
from pydantic import ValidationError

from modules.data_canonization.application.queries import (
    GetAllDataCanonizationsQuery,
    GetDataCanonization,
)

from modules.data_canonization.application.mappers import (
    DataCanonizationDTOJsonMapper,
    CreateIntakeDTOJsonMapper,
)

from modules.data_canonization.application.commands import StartDataCanonizationCommand
from seedwork.application.queries import execute_query
from seedwork.presentation.api import create_router
from seedwork.application.commands import dispatch_command

# Ensure dispatch_command is registered for the commands
import modules.data_canonization.infraestrucuture.command_dispatcher  # type: ignore

data_canonization_router = create_router("/data-canonizations")


@data_canonization_router.get("")
def list_canonizations(page: int = Query(None), limit: int = Query(None)):
    query = GetAllDataCanonizationsQuery(page=page, limit=limit)
    query_result = execute_query(query)
    mapper_data_canonization = DataCanonizationDTOJsonMapper()

    return [
        mapper_data_canonization.dto_to_external(data_canonization)
        for data_canonization in query_result.result
    ]


@data_canonization_router.get("/{data_canonization_id}")
def get_data_canonization(data_canonization_id: uuid.UUID):
    query = GetDataCanonization(id=data_canonization_id)
    query_result = execute_query(query)
    if not query_result.result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Data canonization not found"
        )
    mapper_data_canonization = DataCanonizationDTOJsonMapper()
    return mapper_data_canonization.dto_to_external(query_result.result)


@data_canonization_router.post("")
def start_data_canonization(data_canonization: Dict, response: Response):
    map_data_canonization = CreateIntakeDTOJsonMapper()
    try:
        data_canonization_dto = map_data_canonization.external_to_dto(data_canonization)
        command = StartDataCanonizationCommand.from_dto(data_canonization_dto)
        dispatch_command(command)
        response.status_code = status.HTTP_202_ACCEPTED
        return {}
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors()
        )
