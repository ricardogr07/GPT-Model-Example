param (
    [string]$taskID,
    [string]$specifications = ''
)

# Set the working directory to where your Python script is located
Set-Location 'C:\Users\ricar\Documents\GitHub\GPT-Model-Example\src\SQL'

# Set the environment variable correctly
$env:PYTHONPATH="C:\Users\ricar\Documents\GitHub\GPT-Model-Example\src"

# Run the Python script
python create_SQL_task.py $taskID $specifications

#Can be called as Run-SQLTask "{taskID}" "{specifications}"
#Can be called as Run-SQLTask "{taskID}" which passes specifications as an empty string