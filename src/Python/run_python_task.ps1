param (
    [string]$taskID,
    [string]$project = 'FANCY_RAT'
)

# Set the working directory to where your Python script is located
Set-Location 'C:\Users\ricar\Documents\GitHub\GPT-Model-Example\src\Python'

# Set the environment variable correctly
$env:PYTHONPATH="C:\Users\ricar\Documents\GitHub\GPT-Model-Example\src"

# Run the Python script
python create_python_task.py "$taskID" "$project"

#Can be called as Run-PythonTask "{taskID}" "{project}"