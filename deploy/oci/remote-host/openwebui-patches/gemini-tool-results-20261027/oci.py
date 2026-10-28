"""Compatibility helpers for OCI's OpenAI-compatible endpoint."""

import json
from urllib.parse import urlparse


def normalize_gemini_tool_results(payload: dict, url: str, *, is_responses: bool = False) -> dict:
    """Keep JSON tool outputs object-shaped for OCI's Gemini conversion.

    OCI decodes JSON in tool-message strings into Gemini's functionResponse.response,
    which must be an object. Preserve objects and ordinary text; wrap JSON arrays
    and scalars without discarding any data. Inspect all turns for saved chats too.
    """
    hostname = urlparse(url).hostname or ''
    if (
        is_responses
        or not hostname.startswith('inference.generativeai.')
        or not hostname.endswith('.oci.oraclecloud.com')
        or not payload.get('model', '').startswith('google.gemini-')
    ):
        return payload

    messages = []
    changed = False
    for message in payload.get('messages', []):
        content = message.get('content')
        if message.get('role') == 'tool' and isinstance(content, str):
            try:
                result = json.loads(content)
            except ValueError:
                pass
            else:
                if not isinstance(result, dict):
                    message = {**message, 'content': json.dumps({'result': result}, ensure_ascii=False)}
                    changed = True
        messages.append(message)

    return {**payload, 'messages': messages} if changed else payload
