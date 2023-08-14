import openai
from openai_handler import OpenAIApiHandler

class SQLCodeCreation(OpenAIApiHandler):
    def __init__(self):
        super().__init__()

    def request_new_example(self):
        """Request code example for sql using OpenAI API."""
        messages = [
            {
                "role":"system",
                "content":"I want to train a chatbot to perform the following tasks:\nApplied MySQL's SQL.\n\nPractical implementation and usage of MySQL in real-world scenarios. This means the use of MySQL commands and queries to solve specific data-related problems in an actual database or application.\n\nYou can describe the database tables to the chatbot or inquire about how to perform a specific task using a scenario generated by the chatbot. This could involve prompts such as retrieving specific data from a database, performing data analysis, creating and modifying database tables, joining data from multiple tables, filtering records based on certain conditions, and more."
            },
            {
                "role":"user",
                "content":"Create a new example with a different topic, use 4 tables now. Make sure to add CTEs and practical implementation and utilization of SQL functions in real-world scenarios, in particular, I want you to use the CUME_DIST Window Function for each query.\nCreate 5 queries based on this and make sure to use the CUME_DIST Window Function for each query."
            },
            {
                "role":"assistant",
                "content":"**Table: books**\n| Column       | Description                 |\n|--------------|-----------------------------|\n| book_id      | Book's ID                   |\n| title        | Book's title                |\n| author_id    | ID of the author            |\n| genre        | Book's genre                |\n| price        | Book's price                |\n\n**Table: authors**\n| Column       | Description                 |\n|--------------|-----------------------------|\n| author_id    | Author's ID                 |\n| author_name  | Author's name               |\n| country      | Author's country            |\n\n**Table: customers**\n| Column       | Description                 |\n|--------------|-----------------------------|\n| customer_id  | Customer's ID               |\n| customer_name | Customer's name            |\n| city         | Customer's city             |\n| state        | Customer's state            |\n\n**Table: book_reviews**\n| Column       | Description                 |\n|--------------|-----------------------------|\n| review_id    | Review's ID                 |\n| book_id      | ID of the book being reviewed |\n| customer_id  | ID of the customer who reviewed |\n| rating       | Rating given by the customer |\n| review_text  | Text of the review          |\n\n\n1. **Query: Calculate the cumulative distribution of customer ratings for books**\n```sql\nWITH BookRatings AS (\n    SELECT b.title, br.rating\n    FROM books b\n    JOIN book_reviews br ON b.book_id = br.book_id\n)\nSELECT title, rating, CUME_DIST() OVER(ORDER BY rating DESC) AS cume_dist\nFROM BookRatings;\n```\n\n2. **Query: Identify books with a cumulative distribution rating below 0.4**\n```sql\nWITH BookRatings AS (\n    SELECT b.title, br.rating\n    FROM books b\n    JOIN book_reviews br ON b.book_id = br.book_id\n)\nSELECT title, rating\nFROM BookRatings\nWHERE CUME_DIST() OVER(ORDER BY rating DESC) < 0.4;\n```\n\n3. **Query: Calculate the CUME_DIST of average ratings for books within each genre**\n```sql\nWITH GenreAvgRatings AS (\n    SELECT b.genre, AVG(br.rating) AS avg_rating\n    FROM books b\n    JOIN book_reviews br ON b.book_id = br.book_id\n    GROUP BY b.genre\n)\nSELECT genre, avg_rating, CUME_DIST() OVER(ORDER BY avg_rating DESC) AS cume_dist\nFROM GenreAvgRatings;\n```\n\n4. **Query: Find the genres with a CUME_DIST above 0.6 in terms of average ratings**\n```sql\nWITH GenreAvgRatings AS (\n    SELECT b.genre, AVG(br.rating) AS avg_rating\n    FROM books b\n    JOIN book_reviews br ON b.book_id = br.book_id\n    GROUP BY b.genre\n)\nSELECT genre, avg_rating\nFROM GenreAvgRatings\nWHERE CUME_DIST() OVER(ORDER BY avg_rating DESC) > 0.6;\n```\n\n5. **Query: Calculate the CUME_DIST of customer review counts for books**\n```sql\nWITH BookReviewCounts AS (\n    SELECT b.title, COUNT(br.review_id) AS review_count\n    FROM books b\n    LEFT JOIN book_reviews br ON b.book_id = br.book_id\n    GROUP BY b.title\n)\nSELECT title, review_count, CUME_DIST() OVER(ORDER BY review_count DESC) AS cume_dist\nFROM BookReviewCounts;\n```"
            },
            {
                "role":"user",
                "content":"New example"
            }
        ]
        try:
            response = openai.ChatCompletion.create(
                engine="gpt-35-turbo",
                messages=messages,
                temperature=0,
                max_tokens=4000,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )
            print(response['choices'][0]['message']['content'])
        except openai.error.OpenAIError as e:
            print(f"Error during API call: {e}")


if __name__ == "__main__":
    explainer = SQLCodeCreation()
    explainer.request_new_example()