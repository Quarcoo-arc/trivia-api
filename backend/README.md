# Backend - Trivia API

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```json
{
  "success": false, 
  "error": 400,
  "message": "Invalid request"
}
```

The API will return three error types when requests fail:

- 400: Invalid Request
- 404: Not Found
- 405: Not Allowed
- 422: Unprocessable
- 500: Internal Server Error

### Endpoints

#### GET /categories

- General:
    - Returns an object of all categories (`{ id: type }`) and a success value
- Sample: `curl http://127.0.0.1:5000/categories`

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```

#### GET /questions

- General:
    - Returns a list of question objects, an object of all categories (`{ id: type }`), current category, success value and total number of questions
    - Results are paginated in groups of 10. Include a request argument (`page`) to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/questions`

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": "History",
    "questions": [
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "total_questions": 19
}
```

#### DELETE /questions/{question_id}

- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value and deleted question (could be used to recreate the question).
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/15`

```json
{
    "message": "Question with id 15 was deleted successfully",
    "question": {
        "answer": "Agra",
        "category": 3,
        "difficulty": 2,
        "id": 15,
        "question": "The Taj Mahal is located in which Indian city?"
    },
    "success": true
}
```

#### POST /questions

- General:
    - Creates a new question object using the submitted question, answer, category and difficulty. Returns the question object and success value.
- Sample: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question":"The Taj Mahal is located in which Indian city?", "answer":"Agra", "difficulty":"2", "category":"3",}'`

```json
{
    "question": {
        "answer": "Agra",
        "category": 3,
        "difficulty": 2,
        "id": 25,
        "question": "The Taj Mahal is located in which Indian city?"
    },
    "success": true
}
```

#### POST /questions/search

- General:
    - Takes in a search term and return questions which have the search term as a substring. Returns the questions containing the search term, the number of matching questions, the current category and the success value.
- Sample: `curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json" -d '{"searchTerm":"title"}'`

```json
{
    "current_category": "Geography",
    "questions": [
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```

#### GET /categories/{category_id}/questions

- General:
    - Returns a list of the question objects in a particular category, the current category, success value and total number of questions in the given category
- Sample: `curl http://127.0.0.1:5000/categories/4/questions`

```json
{
    "current_category": "History",
    "questions": [
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        }
    ],
    "success": true,
    "total_questions": 3
}
```

#### POST /quizzes

- General:
    - Takes `category` and `previous_question` parameters and returns a random question within the given category (if provided) that is not one of the previous questions, and a success value.
- Sample: `curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json" -d '{"previous_questions": [11],"quiz_category": {"id": "1", "type": "Science"}}'`

```json
{
    "question": {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
    },
    "success": true
}
```









