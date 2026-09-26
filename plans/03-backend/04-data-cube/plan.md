# Data Cube Plan

## Overview
To ensure sliders and interactivity on the frontend are instant (zero server latency), the backend computes a multi-dimensional "Data Cube" during the simulation and serves it to the frontend in a compressed format.

**Subagents Required**:
- `backend-implementer`
- `data-pipeline-engineer`

## Structure
The data cube contains base values and delta multipliers. When the user moves a slider (e.g., tweaking stringency from 1.0 to 1.5), the frontend applies the scalar to the precomputed sensitivity matrix.

### Format
Due to the large size of tabular map/demographic data, JSON may be too bulky.
- **Delivery format:** Parquet or JSON (if small enough).
- **Storage:** Saved as artifacts in MinIO (S3) bucket. DB stores the URL pointer.

## MinIO Storage
```python
# pseudo-code
def save_cube_to_s3(run_id: str, cube_dict: dict) -> str:
    s3_client = boto3.client('s3')
    object_name = f"runs/{run_id}/cube.json"
    s3_client.put_object(
        Bucket='legisim-data',
        Key=object_name,
        Body=json.dumps(cube_dict).encode('utf-8')
    )
    return object_name
```

## Frontend-Backend Contract
The API will return the cube link:
```json
{
  "run_id": "...",
  "status": "completed",
  "artifacts": {
    "data_cube_url": "https://s3.legisim.internal/runs/.../cube.json",
    "map_tiles_url": "..."
  }
}
```
The frontend downloads the JSON/Parquet once and performs in-memory filtering using Crossfilter or plain JS arrays.
