import copy
import json
import unittest

from open_webui.utils.oci import normalize_gemini_tool_results


OCI_URL = 'https://inference.generativeai.eu-frankfurt-1.oci.oraclecloud.com/20231130/actions/v1'


class OCIGeminiToolResultTests(unittest.TestCase):
    def payload(self, content):
        return {
            'model': 'google.gemini-2.5-flash',
            'messages': [{'role': 'tool', 'tool_call_id': 'call_1', 'content': content}],
        }

    def test_arrays_and_scalars_keep_all_data_inside_an_object(self):
        for value in [[{'text': 'Grüße'}, {'value': 2}], [], [1, [2]], 0, False, None, 'text']:
            with self.subTest(value=value):
                result = normalize_gemini_tool_results(self.payload(json.dumps(value)), OCI_URL)
                self.assertEqual(json.loads(result['messages'][0]['content']), {'result': value})
                self.assertEqual(result['messages'][0]['tool_call_id'], 'call_1')

    def test_objects_and_plain_text_are_preserved(self):
        for content in ['{"items": [1, 2]}', 'Tool failed: unavailable', '', '[invalid', None]:
            with self.subTest(content=content):
                payload = self.payload(content)
                self.assertIs(normalize_gemini_tool_results(payload, OCI_URL), payload)

    def test_all_tool_turns_are_fixed_without_changing_shared_history(self):
        payload = self.payload('[1]')
        payload['messages'] = [
            {'role': 'user', 'content': '[1]'},
            {'role': 'assistant', 'content': None, 'tool_calls': [{'id': 'call_1'}]},
            payload['messages'][0],
            {'role': 'assistant', 'content': 'Checking again'},
            {'role': 'tool', 'tool_call_id': 'call_2', 'content': '[2]'},
        ]
        original = copy.deepcopy(payload)
        result = normalize_gemini_tool_results(payload, OCI_URL)
        self.assertEqual(payload, original)
        self.assertEqual(result['messages'][:2], original['messages'][:2])
        for index, value in [(2, [1]), (4, [2])]:
            self.assertEqual(json.loads(result['messages'][index]['content']), {'result': value})
        self.assertEqual(normalize_gemini_tool_results(result, OCI_URL), result)

    def test_other_models_providers_and_responses_are_unchanged(self):
        for url, model, is_responses in [
            ('https://api.openai.com/v1', 'google.gemini-2.5-flash', False),
            ('https://inference.generativeai.example.com/v1', 'google.gemini-2.5-flash', False),
            (OCI_URL, 'openai.gpt-6-luna', False),
            (OCI_URL, 'google.gemini-2.5-flash', True),
        ]:
            with self.subTest(url=url, model=model, is_responses=is_responses):
                payload = {**self.payload('[1]'), 'model': model}
                self.assertIs(normalize_gemini_tool_results(payload, url, is_responses=is_responses), payload)

    def test_streaming_and_non_streaming_requests_are_normalized(self):
        for stream in [True, False]:
            payload = {**self.payload('[1, 2]'), 'stream': stream}
            result = normalize_gemini_tool_results(payload, OCI_URL)
            self.assertEqual(json.loads(result['messages'][0]['content']), {'result': [1, 2]})
            self.assertEqual(result['stream'], stream)


if __name__ == '__main__':
    unittest.main()
