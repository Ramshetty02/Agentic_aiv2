# Deployment

## Local

```bash
make setup
make run
```

The app starts on Streamlit's default port, `8501`.

## Docker

```bash
make docker-build
docker run --rm -p 8501:8501 --env-file .env erevna:local
```

The container exposes Streamlit's health endpoint at:

```text
http://localhost:8501/_stcore/health
```

## Streamlit Community Cloud

1. Connect `ramshetty01/EREVNA`.
2. Set the main file path to `app.py`.
3. Add `OPENAI_API_KEY` only if OpenAI mode is needed.
4. Leave API keys blank to run demo mode.

No public hosted demo is currently published. Add the URL to README after deployment.

