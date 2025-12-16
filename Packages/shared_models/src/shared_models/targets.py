from shared_db import BaseTargetTable

class TargetTable(BaseTargetTable):
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
