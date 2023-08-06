from ..core.pyi import PYI

# 基础控制器


class PYIService(PYI):

    @staticmethod
    def _extends():
        return PYIService

# def Service(service):
#     def decorator(target):
#         if service._extends and service._extends() == PYIService:
#             return service()
#     return decorator