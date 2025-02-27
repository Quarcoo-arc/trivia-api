import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def get_all_categories():
        try:
            categories = Category.query.all()

            categories_obj = dict()

            for category in categories:
                categories_obj[category.id] = category.type

            return jsonify({
                'success': True,
                'categories': categories_obj,
            })
        
        except:
            abort(404)



    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).                
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = Question.query.all()
        questions_list = [question.format() for question in questions]

        if start > len(questions_list):
            abort(404)
        
        else:
            questions_to_send = questions_list[start:end]

            categories = Category.query.all()
            
            categories_obj = dict()

            for category in categories:
                categories_obj[category.id] = category.type
            
            return jsonify({
                'success': True,
                'questions': questions_to_send,
                'total_questions': len(questions_list),
                'categories': categories_obj,
                'current_category': categories_obj[4]
            })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:            
            question = Question.query.get(question_id)
            deleted_question = question.format()

            deleted = Question.query.filter_by(id=question_id).delete()
            db.session.commit()

            if deleted:

                return jsonify({
                        'success': True,
                        'message': f'Question with id {question_id} was deleted successfully',
                        'question': deleted_question,
                    })

        except :
            abort(422)


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=['POST']) 
    def create_question():
        
        payload = request.get_json()

        try:            
            question = Question(**payload)
            db.session.add(question)
            db.session.commit()

            return jsonify({
                'success': True,
                'question': question.format()
            })

        except Exception as e:
            abort(405)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/search", methods=['POST'])
    def search_question():
        
        try:
            search_term = request.get_json()["searchTerm"]
            
            questions = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()

            questions_list = [question.format() for question in questions]

            category_type = Category.query.get(3).type

            return jsonify({
                'success': True,
                'questions': questions_list,
                'total_questions': len(questions_list),
                'current_category': category_type
            })
            
        except Exception as e:
            abort(422)


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route("/categories/<int:category_id>/questions")
    def get_category_questions(category_id):

        try:

            category = Category.query.filter(Category.id==category_id).one_or_none()

            questions = Question.query.filter(Question.category==str(category_id)).all()
            questions_list = [question.format() for question in questions]
            
            return jsonify({
                'success': True,
                'questions': questions_list,
                'total_questions': len(questions_list),
                'current_category': category.type
            })

        except:
            abort(404)    


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def get_quiz_question():
        data = request.get_json()

        try:
            previous_questions = data["previous_questions"]
            quiz_category = data["quiz_category"]

            questions = Question.query.all()
            questions_list = [question.format() for question in questions]

            filtered_list = []

            for question in questions_list:
                if question['id'] not in previous_questions:
                    filtered_list.append(question)

            if quiz_category:
                for index, item in enumerate(filtered_list):
                    if item["category"] != quiz_category["id"]:
                        filtered_list.pop(index)

            selected_question = random.choice(filtered_list) if len(filtered_list) else None
                
            return jsonify({
                'success': True,
                'question': selected_question,
            })
        except:
            abort(422)


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Not found"
            }), 404
    
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "Not allowed"
            }), 405
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False, 
        "error": 422,
        "message": "Unprocessable"
        }), 422
    
    @app.errorhandler(400)
    def invalid_request(error):
        return jsonify({
        "success": False, 
        "error": 400,
        "message": "Invalid request"
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
        "success": False, 
        "error": 500,
        "message": "Internal server error"
        }), 500

    return app

