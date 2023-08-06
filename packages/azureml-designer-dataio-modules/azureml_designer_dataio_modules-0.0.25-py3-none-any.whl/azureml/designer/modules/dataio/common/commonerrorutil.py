ERROR_GROUPS = {
    'ServerBusy': [
        "ServerBusy",
        "The server is busy."
    ],
    'connection issues': [
        "Remote end closed connection without response",
        "Connection refused",
        "Connection timed out",
        "Connection reset by peer",
        "Temporary failure in name resolution",
    ],
    'memory allocation failures': [
        "Unable to allocate ",
        "for an array with shape",
        "and data type object"
    ]}


EXPORT_USER_ERROR_GROUP = [
    "Access to Datastore denied with error response Forbidden",
    "Cannot create file",
    "Cannot create folder/filesystem",
    "The specifed resource name contains invalid characters",
    "Cannot create blob folder",
    "This request is not authorized to perform this operation using this permission",
    "Access to Datastore denied with error response Forbidden"
]


IMPORT_USER_ERROR_GROUP = [
    "Failed to create or update the dataset definition. The dataset definition has been created or update",
    "The provided path is not valid or the files could not be accessed",
    "Object reference not set to an instance of an object",
]


def get_error_group(err_msg):
    for error_group, error_messages in ERROR_GROUPS.items():
        if any(m in err_msg for m in error_messages):
            return error_group
    return None
