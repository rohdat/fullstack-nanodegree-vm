#
# Database access functions for the web forum.
# 

import time
import psycopg2

## Database connection
DB = []

## Get posts from database.
def GetAllPosts():
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    #c.execute("UPDATE posts SET content = 'cheese' where content like '%SPAM%'")
    c.execute("DELETE FROM posts where content like '%Spam%'")
    #c.execute("DELETE FROM posts ")
    #DB.commit()
    c.execute("SELECT time, content FROM posts ORDER BY time desc")
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    ''' 
    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in c.fetchall()]
    DB.close()
    return posts

## Add a post to the database.
def AddPost(content):
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    #c.execute("UPDATE posts SET content = 'cheese' where content like '%SPAM%'")
    c.execute("INSERT INTO posts (content) VALUES (%s)" , (content,))
    DB.commit()
    DB.close()
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''

#   <script>
#       setTimeout(function() {
    #   var tt = document.getElementById('content');
    #   tt.value = "<h2 style='color: #FF6699; font-family: Comic Sans MS'>Spam, spam, spam, spam,<br>Wonderful spam, glorious spam!</h2>";
    #   tt.form.submit();
#       }, 2500);
#   </script>
