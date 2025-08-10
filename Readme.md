# Background-Removal API

Give any image, get it back with a **transparent background**—powered by the InSPyReNet model and served through FastAPI.

![demo](docs/demo Features
- **State-of-the-art masks** built with MIT-licensed InSPyReNet  
- **Async FastAPI** service—handles concurrent uploads without blocking  
- Returns a ready-to-use **PNG (RGBA)** in a single HTTP call  
- Tiny footprint: fast checkpoint (<15 MB) and optional CUDA GPU acceleration  
- Docker-friendly, zero-config startup

***

## 📂 Project structure
```
.
├── src/
│   └── app.py          # FastAPI endpoint
├── requirements.txt    # Exact Python deps
├── Dockerfile          # Container recipe
└── README.md           # You are here
```

***

## 🚀 Quick start

1.  Clone & install
    ```bash
    git clone https://github.com/youruser/bg-removal-api.git
    cd bg-removal-api
    python -m venv .venv && .\.venv\Scripts\activate
    pip install -r requirements.txt
    ```

2.  Run the server
    ```bash
    uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
    ```

3.  Test in your browser  
    Open `http://localhost:8000/docs`, upload an image to `/remove-bg`, download the transparent result.

***

## 🖼️ Hitting the API

### cURL
```bash
curl -X POST http://localhost:8000/remove-bg ^
     -H "Accept: image/png" ^
     -F "file=@\"C:\path\to\photo.jpg\"" ^
     --output photo_no_bg.png
```

### Python
```python
import requests, pathlib
api = "http://localhost:8000/remove-bg"
img = pathlib.Path("photo.jpg")

with img.open("rb") as f:
    r = requests.post(api,
                      files={"file": (img.name, f, "image/jpeg")},
                      headers={"Accept": "image/png"})
r.raise_for_status()
(img.with_stem(img.stem + "_no_bg")
    .write_bytes(r.content))
```

***

## 🛠️ Configuration

| Env var            | Default | Description                                   |
|--------------------|---------|-----------------------------------------------|
| `BG_MODE`          | `fast`  | `fast`, `base`, or `base-nightly` checkpoint  |
| `BG_DEVICE`        | `auto`  | `cpu`, `cuda`, or `auto` detection            |
| `SERVER_PORT`      | `8000`  | Port exposed by Uvicorn                       |

Set them in a `.env` file or export before launch.

***

## 🐳 Docker

```bash
docker build -t bg-api .
docker run -p 8000:8000 bg-api
```

***

## ⚡ Benchmarks (RTX 3060, 1024 px input)

| Mode | Latency | VRAM |
|------|---------|------|
| `fast` | 120 ms | 1.1 GB |
| `base` | 210 ms | 1.9 GB |

***

## 🧩 Integrating elsewhere

Because the endpoint returns a standard PNG, you can drop it into:

- React/Vue front-ends via `fetch(FormData)`.
- Serverless functions querying the API for on-the-fly thumbnails.
- Batch pipelines—just loop over cURL or the Python snippet.

***

## 🙋 FAQ

**Q. Does it run on CPU-only servers?**  
Yes, set `BG_DEVICE=cpu`. Expect ~1–2 FPS on modern x86 cores.

**Q. Multiple objects in one photo?**  
InSPyReNet keeps all *salient* objects. Post-process the mask if you need a single subject.

**Q. How big can uploads be?**  
Default FastAPI limit is unset; nginx/reverse-proxy may cap at ~2 GB. Tune as needed.

***

## 📜 License

This project: **Apache-2.0**  
Model weights: **MIT** (from original InSPyReNet authors)

***

## 🌟 Star if useful & PRs welcome!