import requests
from config import Config


def generate_mongo_query(user_input):

    prompt = f"""
You are a STRICT MongoDB filter generator.

Your ONLY task is to convert natural language into a valid MongoDB filter object
for use inside collection.find(<filter>).

You must obey ALL rules below strictly.

========================================
DATABASE INFORMATION
========================================

Database: collegeDB
Collection: results

Each document structure:

{{
"name": string,
"branch": string,
"subject": string,
"grade": "O | E | A | B | C | D"
}}

Each document represents ONE student.

There are NO nested arrays.
There are NO embedded documents.
There is NO field named "results" inside documents.

========================================
STRICT OUTPUT RULES
========================================

1. Output ONLY a valid JSON object.
2. Do NOT include explanations.
3. Do NOT include markdown.
4. Do NOT include backticks.
5. Do NOT include the word "find".
6. Do NOT wrap the JSON inside another object.
7. Do NOT invent new fields.
8. Allowed fields: name, branch, subject, grade.
9. Use correct MongoDB operators when needed.
10. If multiple conditions exist, combine them in one JSON object.
11. NEVER use $elemMatch.
12. NEVER use nested objects unless using valid MongoDB operators.
13. Output must be directly usable inside collection.find().

========================================
BUSINESS LOGIC
========================================

Grade Meaning:

- D = Failed
- O, E, A, B, C = Passed

Natural Language Mapping:

- "failed students" → {{"grade":"D"}}
- "passed students" → {{"grade":{{"$ne":"D"}}}}

Comparison Mapping:

O > E > A > B > C > D

If user says:

- "better than B" → grades O,E,A
- "worse than B" → grades C,D
- "at least A" → grades O,E,A
- "at most C" → grades C,D

Use $in operator.

Example:

"grade better than B"

→ {{"grade":{{"$in":["O","E","A"]}}}}

========================================
VALID EXAMPLES
========================================

User: Show students who failed
Output:
{{"grade":"D"}}

User: Show students who passed
Output:
{{"grade":{{"$ne":"D"}}}}

User: Show CSE students who failed
Output:
{{"branch":"CSE","grade":"D"}}

User: Show students with grade O
Output:
{{"grade":"O"}}

User: Show ECE students with grade better than B
Output:
{{"branch":"ECE","grade":{{"$in":["O","E","A"]}}}}

========================================
FINAL INSTRUCTION
========================================

Now generate ONLY the MongoDB filter JSON
for this user request:

{user_input}
"""

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {Config.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0,
        "top_p": 1
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=data
        )

        if response.status_code != 200:
            return {"error": response.text}

        result = response.json()

        if "choices" not in result:
            return {"error": result}

        return result["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return {"error": str(e)}