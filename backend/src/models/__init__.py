# Central model imports to resolve SQLAlchemy relationships
# Both models must be imported together so relationship() can find referenced classes
# This prevents "expression 'Ticket' failed to locate a name" errors
from src.users.models import User
from src.tickets.models import Ticket

__all__ = ["User", "Ticket"]