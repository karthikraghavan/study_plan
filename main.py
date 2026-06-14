import json
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_PATH = os.path.join(BASE_DIR, 'vk_logs.json')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['GET', 'POST', 'OPTIONS'],
    allow_headers=['*'],
)

@app.get('/load-logs')
async def load_logs():
    if not os.path.exists(LOGS_PATH):
        return JSONResponse([])
    with open(LOGS_PATH, 'r') as f:
        return JSONResponse(content=json.load(f))

@app.post('/save-logs')
async def save_logs(request: Request):
    logs = await request.json()
    with open(LOGS_PATH, 'w') as f:
        json.dump(logs, f, indent=2)
    return JSONResponse({'status': 'saved'})

@app.get('/')
async def index():
    return FileResponse(os.path.join(BASE_DIR, 'index.html'))

app.mount('/static', StaticFiles(directory=BASE_DIR), name='static')

# Vercel completely ignores everything below this line
if __name__ == '__main__':
    import uvicorn  # Moved inside here so Vercel doesn't try to import it
    print('Starting server on http://localhost:8000')
    print('Open: http://localhost:8000/')
    uvicorn.run(app, host='localhost', port=8000)
