# API Examples

## Start the API

```bash
python api.py
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

## Endpoints

- `POST /analyze` - Synchronous analysis
- `POST /analyze/async` - Asynchronous analysis
- `GET /analyze/{id}` - Get async results
- `GET /health` - Health check

## Examples

### cURL

**Synchronous analysis:**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"input": "https://example.com"}'
```

**Asynchronous analysis:**
```bash
# Start analysis
curl -X POST http://localhost:8000/analyze/async \
  -H "Content-Type: application/json" \
  -d '{"input": "https://example.com"}'

# Get results
curl http://localhost:8000/analyze/{task_id}
```

**HTML analysis:**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"input": "<html><head><title>Test</title></head></html>"}'
```

### Python

```python
import requests

# Synchronous
response = requests.post(
    "http://localhost:8000/analyze",
    json={"input": "https://example.com"}
)
print(response.json())

# Asynchronous
task = requests.post(
    "http://localhost:8000/analyze/async",
    json={"input": "https://example.com"}
).json()

# Poll for results
import time
while True:
    result = requests.get(f"http://localhost:8000/analyze/{task['task_id']}").json()
    if result["status"] == "completed":
        print(result["result"])
        break
    time.sleep(2)
```

### JavaScript

```javascript
// Synchronous
fetch('http://localhost:8000/analyze', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({input: 'https://example.com'})
})
.then(res => res.json())
.then(data => console.log(data));

// Asynchronous
async function analyzeAsync(url) {
  // Start analysis
  const task = await fetch('http://localhost:8000/analyze/async', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({input: url})
  }).then(res => res.json());

  // Poll for results
  while (true) {
    const result = await fetch(`http://localhost:8000/analyze/${task.task_id}`)
      .then(res => res.json());

    if (result.status === 'completed') {
      return result.result;
    }

    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}

analyzeAsync('https://example.com').then(console.log);
```

## Response Format

```json
{
  "status": "success",
  "input_type": "url",
  "result": "# Analysis Results\n\n...",
  "timestamp": "2024-01-01T12:00:00"
}
```

## Interactive Documentation

Visit http://localhost:8000/docs for full interactive API documentation with built-in testing.
