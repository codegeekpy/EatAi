def handle_upload_error(error):
    """Convert technical errors to user-friendly messages"""
    error_str = str(error)
    
    messages = {
        "Expecting value: line 1": "Server communication error",
        "Bucket not found": "Image storage not configured",
        "403": "Permission denied - please login again",
        "413": "Image too large (max 5MB)",
        "timed out": "Connection timeout - try again"
    }
    
    for key, message in messages.items():
        if key in error_str:
            return message
    
    return "An error occurred during upload"