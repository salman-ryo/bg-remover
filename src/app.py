from transparent_background import Remover
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from PIL import Image
import io, asyncio, torch

app = FastAPI(title="BG-Removal API")

remover = Remover(mode="fast", device="cuda" if torch.cuda.is_available() else "cpu")

@app.post(
    "/remove-bg",
    responses={200: {"content": {"image/png": {}}}},
    response_class=Response
)
async def remove_bg(file: UploadFile = File(...)):
    raw = await file.read()
    img = Image.open(io.BytesIO(raw)).convert("RGB")

    # run inference off the event loop
    rgba = await asyncio.to_thread(remover.process, img)   # note .process()

    buff = io.BytesIO()
    rgba.save(buff, format="PNG")
    return Response(buff.getvalue(), media_type="image/png")


# Test
# http://localhost:8000/remove-bg POST with formdata key = file, value = image