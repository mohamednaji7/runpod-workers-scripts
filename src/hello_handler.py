import runpod
import subprocess
import os
# If your handler runs inference on a model, load the model here.
# You will want models to be loaded into memory before starting serverless.
import logging
# Setup logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.debug("hello RunPod! 'hello_handler.py' script is here.")



def update():
    # Perform git pull to update
    subprocess.run(['git', 'pull'], check=True)
    logging.info("Git pull successful.")

def handler(job):
    """ Handler function that will be used to process jobs. """
    if os.getenv('PULL_BEFORE_REQUEST')=='True':
        logging.info("`handler` is making update.")
        update()

    logging.info("[handler] processing request.")

    job_input = job['input']

    name = job_input.get('name', 'World')
    output = f"Hello, {name}!"
    logging.info("[handler] output: {output}.")
    return 


runpod.serverless.start({"handler": handler})