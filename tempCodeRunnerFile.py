# pyrefly: ignore [unknown-name]
@app.get(f"{API_PREFIX}/model-info", response_model=ModelInfoResponse, tags=["System"])
async def get_model_info():
   
    # pyrefly: ignore [unknown-name]
    manager = get_model_manager()
    # pyrefly: ignore [unknown-name]
    return ModelInfoResponse(**manager.get_model_info())
