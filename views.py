from flask import Flask, render_template, request
import pandas as pd
import psycopg2

from Models import GetComments, CommentChecker
from UserInfo import user, host, dbname

app = Flask(__name__)

# psql connection
con = None
con = psycopg2.connect(database = dbname, user=user,host=host)



# recipe index
recipe_table = []
query = """
          SELECT title, url, rank_compound FROM recipes;
          """
query_results = pd.read_sql_query(query,con)
for i in range(0,query_results.shape[0]):
    recipe_table.append(dict(recipe_title=query_results.iloc[i]['title'].decode('utf-8'), url=query_results.iloc[i]['url'].decode('utf-8')))
recipe_table = sorted(recipe_table)

recipe_titles = []
for i in range(0,query_results.shape[0]):
    recipe_titles += [query_results.iloc[i]['title'].decode('utf-8')]
recipe_titles = sorted(recipe_titles)


@app.route('/')
@app.route('/index')
def main():
  return render_template('main.html', autocomplete_list=recipe_titles)


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
    comments, url, rank, total_helpful, fraction_helpful, total_comments = GetComments(user_input,con)
    happiness_graph = "../static/img/images/" + user_input + ".png"
    return render_template('recipe_data.html', commentslist=comments, title=user_input, url=url, image=happiness_graph, rank=rank,
      totalhelpful=total_helpful, fractionhelpful=fraction_helpful, numberofcomments=total_comments, numberofrecipes=len(recipe_titles))

  else:
    return render_template('recipe_index.html', recipes=recipe_table)


@app.route('/check', methods=['GET', 'POST'])
def check_comment():
  user_input = request.args.get('comment_check')
  prediction, response = CommentChecker(user_input, con)
  return render_template('comment_checker.html', prediction=prediction, response=response, checkedcomment=user_input)




