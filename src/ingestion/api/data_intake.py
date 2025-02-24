from typing import Dict
import uuid

from fastapi import HTTPException, Query, Response, status
from pydantic import ValidationError

from modules.data_intake.application.queries import (
    GetAllDataIntakesQuery,
    GetDataIntake,
)
from modules.data_intake.application.mappers import (
    DataIntakeDTOJsonMapper,
    CreateIntakeDTOJsonMapper,
)
from modules.data_intake.application.commands import StartDataIntakeCommand
from seedwork.application.queries import execute_query
from seedwork.presentation.api import create_router
from seedwork.application.commands import dispatch_command

# Ensure dispatch_command are registered for the commands
import modules.data_intake.infraestrucuture.command_dispatcher  # type: ignore

data_intake_router = create_router("/data-intakes")


@data_intake_router.get("")
def list_intakes(page: int = Query(None), limit: int = Query(None)):
    query = GetAllDataIntakesQuery(page=page, limit=limit)
    query_result = execute_query(query)
    mapper_data_intake = DataIntakeDTOJsonMapper()

    return [
        mapper_data_intake.dto_to_external(data_source)
        for data_source in query_result.result
    ]


@data_intake_router.get("/{data_intake_id}")
def get_data_intake(data_intake_id: uuid.UUID):
    query = GetDataIntake(id=data_intake_id)
    query_result = execute_query(query)
    if not query_result.result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Data source not found"
        )
    mapper_data_source = DataIntakeDTOJsonMapper()
    return mapper_data_source.dto_to_external(query_result.result)


@data_intake_router.post("")
def start_data_intake(data_intake: Dict, response: Response):
    map_data_intake = CreateIntakeDTOJsonMapper()
    try:
        data_intake_dto = map_data_intake.external_to_dto(data_intake)
        command = StartDataIntakeCommand.from_dto(data_intake_dto)
        dispatch_command(command)
        response.status_code = status.HTTP_202_ACCEPTED
        return {}
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors()
        )
