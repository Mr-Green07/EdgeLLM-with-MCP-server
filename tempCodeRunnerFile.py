@app.get(f"{API_PREFIX}/model-info", response_model=ModelInfoResponse, tags=["System"])
async def get_model_info():
   
    manager = get_model_manager()
    return ModelInfoResponse(**manager.get_model_info())