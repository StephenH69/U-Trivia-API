import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

# NEED TO ADD PASSWORD WHEN FIRST DOWNLOADED AND REMOVE WHEN UPLOADING

QUESTIONS_PER_PAGE = 10

def paginate_questions(request,selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  formatted_questions = [question.format() for question in selection]
  current_questions = formatted_questions[start:end]
  return current_questions


def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Control-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


  @app.route('/categories', methods=['GET'])
  def get_categories():

    categories = list(map(Category.format, Category.query.all()))

    return jsonify({
      'categories': categories,
      'success':True,
      'Total Categories': len(categories)
    })

  @app.route('/questions', methods=['GET'])
  def get_questions():

    selection = Question.query.all()
    current_questions = paginate_questions(request,selection)

    if len(current_questions) == 0:
      abort(422)

    return jsonify({
      'questions': current_questions,
      'success':True,
      'total questions': len(Question.query.all())
    })

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

    question_delete = Question.query.filter(Question.id == question_id).one_or_none()

    if question_delete is None:
      abort(404)
    else:
      question_delete.delete()

      selection = Question.query.all()
      current_questions = paginate_questions(request,selection)

      return jsonify({
        'questions': current_questions,
        'success':True,
        'total questions': len(Question.query.all())
      })

  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)

    question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
    question.insert()

    selection = Question.query.all()
    current_questions = paginate_questions(request,selection)

    return jsonify({
      'questions': current_questions,
      'success':True,
      'total questions': len(Question.query.all())
    })


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''






  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': "resource not found"
      }), 404

  @app.errorhandler(422)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': "unprocessable entity"
      }), 422

  return app

    