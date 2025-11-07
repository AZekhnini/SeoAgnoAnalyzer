# API Usage Examples

Quick reference guide for using the Website Analyzer REST API.

---

## Getting Started

### 1. Start the API

```bash
python api.py
```

The API will be available at: **http://localhost:8000**

### 2. View Interactive Docs

Open in your browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Quick Examples

### Using cURL

#### Health Check

```bash
curl http://localhost:8000/health
```

#### Analyze a URL (Synchronous)

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"input": "https://nightwatch.io"}'
```

#### Analyze with Natural Language

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"input": "Analyze the website: https://example.com"}'
```

#### Async Analysis (Non-blocking)

```bash
# Start analysis
curl -X POST http://localhost:8000/analyze/async \
  -H "Content-Type: application/json" \
  -d '{"input": "https://nightwatch.io"}'

# Response: {"analysis_id": "abc-123", "status": "pending", ...}

# Check status
curl http://localhost:8000/analyze/abc-123
```

### Using Python Requests

```python
import requests
import json
import time

# Base URL
BASE_URL = "http://localhost:8000"

# Example 1: Synchronous Analysis
response = requests.post(
    f"{BASE_URL}/analyze",
    json={"input": "https://nightwatch.io"}
)

result = response.json()
print(result["result"])

# Example 2: Asynchronous Analysis
# Start analysis
response = requests.post(
    f"{BASE_URL}/analyze/async",
    json={"input": "https://example.com"}
)

analysis_id = response.json()["analysis_id"]
print(f"Analysis ID: {analysis_id}")

# Poll for results
while True:
    status_response = requests.get(f"{BASE_URL}/analyze/{analysis_id}")
    status = status_response.json()

    if status["status"] == "completed":
        print("Analysis complete!")
        print(status["result"])
        break
    elif status["status"] == "error":
        print(f"Error: {status['error']}")
        break
    else:
        print(f"Status: {status['status']}")
        time.sleep(5)  # Wait 5 seconds before checking again
```

### Using JavaScript (fetch)

```javascript
// Example 1: Synchronous Analysis
async function analyzeWebsite(url) {
  const response = await fetch('http://localhost:8000/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ input: url })
  });

  const result = await response.json();
  console.log(result.result);
}

analyzeWebsite('https://nightwatch.io');

// Example 2: Asynchronous Analysis
async function analyzeAsync(url) {
  // Start analysis
  const startResponse = await fetch('http://localhost:8000/analyze/async', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ input: url })
  });

  const { analysis_id } = await startResponse.json();
  console.log(`Analysis started: ${analysis_id}`);

  // Poll for results
  while (true) {
    const statusResponse = await fetch(`http://localhost:8000/analyze/${analysis_id}`);
    const status = await statusResponse.json();

    if (status.status === 'completed') {
      console.log('Analysis complete!');
      console.log(status.result);
      break;
    } else if (status.status === 'error') {
      console.error('Error:', status.error);
      break;
    }

    console.log(`Status: ${status.status}`);
    await new Promise(resolve => setTimeout(resolve, 5000)); // Wait 5 seconds
  }
}

analyzeAsync('https://example.com');
```

---

## Input Types

### 1. URL Analysis (Full)

```json
{
  "input": "https://example.com"
}
```

**Runs**: SEO + Performance + UI/UX analysis

### 2. Natural Language with URL

```json
{
  "input": "Analyze the website: https://nightwatch.io"
}
```

**Runs**: SEO + Performance + UI/UX analysis

### 3. HTML Analysis (SEO Only)

```json
{
  "input": "<html><head><title>Test</title></head><body><h1>Hello</h1></body></html>"
}
```

**Runs**: SEO analysis only

### 4. Screenshot Analysis (UI/UX Only)

Single screenshot:
```json
{
  "input": {
    "screenshot": "path/to/screenshot.png"
  }
}
```

Multiple screenshots:
```json
{
  "input": {
    "screenshots": {
      "desktop": "desktop.png",
      "tablet": "tablet.png",
      "mobile": "mobile.png"
    }
  }
}
```

**Runs**: UI/UX analysis only

---

## Response Structure

### Successful Analysis

```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "result": "# Website Analysis Report\n\n## SEO Analysis\n...",
  "error": null,
  "timestamp": "2025-01-07T10:30:00.000Z"
}
```

### Error Response

```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "error",
  "result": null,
  "error": "Failed to fetch URL: Connection timeout",
  "timestamp": "2025-01-07T10:30:00.000Z"
}
```

### Async Analysis (Pending)

```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "result": null,
  "error": null,
  "timestamp": "2025-01-07T10:30:00.000Z"
}
```

---

## Testing with Postman

### 1. Import Collection

Create a new Postman collection with these requests:

**Health Check**
- Method: GET
- URL: `http://localhost:8000/health`

**Analyze URL**
- Method: POST
- URL: `http://localhost:8000/analyze`
- Body (JSON):
  ```json
  {
    "input": "https://nightwatch.io"
  }
  ```

**Async Analysis**
- Method: POST
- URL: `http://localhost:8000/analyze/async`
- Body (JSON):
  ```json
  {
    "input": "https://example.com"
  }
  ```

**Check Status**
- Method: GET
- URL: `http://localhost:8000/analyze/{{analysis_id}}`

### 2. Environment Variables

Create variables:
- `base_url`: `http://localhost:8000`
- `analysis_id`: (will be set from response)

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid input) |
| 404 | Analysis ID not found |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

---

## Tips

### 1. Use Async for Long-Running Analysis

For URLs (which include UI/UX analysis), use the async endpoint:

```python
# Better for URLs
response = requests.post(f"{BASE_URL}/analyze/async", ...)
```

### 2. Cache Results

Store analysis results to avoid re-analyzing the same URLs:

```python
import hashlib

def get_cache_key(url):
    return hashlib.md5(url.encode()).hexdigest()

# Check cache before analyzing
cache_key = get_cache_key(url)
if cache_key in cache:
    return cache[cache_key]

# Analyze and cache
result = analyze(url)
cache[cache_key] = result
```

### 3. Batch Processing

For multiple URLs, use async endpoint and process in parallel:

```python
import asyncio

urls = ["https://example1.com", "https://example2.com", ...]

async def analyze_batch(urls):
    tasks = [analyze_async(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results
```

---

## Need Help?

- **Interactive Docs**: http://localhost:8000/docs
- **Installation Guide**: See [INSTALLATION.md](INSTALLATION.md)

---

**Happy Analyzing! 🚀**
