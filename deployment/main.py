import os
from pathlib import Path
import subprocess

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

def main():
    # Define the path to the marker file
    marker_file = Path.home() / ".setup_completed"

    if marker_file.exists():
        rich_console.info("Setup already completed. Skipping setup.sh.")
    else:
        rich_console.info("Running setup.sh for the first time...")
        try:
            # Run setup.sh
            rich_console.info("Running `setup.sh`...")

            subprocess.run(['bash', 'setup.sh'], check=True)
            
            # Create the marker file to indicate successful setup
            marker_file.touch()
            rich_console.info("Setup completed successfully.")
        except subprocess.CalledProcessError as e:
            rich_console.error(f"Error during setup: {e}")

    # Change conda environment
    rich_console.info("Activating unsloth_env...")
    # Initialize conda and activate environment, then run handler.py in one subprocess
    try:
        # Chain the commands: initialize conda, activate the environment, and run the script
        command = (
            '/root/miniconda3/bin/conda init bash && '  # Initialize conda
            'source /root/miniconda3/etc/profile.d/conda.sh && '  # Source conda initialization
            'conda activate unsloth_env && '  # Activate the environment
            'python3 handler.py'  # Run the handler.py script
        )
        
        rich_console.info(f"Running commands: {command}")
        
        # Execute the command in one subprocess
        result = subprocess.run(command, shell=True, check=True)
        rich_console.info("Environment activated and handler.py executed successfully")
        
    except subprocess.CalledProcessError as e:
        rich_console.error(f"An error occurred: {e}")
        
        # rich_console.info('Command: os.system("conda activate unsloth_env")')
        # os.system("conda activate unsloth_env") # made ERROR

        # rich_console.info("Command: ['conda', 'activate', 'unsloth_env']")
        # subprocess.run(['conda', 'activate', 'unsloth_env'], check=True) # made ERROR

        # Add conda initialization before activation
        # rich_console.info("Command: ['source', '~/miniconda3/etc/profile.d/conda.sh']")
        # subprocess.run(['source', '~/miniconda3/etc/profile.d/conda.sh'], shell=True, check=True) # made ERROR
    # Initialize conda
    # try:
    #     rich_console.info("['/root/miniconda3/bin/conda', 'init', 'bash']")
    #     subprocess.run(['/root/miniconda3/bin/conda', 'init', 'bash'], check=True)
    #     rich_console.info("Conda initialized successfully")
        
    # except subprocess.CalledProcessError as e:
    #     rich_console.error(f"Failed to initialize conda: {e}")    

    # try:
    #     rich_console.info("Command: ['/root/miniconda3/bin/conda', 'activate', 'unsloth_env']")
    #     subprocess.run(['/root/miniconda3/bin/conda', 'activate', 'unsloth_env'], check=True)
    #     rich_console.info("Env activated successfully")

    # except subprocess.CalledProcessError as e:
    #     rich_console.error(f"Failed to activate conda environment: {e}")


    # # Run handler.py
    # scriptname = 'handler.py'
    # rich_console.info(f"Running `{scriptname}`...")
    # result = subprocess.run(['python3', scriptname], check=True)

    # # Log the output
    # rich_console.info(result)

if __name__ == "__main__":
    main()