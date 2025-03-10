import logging
from sqlalchemy import event
from app.core.event_publisher import get_event_publisher
from app.models import User

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class UserEventHandler:
    """
    Handles events related to the User model and delegates to the internal event publisher.
    """
    def __init__(self):
        self.publisher = get_event_publisher()

    def handle_after_insert(self, mapper, connection, target):
        """
        Handle the event after a User is inserted into the database.
        
        Args:
            mapper: The mapper managing the operation.
            connection: The database connection.
            target: The User instance that has been inserted.
        """
        logger.info("DB event triggered | User created: %s", target.id)
        self.publisher.publish_user_created_event(id=str(target.id))

    def handle_after_delete(self, mapper, connection, target):
        """
        Handle the event after a User is deleted from the database.
        
        Args:
            mapper: The mapper managing the operation.
            connection: The database connection.
            target: The User instance that was deleted.
        """
        logger.info("DB event triggered | User deleted: %s", target.id)
        self.publisher.publish_user_deleted_event(id=str(target.id))

def register_event_listeners():
    """
    Registers SQLAlchemy event listeners
    """
    user_events = UserEventHandler()
    event.listen(User, "after_insert", user_events.handle_after_insert)
    event.listen(User, "after_delete", user_events.handle_after_delete)
    logger.info("Registered event listeners.")
