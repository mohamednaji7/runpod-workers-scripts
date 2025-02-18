# handler.py
import runpod
from engine_api import OpenaiEngine
from model_api import MockModel
import os
import time

if os.environ.get('SCRIPT_NAME') is not None:
    import logging
    # Configure logging to output plain text to stdout
    logging.basicConfig(
        level=logging.DEBUG,       # Set the minimum logging level
        format='[%(levelname)s] %(message)s'  # Text-only format
    )
    rich_console = logging

else:
    from rich_console import Rich_Console
    rich_console = Rich_Console()





## Initialize the model
model = MockModel()
## Initialize the engine
engine = OpenaiEngine(model)

def get_max_concurrency(default=300):
    """Get maximum concurrency from environment variable."""
    return int(os.getenv('MAX_CONCURRENCY', default))

def async_handler(job):
    """Asynchronous job handler with comprehensive logging."""

    rich_console.info("Job")
    rich_console.info("Job")
    rich_console.info(f"Job >> {str(job)}")
    # Retrieve environment variables
    REPO_URL = os.environ.get('REPO_URL')
    REPO_NAME = os.environ.get('REPO_NAME')
    SCRIPT_DIR = os.environ.get('SCRIPT_DIR')
    SCRIPT_NAME = os.environ.get('SCRIPT_NAME')
    for env_var in [REPO_URL, REPO_NAME, SCRIPT_DIR, SCRIPT_NAME]:
        rich_console.info(env_var)


    job_id = job.get('id')
    rich_console.info(f"Processing job: {job_id}")
    
    # Extract job input + Handle request
    # response = engine.process_job_input(job['input'])
    job_input = job['input']
    if 'openai_input' in  job_input:
        job_input = job_input['openai_input']


    response = engine.process_job_input(job_input)
    
    rich_console.debug("here is the response >>>")
    rich_console.debug(response)
    rich_console.info(f"Job {job_id}: Processed successfully")


    time.sleep(5)
    return response


# Start RunPod serverless function
runpod.serverless.start({
    "handler": async_handler
})

import json
import runpod

def handler(job):
    """Handler function to process jobs."""
    job_input = job['input']
    prompt = job_input.get('prompt', 'Hello, World!')
    # Replace this with your model's inference logic
    response_text = f"Generated response for: {prompt}"
    return json.dumps({"choices": [{"text": response_text}]})

runpod.serverless.start({"handler": handler})


