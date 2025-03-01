from fastapi import APIRouter


def create_router(path: str) -> APIRouter:
    """
    Creates and returns an APIRouter instance with the specified prefix path.
    Args:
        path (str): The prefix path for the APIRouter.
    Returns:
        APIRouter: An instance of APIRouter with the specified prefix path.
    """

    return APIRouter(prefix=path)
