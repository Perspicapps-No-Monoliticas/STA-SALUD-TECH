from typing import Dict

from fastapi import HTTPException, Response, status
from pydantic import ValidationError

from modules.data_source.application.mappers import MapperDataSourceDTOJson
from modules.data_source.application.commands.create_data_source import (
    CreateDataSource as CreateDataSourceCommand,
)
from modules.data_source.infraestrucuture.dispatcher import DataSourceDispatcher
from seedwork.presentation.api import create_router

data_source_router = create_router("/data-sources")


@data_source_router.get("")
def list_sources():
    return []


@data_source_router.post("")
def create_data_source(data_source: Dict, response: Response):

    map_data_source = MapperDataSourceDTOJson()
    try:
        data_source_dto = map_data_source.external_to_dto(data_source)
        command = CreateDataSourceCommand.from_dto(data_source_dto)
        dispatcher = DataSourceDispatcher()
        dispatcher.publish_command(command)
        response.status_code = status.HTTP_202_ACCEPTED
        return map_data_source.dto_to_external(data_source_dto)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors()
        )
