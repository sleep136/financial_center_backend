import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,  # 根据 CPU 核心数调整
        reload=False
    )