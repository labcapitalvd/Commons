from enum import Enum


class TargetTable(Enum):
    LOG_ACTION_TYPES = ("log_action_types", "reference")
    FILE_TYPES = ("file_types", "reference")
    ROLES = ("roles", "reference")
    USER_TIERS = ("user_tiers", "reference")

    USERS = ("users", "auth")
    LOGS = ("logs", "audit")
    REFRESH_SESSIONS = ("refresh_sessions", "auth")
    USER_DETAILS = ("user_details", "auth")
    FILES = ("files", "files")
    USER_PROFILES = ("user_profiles", "auth")
    LINK_USER_FILE = ("user_file_links", "links")

    COMMENT_TYPES = ("comment_types", "reference")
    NOTIFICATION_TYPES = ("notification_types", "reference")
    COMMENTS = ("comments", "interactions")
    NOTIFICATIONS = ("notifications", "interactions")

    def __init__(self, table_name: str, schema: str):
        self.table = table_name
        self.schema = schema

    @property
    def fq_name(self) -> str:
        return f"{self.schema}.{self.table}"
