from flask import Flask, render_template, request

app = Flask(__name__)

import pandas as pd
from Models import GetComments, CommentChecker


#sentence_data = pd.read_csv("./static/data/comments_sentences.csv")
recipe_data = pd.read_csv("./static/data/recipes_with_sentiment.csv")


# recipe index - pandas/csv
recipe_table = []
for i in range(0,recipe_data.shape[0]):
    recipe_table.append(dict(recipe_title=recipe_data.iloc[i]['title'].decode('utf-8'), url=recipe_data.iloc[i]['url'].decode('utf-8')))
recipe_table = sorted(recipe_table)

recipe_titles = []
for i in range(0,recipe_data.shape[0]):
    recipe_titles += [recipe_data.iloc[i]['title'].decode('utf-8')]
recipe_titles = sorted(recipe_titles)




@app.route('/')
def check():
    return render_template('about.html')
    #return "<h1 style='color:blue'>Hello There!</h1>"

@app.route('/index')
def main():
  return render_template('main.html', autocomplete_list=recipe_titles)
 # return render_template('main.html', autocomplete_list=['a','b','c','d','e','f'])

# list all the recipes currently in the database
@app.route('/recipe_index')
def recipe_index():
  return render_template('recipe_index.html', recipes=recipe_table)


@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/contact')
def contact_details():
  return render_template('contact.html')


@app.route('/search', methods=['GET', 'POST'])
def find_comments():
  user_input = request.args.get('recipe_choice')

  if user_input == '':
    return render_template('recipe_index.html', recipes=recipe_table)

  elif user_input != '':
    comments, url, rank, total_helpful, fraction_helpful, total_comments = GetComments(user_input, sentence_data, recipe_data)
    happiness_graph = "../static/img/images/" + user_input + ".png"
    return render_template('recipe_data.html', commentslist=comments, title=user_input, url=url, image=happiness_graph, rank=rank,
      totalhelpful=total_helpful, fractionhelpful=fraction_helpful, numberofcomments=total_comments, numberofrecipes=len(recipe_titles))

  else:
    return render_template('recipe_index.html', recipes=recipe_table)


@app.route('/check', methods=['GET', 'POST'])
def check_comment():
  user_input = request.args.get('comment_check')
  prediction, response = CommentChecker(user_input)
  return render_template('comment_checker.html', prediction=prediction, response=response, checkedcomment=user_input)


