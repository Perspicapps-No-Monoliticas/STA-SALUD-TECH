from typing import Dict
import uuid

from fastapi import HTTPException, Query, Response, status
from pydantic import ValidationError

from modules.data_source.application.mappers import DataSourceDTOJsonMapper
from modules.data_source.application.commands.create_data_source import (
    CreateDataSource as CreateDataSourceCommand,
)
from modules.data_source.application.queries import (
    GetAllDataSourcesQuery,
    GetDataSource,
)
from seedwork.application.commands import dispatch_command
from seedwork.presentation.api import create_router
from seedwork.application.queries import execute_query

# Ensure dispatch_command are registered for the commands
import modules.data_source.infraestrucuture.command_dispatcher  # type: ignore

data_source_router = create_router("/data-sources")


@data_source_router.get("")
def list_sources(page: int = Query(None), limit: int = Query(None)):
    query = GetAllDataSourcesQuery(page=page, limit=limit)
    query_result = execute_query(query)
    mapper_data_source = DataSourceDTOJsonMapper()

    return [
        mapper_data_source.dto_to_external(data_source)
        for data_source in query_result.result
    ]


@data_source_router.get("/{data_source_id}")
def get_data_source(data_source_id: uuid.UUID):
    query = GetDataSource(id=data_source_id)
    query_result = execute_query(query)
    if not query_result.result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Data source not found"
        )
    mapper_data_source = DataSourceDTOJsonMapper()
    return mapper_data_source.dto_to_external(query_result.result)


@data_source_router.post("")
def create_data_source(data_source: Dict, response: Response):

    map_data_source = DataSourceDTOJsonMapper()
    try:
        data_source_dto = map_data_source.external_to_dto(data_source)
        command = CreateDataSourceCommand.from_dto(data_source_dto)
        dispatch_command(command)
        response.status_code = status.HTTP_202_ACCEPTED
        return {}
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors()
        )
