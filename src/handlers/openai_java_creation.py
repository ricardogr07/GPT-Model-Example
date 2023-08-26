import re
from handlers.openai_handler import OpenAIApiHandler as AIHandler


class JavaCodeCreation(AIHandler):
    def __init__(self):
        super().__init__()

    def extract_prompts_and_answers(self,text: str) ->list:
        # This pattern is for matching 'Prompt X:' and everything after it until 'Answer X:' appears.
        prompt_pattern = re.compile(r'Prompt \d+:(.*?)(?=Answer \d+:|$)', re.DOTALL)
        # This pattern is for matching 'Answer X:' and everything after it until 'Prompt X:' appears.
        answer_pattern = re.compile(r'Answer \d+:(.*?)(?=Prompt \d+|$)', re.DOTALL)
        
        # Find all matches for the patterns in the input text
        prompts = prompt_pattern.findall(text)
        answers = answer_pattern.findall(text)
        
        # This will strip the leading and trailing whitespace from each string in the lists
        prompts = [p.strip() for p in prompts]
        answers = [a.strip() for a in answers]
        
        # Zip the prompts and answers together into pairs
        paired_prompts_and_answers = list(zip(prompts, answers))
        
        return paired_prompts_and_answers
    def request_new_example(self) -> str:
        messages = [
            {
                "role": "system",
                "content": "I want to train a chatbot to perform tasks and create code in Java. From now, each time I give you as input \"New example\" create a conversation between the user and the bot. Use a random example topic.\nThen continue asking for code changes until you get 5 prompts with 5 answers.\n"
            },
            {
                "role": "user",
                "content": "New Example"
            },
            {
                "role": "assistant",
                "content": "Prompt 1:\nI have a log file named \"server.log\" that contains timestamped log entries. Each entry is a new line with the format \"YYYY-MM-DD HH:MM:SS - Log Message\". I need a Java program to read this file and store each log entry as an object in a list. How can I start with this?\nAnswer 1:\n```java\nimport java.io.BufferedReader;\nimport java.io.FileReader;\nimport java.io.IOException;\nimport java.text.ParseException;\nimport java.text.SimpleDateFormat;\nimport java.util.ArrayList;\nimport java.util.Date;\nimport java.util.List;\n\npublic class LogReader {\n    public static void main(String[] args) {\n        List<LogEntry> logEntries = new ArrayList<>();\n        SimpleDateFormat format = new SimpleDateFormat(\"yyyy-MM-dd HH:mm:ss\");\n\n        try (BufferedReader reader = new BufferedReader(new FileReader(\"server.log\"))) {\n            String line;\n            while ((line = reader.readLine()) != null) {\n                String[] parts = line.split(\" - \", 2);\n                if (parts.length >= 2) {\n                    Date timestamp = format.parse(parts[0]);\n                    String message = parts[1];\n                    logEntries.add(new LogEntry(timestamp, message));\n                } else {\n                    System.err.println(\"Invalid log format: \" + line);\n                }\n            }\n        } catch (IOException | ParseException e) {\n            e.printStackTrace();\n        }\n\n        // Process the logEntries list as needed\n    }\n}\n\nclass LogEntry {\n    private Date timestamp;\n    private String message;\n\n    public LogEntry(Date timestamp, String message) {\n        this.timestamp = timestamp;\n        this.message = message;\n    }\n\n    // Getters and setters as needed\n}\n```\nPrompt 2:\nI want to filter the list to include only the log entries that contain the word \"ERROR\" in their messages.\nAnswer 2:\n```java\nimport java.io.BufferedReader;\nimport java.io.FileReader;\nimport java.io.IOException;\nimport java.text.ParseException;\nimport java.text.SimpleDateFormat;\nimport java.util.ArrayList;\nimport java.util.Date;\nimport java.util.List;\nimport java.util.logging.Level;\nimport java.util.logging.Logger;\n\npublic class LogReader {\n\n    private static final Logger LOGGER = Logger.getLogger(LogReader.class.getName());\n    private static final SimpleDateFormat DATE_FORMAT = new SimpleDateFormat(\"yyyy-MM-dd HH:mm:ss\");\n    \n    public static void main(String[] args) {\n        List<LogEntry> logEntries = readLogEntries(\"server.log\");\n        \n        // Process the logEntries list as needed\n    }\n\n    public static List<LogEntry> readLogEntries(String filePath) {\n        List<LogEntry> logEntries = new ArrayList<>();\n        \n        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {\n            String line;\n            while ((line = reader.readLine()) != null) {\n                LogEntry entry = parseLogEntry(line);\n                if (entry != null) {\n                    logEntries.add(entry);\n                }\n            }\n        } catch (IOException e) {\n            LOGGER.log(Level.SEVERE, \"Failed to read log file\", e);\n        }\n        \n        return logEntries;\n    }\n\n    private static LogEntry parseLogEntry(String line) {\n        try {\n            String[] parts = line.split(\" - \", 2);\n            if (parts.length >= 2) {\n                Date timestamp = DATE_FORMAT.parse(parts[0]);\n                String message = parts[1];\n                if (message.contains(\"ERROR\")) {\n                    return new LogEntry(timestamp, message);\n                }\n            } else {\n                LOGGER.log(Level.WARNING, \"Invalid log format: {0}\", line);\n            }\n        } catch (ParseException e) {\n            LOGGER.log(Level.WARNING, \"Failed to parse log entry date\", e);\n        }\n        \n        return null;\n    }\n}\n\nclass LogEntry {\n    private final Date timestamp;\n    private final String message;\n\n    public LogEntry(Date timestamp, String message) {\n        this.timestamp = new Date(timestamp.getTime());\n        this.message = message;\n    }\n\n    // Getters and immutable setters\n}\n```\nPrompt 3:\nI want to sort the filtered list of log entries in ascending order based on their timestamps. \nAnswer 3:\n```java\nimport java.io.BufferedReader;\nimport java.io.FileReader;\nimport java.io.IOException;\nimport java.text.ParseException;\nimport java.text.SimpleDateFormat;\nimport java.util.ArrayList;\nimport java.util.Date;\nimport java.util.List;\nimport java.util.logging.Level;\nimport java.util.logging.Logger;\n\npublic class LogReader {\n\n    private static final Logger LOGGER = Logger.getLogger(LogReader.class.getName());\n    private static final SimpleDateFormat DATE_FORMAT = new SimpleDateFormat(\"yyyy-MM-dd HH:mm:ss\");\n    \n    public static void main(String[] args) {\n        List<LogEntry> logEntries = readLogEntries(\"server.log\");\n        logEntries.sort((a, b) -> a.getTimestamp().compareTo(b.getTimestamp()));\n        \n        // Process the logEntries list as needed\n    }\n\n    public static List<LogEntry> readLogEntries(String filePath) {\n        List<LogEntry> logEntries = new ArrayList<>();\n        \n        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {\n            String line;\n            while ((line = reader.readLine()) != null) {\n                LogEntry entry = parseLogEntry(line);\n                if (entry != null) {\n                    logEntries.add(entry);\n                }\n            }\n        } catch (IOException e) {\n            LOGGER.log(Level.SEVERE, \"Failed to read log file\", e);\n        }\n        \n        return logEntries;\n    }\n\n    private static LogEntry parseLogEntry(String line) {\n        try {\n            String[] parts = line.split(\" - \", 2);\n            if (parts.length >= 2) {\n                Date timestamp = DATE_FORMAT.parse(parts[0]);\n                String message = parts[1];\n                if (message.contains(\"ERROR\")) {\n                    return new LogEntry(timestamp, message);\n                }\n            } else {\n                LOGGER.log(Level.WARNING, \"Invalid log format: {0}\", line);\n            }\n        } catch (ParseException e) {\n            LOGGER.log(Level.WARNING, \"Failed to parse log entry date\", e);\n        }\n        \n        return null;\n    }\n}\n\nclass LogEntry implements Comparable<LogEntry> {\n    private final Date timestamp;\n    private final String message;\n\n    public LogEntry(Date timestamp, String message) {\n        this.timestamp = new Date(timestamp.getTime());\n        this.message = message;\n    }\n\n    public Date getTimestamp() {\n        return timestamp;\n    }\n\n    public String getMessage() {\n        return message;\n    }\n\n    @Override\n    public int compareTo(LogEntry o) {\n        return timestamp.compareTo(o.timestamp);\n    }\n}\n```"
            },
            {
                "role": "user",
                "content": "New example"
            }
        ]
        return super().generate_chat_completion(messages, 0.25)