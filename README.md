# Battle-Tested Regex Validations

A curated collection of 25+ reliable, tested regular expressions for common validation tasks such as emails, URLs, and phone numbers. Each entry includes the pattern, a test input, and a note explaining its real-world applicability. Ideal for developers who need dependable validation logic without reinventing the wheel.

**30 rows** · category: `utility` · licence: CC0-1.0 (public domain)

## Usage

```python
import sys
sys.path.insert(0, ".")
from tool import validate_label, get_entries

entries = get_entries()
print(f"Loaded {len(entries)} regex entries")

print(validate_label("email", "user@example.com"))   # True
print(validate_label("email", "not-an-email"))        # False
print(validate_label("ipv4", "192.168.1.1"))          # True
print(validate_label("uuid", "12345678-1234-1234-1234-123456789012"))  # True
print(validate_label("slug", "my-blog-post"))         # True
print(validate_label("hex-color", "#ff5733"))         # True
```

## Sample rows

```json
{"input": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", "label": "email", "note": "Standard email validation covering local, domain, and TLD per RFC 5322 simplified"}
{"input": "^(https?://)?(www\\.)?[-a-zA-Z0-9@:%._\\+~#?&/=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%_\\+.~#?&//=]*)$", "label": "url", "note": "Validates HTTP/HTTPS URLs with optional scheme and www prefix"}
{"input": "^\\+?[1-9]\\d{1,14}$", "label": "phone-e164", "note": "E.164 international phone format: optional plus, 1-15 digits, no leading zero"}
```

## Files

| File | What |
|---|---|
| `data.jsonl` | the dataset, one JSON object per line |
| `tool.py` | stdlib-only loader and helpers |
| `test_tool.py` | tests that pass against the data |

Also on Hugging Face: https://huggingface.co/datasets/SharkSkin/battle-tested-regex-validations

Source: https://github.com/simalidudu-boop/battle-tested-regex-validations

## Support

This is free and public domain. If it saved you time, zap it: `SharkSkin@coinos.io`

---
*Generated and maintained by an autonomous pipeline. Issues and PRs welcome.*
