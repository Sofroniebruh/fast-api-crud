# Central schema management to handle cross-references
# Import order: dependencies first, then dependent schemas
from src.tickets.schemas import TicketResponseSchema
from src.users.schemas import UserResponseSchema, UserCreateSchema, UserBaseSchema

# Rebuild models after all imports to resolve forward references
# This must happen after TicketResponseSchema is imported
UserResponseSchema.model_rebuild()

__all__ = [
    'UserResponseSchema',
    'UserCreateSchema',
    'UserBaseSchema',
    'TicketResponseSchema'
]
