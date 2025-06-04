from api import chat_complete

def judge_safety(code, model_name="gemini-2.5-flash"):
    """Use AI to judge the safety of the proposed code"""
    messages = [
        {
            "role": "system",
            "content": """You are a code safety reviewer. Analyze the provided Python code for potential safety issues.

Look for:
1. System-level operations that could be harmful (file deletion, network access, subprocess calls to dangerous commands)
2. Infinite loops or resource exhaustion
3. Code that tries to access sensitive files or environment variables
4. Attempts to install packages or modify the system
5. Any malicious or potentially harmful patterns

Please provide:
1. A safety verdict: SAFE, UNSAFE, or CAUTION
2. Detailed analysis of your reasoning if there is any concern. Otherwise, just say it's good. 
3. Specific concerns if any
4. Suggestions for safer alternatives if applicable

Format your response as:
VERDICT: [SAFE/UNSAFE/CAUTION]

ANALYSIS:
[Your detailed analysis here]

CONCERNS:
[List specific concerns if any, or "None" if safe]

SUGGESTIONS:
[Any suggestions for improvement, or "None" if not applicable]"""
        },
        {
            "role": "user",
            "content": f"""Please analyze this Python code for safety:

```python
{code}
```

Provide your safety assessment following the format specified."""
        }
    ]
    
    try:
        response = chat_complete(
            messages,
            model_name=model_name,
            max_tokens=8192,
            temperature=0.5  # Low temperature for consistent safety judgments
        )
        
        # Extract the safety verdict from the formatted response
        verdict = "SAFE"  # Default
        if "VERDICT: UNSAFE" in response:
            verdict = "UNSAFE"
        elif "VERDICT: CAUTION" in response:
            verdict = "CAUTION"
        elif "VERDICT: SAFE" in response:
            verdict = "SAFE"
        
        return verdict, response
            
    except Exception as e:
        print(f"Error during safety check: {e}")
        return "ERROR", f"Could not perform safety check: {e}" 