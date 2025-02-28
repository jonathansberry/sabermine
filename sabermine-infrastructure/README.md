# CDK Infrastructure - Saber Technical Exercise

This is AWS Cloud Development Kit (CDK) app that deploys a lambda function and api gateway service to run the sabermine-backend FastAPI service. 

To get going with this:

1. Install poetry
   ```
   pipx install poetry
   ```

2. Optionally install the poetry plugin "poetry-dotenv-plugin".  This plugin will automatically load a .env file in the root directory when activating poetry's venv.  This allows you to optional persist env var variables such as AWS_PROFILE within the venv for convienience.  An example .env file is included in .env.example.    
   ```
   poetry self add poetry-dotenv-plugin
   ```

3. Sync the poetry package - this will ensure you install the tested dependancy versions instead of the latest dependancy versions which may break things.  
   ```
   poetry sync
   ```

4. Poetry will automatically create a Python venv with installed packages.  You can review the location and details of this venv, activate it, and use it as any other python venv. 
   ```
   poetry env info
   `poetry env activate`
   pip freeze
   ```

