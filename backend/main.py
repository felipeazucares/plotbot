import uvicorn

if __name__ == "__main__":
    uvicorn.run("api.api:app", host="0.0.0.0", port=8450, reload=True)
