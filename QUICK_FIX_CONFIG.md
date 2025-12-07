# Quick Fix: Use only OpenAI

If you want to test immediately with only OpenAI (which is working),
update `backend/config.py`:

```python
COUNCIL_MODELS = [
    "gpt-4o",
    "gpt-4o-mini",  # Cheaper alternative
]

CHAIRMAN_MODEL = "gpt-4o"
```

Then commit and push:
```bash
git add backend/config.py
git commit -m "Temporarily use only OpenAI models"
git push
```

Railway will redeploy automatically and the app will work!

---

## After testing, add other providers

Once you've verified OpenAI works, add the other API keys one by one:

1. Add GOOGLE_API_KEY → test
2. Add ANTHROPIC_API_KEY → test
3. Add XAI_API_KEY → test

This way you can isolate which keys work and which don't.
