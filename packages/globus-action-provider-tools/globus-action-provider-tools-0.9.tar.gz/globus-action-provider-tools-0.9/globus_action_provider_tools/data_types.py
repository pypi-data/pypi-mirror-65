from enum import Enum, auto
from json import JSONEncoder
from typing import Any, Dict, List, NamedTuple, Optional, Union

from .authentication import AuthState


class ProviderType(Enum):
    Action = auto()
    Event = auto()


class EventType(Enum):
    STARTED = auto()
    STATUS_UPDATE = auto()
    LOG_UPDATE = auto()
    COMPLETED = auto()
    FAILED = auto()


class ActionProviderDescription(NamedTuple):
    globus_auth_scope: str
    title: str
    admin_contact: str
    synchronous: bool
    input_schema: Union[str, Dict[str, Any]]
    types: List[ProviderType] = [ProviderType.Action]
    api_version: str = "1.0"
    subtitle: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    visible_to: List[str] = ["public"]
    maximum_deadline: str = "P30D"  # Default value of 30 days
    log_supported: Optional[bool] = False
    runnable_by: List[str] = ["all_authenticated_users"]
    administered_by: Optional[List[str]] = None
    event_types: Optional[List[EventType]] = None


class ActionRequest(NamedTuple):
    request_id: str
    body: Dict[str, Any]
    label: Optional[str] = None
    monitor_by: Optional[List[str]] = None
    manage_by: Optional[List[str]] = None
    allowed_clients: Optional[List[str]] = None
    deadline: Optional[str] = None
    release_after: Optional[str] = None


class ActionStatusValue(Enum):
    SUCCEEDED = auto()
    FAILED = auto()
    ACTIVE = auto()
    INACTIVE = auto()


class ActionStatus(NamedTuple):
    action_id: str
    status: ActionStatusValue
    creator_id: str
    label: Optional[str] = None
    monitor_by: Optional[List[str]] = None
    manage_by: Optional[List[str]] = None
    start_time: Optional[str] = None
    completion_time: Optional[str] = None
    release_after: Optional[str] = None
    display_status: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class ActionProviderJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.name
        return super(ActionProviderJsonEncoder, self).default(obj)
