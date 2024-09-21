import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend:app", host="0.0.0.0", port=9999, reload=True, log_config="backend/uvicorn_loggin_config.json")
