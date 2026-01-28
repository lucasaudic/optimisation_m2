
try:
    print("Start import check")
    import src.model.tsp_model
    print("Import tsp_model ok")
    import src.constructive.nearest_neighbor
    print("Import nearest_neighbor ok")
    import pandas
    print("Import pandas ok")
except Exception as e:
    print(f"Error: {e}")
