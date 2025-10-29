log = logging.getLogger(__name__)


class Core:
    """
    Store class for registring core entities.
    """

    def __init__(self):
        self.core_entities = []

    # def get_status_by_core_uuid(self, core_uuid):
    #     for entity in self.core_entities:
    #         if entity.core_id == core_id:
    #             return entity.status
    #     return None

    # def register_core(self, core_uuid):
    #     # send detected gesture to the core

    #     # TODO
