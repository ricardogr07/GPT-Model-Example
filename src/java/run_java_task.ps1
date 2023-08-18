param (
    [string]$taskID
)

# Set the working directory to where your Python script is located
Set-Location 'C:\Users\ricar\Documents\GitHub\GPT-Model-Example\src\java'

# Set the environment variable correctly
$env:PYTHONPATH="C:\Users\ricar\Documents\GitHub\GPT-Model-Example\src"

# Run the Python script
python create_java_task.py $taskID

#Can be called as Run-PythonTask "{taskID}"