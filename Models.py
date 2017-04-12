import pandas as pd
from sklearn.externals import joblib
import random

# import classifier
filename = 'trained_classifiers/commentsclassifier_LR.pkl'
classify_helpful = joblib.load(filename)



min_to_show = 6


# Python/pandas version
def GetComments(user_input, sentence_data, recipe_data, fromUser='Default'):
    # sentence_data = pd.read_csv("./somanycooks/static/comments.csv")

    sentence_query_returns = sentence_data[sentence_data.title == user_input]


    # sentence_query = ("""
    #     SELECT sentence, usercomment, url, username, sentence_tokens  FROM sentences WHERE title='%s';
    #     """ % user_input)

    # sentence_query_returns = pd.read_sql_query(sentence_query,con)

    if len(sentence_query_returns) < 1:
        return {'comment':'sorry, no comments', 'username':'-'}, 'blank', 'blank'

    elif len(sentence_query_returns) > 1:

        url = sentence_query_returns.iloc[0].url.decode('utf-8')

        recipe_query_returns = recipe_data[recipe_data.title == user_input]


        # apply classifier
        predictions = classify_helpful.predict(sentence_query_returns.sentence)
        helpful_sentences = sentence_query_returns.iloc[predictions == 'helpful', :]
        helpful_comments = helpful_sentences.drop_duplicates('usercomment','first')

        total_helpful = len(helpful_comments)
        total_comments = recipe_query_returns.numberofcomments.values[0]
        fraction_helpful = 100*total_helpful / total_comments
        rank = recipe_query_returns.rank_compound.values[0]




        comments_to_show = []
        if (helpful_comments.shape[0] > 0 )& (helpful_comments.shape[0] < min_to_show):
            for ix in range(0, helpful_comments.shape[0]):
                comments_to_show.append(dict(comment=helpful_comments.iloc[ix].usercomment.decode('utf-8'),
                                            username=helpful_comments.iloc[ix].username.decode('utf-8')))
            return comments_to_show, url, rank, total_helpful, fraction_helpful, total_comments


        elif helpful_comments.shape[0] > min_to_show:
            randomnumbers = random.sample(range(0, helpful_comments.shape[0]), min_to_show)
            for _, ix in enumerate(randomnumbers):
                comments_to_show.append(dict(comment=helpful_comments.iloc[ix].usercomment.decode('utf-8'),
                                            username=helpful_comments.iloc[ix].username.decode('utf-8')))
            return comments_to_show, url, rank, total_helpful, fraction_helpful, total_comments

        else:
            return {'comment':'sorry, no comments', 'username':'-'}, 'blank', 'blank'

    else:
        return  {'comment':'sorry, no comments', 'username':'-'}, 'blank', 'blank'


# SQL version
# def GetComments(user_input, con, fromUser='Default'):
#     sentence_query = ("""
#         SELECT sentence, usercomment, url, username, sentence_tokens  FROM sentences WHERE title='%s';
#         """ % user_input)

#     sentence_query_returns = pd.read_sql_query(sentence_query,con)

#     if len(sentence_query_returns) < 1:
#         return {'comment':'sorry, no comments', 'username':'-'}, 'blank', 'blank'

#     elif len(sentence_query_returns) > 1:

#         url=sentence_query_returns.iloc[0].url.decode('utf-8')

#         recipe_query = ("""
#             SELECT numberofcomments, rank_compound FROM recipes WHERE title='%s';
#                        """ % user_input)

#         recipe_query_returns = pd.read_sql_query(recipe_query, con)

#         # if len(recipe_query_returns.sentence_rank) == 0:
#         #     rank = 0
#         # # elif
#         # else:
#         #     rank = int(recipe_query_returns.sentence_rank.mean()*100)



#         # apply classifier
#         predictions = classify_helpful.predict(sentence_query_returns.sentence)
#         helpful_sentences = sentence_query_returns.iloc[predictions == 'helpful', :]
#         helpful_comments = helpful_sentences.drop_duplicates('usercomment','first')

#         total_helpful = len(helpful_comments)
#         total_comments = recipe_query_returns.numberofcomments.values[0]
#         fraction_helpful = 100*total_helpful / total_comments
#         rank = recipe_query_returns.rank_compound.values[0]




#         comments_to_show = []
#         if (helpful_comments.shape[0] > 0 )& (helpful_comments.shape[0] < min_to_show):
#             for ix in range(0, helpful_comments.shape[0]):
#                 comments_to_show.append(dict(comment=helpful_comments.iloc[ix].usercomment.decode('utf-8'),
#                                             username=helpful_comments.iloc[ix].username.decode('utf-8')))
#             return comments_to_show, url, rank, total_helpful, fraction_helpful, total_comments


#         elif helpful_comments.shape[0] > min_to_show:
#             randomnumbers = random.sample(range(0, helpful_comments.shape[0]), min_to_show)
#             for _, ix in enumerate(randomnumbers):
#                 comments_to_show.append(dict(comment=helpful_comments.iloc[ix].usercomment.decode('utf-8'),
#                                             username=helpful_comments.iloc[ix].username.decode('utf-8')))
#             return comments_to_show, url, rank, total_helpful, fraction_helpful, total_comments

#         else:
#             return {'comment':'sorry, no comments', 'username':'-'}, 'blank', 'blank'

#     else:
#         return  {'comment':'sorry, no comments', 'username':'-'}, 'blank', 'blank'



def CommentChecker(user_input):
    prediction = classify_helpful.predict([user_input])

    if prediction.any() == "helpful":
        return prediction, "yes! that sounds like useful feedback!"

    elif prediction.all() == "other":
        return prediction, "hmm... I don't know how useful that suggestion will be... can you give some more details?"

    else:
        return "sorry, Dave, I can't do that"
