from seedwork.presentation.api import create_router

data_intake_router = create_router("/data-intakes")


@data_intake_router.get("")
def list_intakes():
    return []
