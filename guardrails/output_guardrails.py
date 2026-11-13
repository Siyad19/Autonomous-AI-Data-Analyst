import re

# Email detection
email_pattern = re.compile(
    r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
)

# API key / token detection
secret_pattern = [
    
    # Common API key patterns
    re.compile(r"(?i)(?:api[-_]?key|secret|token|access[-_]?key|private[-_]?key)\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]{20,}['\"]?"),
    
    # GitHub personal access tokens
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),

    # Password detection
    re.compile(r"(?i)(?:password|pass|pwd)\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]{8,}['\"]?"),   
]

# Prompt or insttruction leakage patterns
prompt_patterns = [
    "system prompt",
    "system message",
    "hidden prompt",
    "internal instructions",
    "developer instructions",
    "developer message",
    "internal prompt",    
]

def validate_output(response: str):
    
    if not response or not response.strip():
        raise ValueError("The output response is empty or No valid response was generated.")
    
    if len(response) > 1000:
        return False, "The output response exceeds the maximum length of 1000 characters."
    
    if email_pattern.search(response):
        return False, "Sensitive information detected in response! "
    
    for pattern in secret_pattern:
        if pattern.search(response):
            return False, "Sensitive information detected in response! "
        
    response_lower = response.lower()
    for pattern in prompt_patterns:
        if re.search(pattern, response_lower):
            return False, "Internal instructions cannot be disclosed! "
        
    return True, response