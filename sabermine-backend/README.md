# Backend - Saber Technical Exercise

This is a FastAPI service using Mangum so that it can be deployed to AWS Lambda.

To get going with this:

1. Install poetry
   ```
   pipx install poetry
   ```

2. Install the poetry plugins "poetry-auto-export".  Lambda requires a requirements.txt file and poetry-auto-export plugin will automatically keep that file in sync with your poetry commands. The poetry-dotenv-plugin helps with loading ENV VARs into the poetry venv.
   ```
   poetry self add poetry-auto-export poetry-dotenv-plugin
   ```

3. Sync the poetry package - this will ensure you install the tested dependancy versions instead of the latest dependancy versions which may break things.
   ```
   poetry sync
   ```

4. Poetry will automatically create a Python venv with install packages.  You can review the location and details of this venv, activate it, and use it as any other python venv.
   ```
   poetry env info
   `poetry env activate`
   pip freeze
   ```

5. Run tests inside the poetry venv using
   ```
   pytest
   ```
