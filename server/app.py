from config import app, api
from models import Post, Comment
from flask_restful import Resource

# create routes here:
class SortedPosts(Resource):
  def get(self):
    #posts_alphabetized_dict_list = [p.to_dict() for p in Post.query.order_by(Post.title).all()]
    posts_alphabetized_dict_list = sorted([p.to_dict() for p in Post.query.all()], key=lambda x: x['title'])
    return posts_alphabetized_dict_list, 200
api.add_resource(SortedPosts, '/api/sorted_posts')

class AuthorByName(Resource):
  def get(self, author_name):
    posts = Post.query.filter(Post.author == author_name).all()
    posts_dict_list = [p.to_dict() for p in posts]
    return posts_dict_list, 200
api.add_resource(AuthorByName, '/api/posts_by_author/<string:author_name>')

class SearchedPosts(Resource):
  def get(self, title):
    posts = Post.query.filter(Post.title.contains(title)).all()
    posts_dict_list = [p.to_dict() for p in posts]
    return posts_dict_list, 200
api.add_resource(SearchedPosts, '/api/search_posts/<string:title>')

class PostsOrderedByNumComments(Resource):
  def get(self):
    posts_dict_list = sorted([p.to_dict() for p in Post.query.all()], key=lambda x: len(x['comments']), reverse=True)
    return posts_dict_list, 200
api.add_resource(PostsOrderedByNumComments, '/api/posts_ordered_by_num_comments')

class MostPopularCommenter(Resource):
  def get(self):
    commenters = {}
    # for each comment in database
    for c in [comment.to_dict() for comment in Comment.query.all()]:
      # count comments made by each commenter
      commenters[c['commenter']] = commenters.get(c['commenter'], 0) + 1  
    # for each commenter in commenters dictionary
    for commenter in commenters:
      # if commenter had greatest number of comments
      if commenters[commenter] == max(commenters.values()):
        most_popular = commenter
    return {'commenter': most_popular}, 200
api.add_resource(MostPopularCommenter, '/api/most_popular')
    



if __name__ == "__main__":
  app.run(port=5555, debug=True)