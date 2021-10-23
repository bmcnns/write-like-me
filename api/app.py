from flask import Flask, jsonify
import sqlite3
import uuid

app = Flask(__name__)

def get_entries_for_blog_post(post_id):
	conn = sqlite3.connect("../test.db")
	cur = conn.cursor()

	query = """
		SELECT * FROM entries
		WHERE post_id = '${_post_id}';
		""".format(_post_id = post_id)

	cur.execute(query)

@app.route("/")
def index():
	return get_all_posts()


@app.route("/api/posts/<post_id>", methods=['GET'])
def get_blog_post(post_id):
	conn = sqlite3.connect("../test.db")
	cur = conn.cursor()

	query = """
		SELECT * FROM posts
		WHERE post_id = '{_post_id}';
		""".format(_post_id = post_id)

	cur.execute(query)
	
	rows = cur.fetchall()

	if len(rows) == 0:
		return "No posts found with that id."
	else:
		posts = []
		for row in rows:
			post = {
				"id": row[0],
				"header": row[1],
				"keywords": row[2],
			}
	
			posts += post

		return jsonify(posts)

@app.route("/api/posts/", methods=['GET'])
def get_all_posts():
	conn = sqlite3.connect("../test.db")
	cur = conn.cursor()
	
	query = """
		SELECT * FROM posts
		"""

	cur.execute(query)
	
	rows = cur.fetchall()

	if len(rows) == 0:
		return "No posts found."

	posts = []
	for row in rows:
		post = {
			"id": row[0],
			"header": row[1],
			"keywords": row[2]
		}

		posts.append(post)
	print (posts)

	return jsonify(posts)

@app.route("/api/posts/<post_id>", methods = ['POST'])
def create_blog_post(header, keywords, entries):
	conn = sqlite3.connect("../test.db")
	cur = conn.cursor()

	post_id = str(uuid.uuid4()) 

	query = """
		INSERT INTO "posts"
		("post_id", "header", "keywords")
		VALUES ('{_post_id}', '{_header}', '{_keywords}');
		""".format(_post_id = post_id, _header = header, _keywords = keywords)

	cur.execute(query)
	conn.commit()

	return get_blog_post(post_id)	

@app.route("/api/posts/<post_id>", methods = ['PUT'])
def update_blog_post(post_id, header, keywords, entries):
	conn = sqlite3.connect("../test.db")
	cur = conn.cursor()

	query = """
		UPDATE posts
		SET header = '{_header}', keywords = '{_keywords}'
		WHERE post_id = '{_post_id}';
		""".format(_post_id = post_id, _header = header, _keywords = keywords)

	cur.execute(query)
	conn.commit()

	return get_blog_post(post_id)

@app.route("/api/posts/<post_id>", methods = ['DELETE'])
def delete_blog_post(post_id):
	conn = sqlite3.connect("../test.db")
	cur = conn.cursor()

	query = """
		DELETE FROM posts
		WHERE post_id = '{_post_id}';
		""".format(_post_id = post_id) 

	cur.execute(query)
	conn.commit()

	return jsonify({"success": True});
