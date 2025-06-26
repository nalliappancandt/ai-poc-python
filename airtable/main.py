from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio

from airtable import chat

app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Item(BaseModel):
    query: str

async def generate_response(query: Item):
    response = await chat.chat_invoke(query)
    print(response)
   # return response
    
    # Extract the output from the response
    if "output" in response:
        yield f"data:{json.dumps({'content': response['output']})}\n\n"
    
    # If there are intermediate steps, stream them as well
    if "intermediate_steps" in response:
        for step in response["intermediate_steps"]:
            if "action" in step and "action_input" in step:
                yield f"data: {json.dumps({'content': f'Action: {step['action']}, Input: {step['action_input']}', 'type': 'thinking'})}\n\n"
            if "observation" in step:
                yield f"data: {json.dumps({'content': f'Observation: {step['observation']}', 'type': 'thinking'})}\n\n"
    
    # Signal the end of the stream
    yield f"data: [DONE]\n\n"

@app.post("/chat")
async def chat_endpoint(query: Item):
    print(query)
    #return generate_response(query)
    return StreamingResponse(
        generate_response(query),
        media_type="text/event-stream"
    )

# List available models endpoint
@app.get("/models")
async def list_models():
    """List available Ollama models."""
    import requests

    try:
        # Get models from Ollama API
        response = requests.get("http://localhost:11434/api/tags")

        if response.status_code == 200:
            models = response.json().get("models", [])
            return {"models": [model["name"] for model in models]}
        else:
            return {"error": f"Failed to fetch models: {response.status_code}"}
    except Exception as e:
        return {"error": f"Error connecting to Ollama: {str(e)}"}


@app.get("/client_example")
async def client_example():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Explore Airtable Profiles using LLM</title>
        <script>
            // Fetch available models when page loads
            window.onload = async function() {
                try {
                    const response = await fetch('/models');
                    const data = await response.json();
                    
                    const modelSelect = document.getElementById('model-select');
                    if (data.models && data.models.length > 0) {
                        data.models.forEach(model => {
                            const option = document.createElement('option');
                            option.value = model;
                            option.textContent = model;
                            if (model === 'llama2') {
                                option.selected = true;
                            }
                            modelSelect.appendChild(option);
                        });
                    } else {
                        const option = document.createElement('option');
                        option.value = 'llama2';
                        option.textContent = 'llama2 (default)';
                        modelSelect.appendChild(option);
                    }
                } catch (e) {
                    console.error('Error fetching models:', e);
                    const modelSelect = document.getElementById('model-select');
                    const option = document.createElement('option');
                    option.value = 'llama2';
                    option.textContent = 'llama2 (default)';
                    modelSelect.appendChild(option);
                }
            };
            
            async function testStream() {
                const query = document.getElementById('query').value;
                const modelName = document.getElementById('model-select').value;
                const resultDiv = document.getElementById('result');
                const statusDiv = document.getElementById('status');
                
                resultDiv.innerHTML = '';
                statusDiv.textContent = 'Processing...';
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            query: query,
                            streaming: true,
                            model: modelName,
                            history: []
                        })
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    
                    const reader = response.body.getReader();
                    const decoder = new TextDecoder();
                    
                    statusDiv.textContent = 'response...';
                    
                    while (true) {
                        const {value, done} = await reader.read();
                        if (done) break;
                        
                        const text = decoder.decode(value);
                        const lines = text.split('\\n').filter(line => line.trim());
                        
                        for (const line of lines) {
                            try {
                                const event = JSON.parse(line.replace(/^data:/, ''));
                                
                                if (event.type === 'token') {
                                    resultDiv.innerHTML += event.content;
                                } else if (event.type === 'agent_action') {
                                    resultDiv.innerHTML += `<div class="action">Using tool: ${event.tool} with input: ${event.tool_input}</div>`;
                                } else if (event.type === 'agent_finish') {
                                    resultDiv.innerHTML += `<div class="finish">${event.output}</div>`;
                                } else if (event.type === 'error') {
                                    resultDiv.innerHTML += `<div class="error">Error: ${event.content}</div>`;
                                    statusDiv.textContent = 'Error occurred';
                                } else if (event.content) {
                                    statusDiv.textContent = `Complete`;
                                    resultDiv.innerHTML += `<div>${event.content}</div>`;
                                }
                            } catch (e) {
                                console.error('Error parsing JSON:', e, line);
                            }
                        }
                    }
                    
                    statusDiv.textContent = 'Complete';
                } catch (e) {
                    console.error('Fetch error:', e);
                    statusDiv.textContent = `Error: ${e.message}`;
                    resultDiv.innerHTML += `<div class="error">Connection error: ${e.message}</div>`;
                }
            }
        </script>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .container { max-width: 800px; margin: 0 auto; }
            .controls { margin-bottom: 20px; }
            .action { color: #2c5282; margin: 10px 0; background: #ebf8ff; padding: 5px; border-radius: 4px; }
            .finish { font-weight: bold; margin-top: 10px; }
            .error { color: #c53030; background: #fff5f5; padding: 5px; border-radius: 4px; }
            #result { white-space: pre-wrap; border: 1px solid #e2e8f0; padding: 15px; min-height: 200px; border-radius: 4px; }
            #status { font-style: italic; color: #718096; margin-bottom: 10px; }
            input, select, button { padding: 8px; margin-right: 10px; }
            button { background: #4299e1; color: white; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background: #3182ce; }
            h1 { color: #2d3748; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Query Airtable Profiles</h1>
            <div class="controls">
                <input type="text" id="query" placeholder="Enter your query" style="width: 300px;">
                <select id="model-select">
                    <!-- Will be populated dynamically -->
                </select>
                <button onclick="testStream()">Submit</button>
            </div>
            <div id="status">Ready</div>
            <div id="result"></div>
        </div>
    </body>
    </html>
    """
    return Response(content=html_content, media_type="text/html")
