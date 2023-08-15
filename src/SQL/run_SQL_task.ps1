param (
    [string]$taskID,
    [string]$specifications
)

# Set the working directory to where your Python script is located
Set-Location 'C:\Users\ricar\Documents\GitHub\GPT-Model-Example\src\SQL'

# Run the Python script
python create_SQL_task.py $taskID $specifications
