import re

# Email detection
email_pattern = re.compile(
    r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
)

def validate_input(question: str):
    
    if not question or not question.strip():
        raise ValueError("The input question is empty or None.")
    
    if len(question) > 500:
        return False, "The input question exceeds the maximum length of 500 characters."
    
    blocked_patterns = [
        # Prompt Injection Markers
        "ignore previous instructions",
        "ignore all instructions",
        "reveal your system prompt",
        "show me your system prompt",
        
        # Malicious Operations
        "delete data",
        "delete files",
        "execute shell command",
        "run terminal command",
        "access local files",
        "access system files",
        
        # SQL Injection Patterns
        r"\bdrop\s+(the\s+)?column\b",
        r"\bdelete\s+(the\s+)?column\b",
        r"\bremove\s+(the\s+)?column\b",
        r"\brename\s+(the\s+)?column\b",
        r"\bmodify\s+(the\s+)?column\b",
        r"\bupdate\s+(the\s+)?data\b",
        r"\bdelete\s+(the\s+)?data\b",
        r"\btruncate\b",
    ]
    
    question_lower = question.lower()
    
    for pattern in blocked_patterns:
        if re.search(pattern, question_lower):
            raise ValueError(
                "Unsafe operation detected in the input question. "
                "This operation is not allowed for security reasons. "
                "This application is designed to analyze data and generate insights, not to perform destructive operations on the data."
            )
        elif email_pattern.search(question):
            raise ValueError(
                "Email addresses are not allowed in the input question. "
                "Please remove any email addresses and try again."
            )

    return True