from enum import Enum


class AccountStatus(Enum):
    ACTIVE = "active"
    DEACTIVATED = "deactivated"
    SUSPENDED = "suspended"