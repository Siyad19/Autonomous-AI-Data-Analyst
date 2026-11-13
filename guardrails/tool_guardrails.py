import re

def validate_query(query: str):
    
    if not query or not query.strip():
        raise ValueError("The SQL query is empty or None.")
    
    query = query.strip()
    
    forbidden = [
            "INSERT",
            "UPDATE",
            "DELETE",
            "DROP",
            "ALTER",
            "CREATE",
            "TRUNCATE"
        ]

    upper_query = query.upper() # Covert the query to uppercase.

        # Raise an ValueError if the following forbidden keywords are found in the LLM generated query.
    for keyword in forbidden:
        if re.search(rf"\b{keyword}\b", upper_query):
            raise ValueError(f"Unsafe SQL operation detected: {keyword}")
        
    return True