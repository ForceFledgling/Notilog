import uvicorn


uvicorn.run(
    'server.app:app',
    reload=True,
)