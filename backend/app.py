# # backend/app.py
# from flask import Flask, request, jsonify, abort
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# from datetime import datetime
# import json

# app = Flask(__name__)
# CORS(app)

# # SQLite DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///models.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# # Project model
# class Project(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     category = db.Column(db.String(50))
#     tools = db.Column(db.Text)        # JSON-encoded list
#     imageUrls = db.Column(db.Text)    # JSON-encoded list
#     projectUrl = db.Column(db.String(300))
#     clientName = db.Column(db.String(200))
#     completionYear = db.Column(db.Integer)
#     tags = db.Column(db.Text)         # JSON-encoded list
#     isFeatured = db.Column(db.Boolean, default=False)
#     createdAt = db.Column(db.DateTime, default=datetime.utcnow)
#     updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "title": self.title,
#             "description": self.description,
#             "category": self.category,
#             "tools": json.loads(self.tools) if self.tools else [],
#             "imageUrls": json.loads(self.imageUrls) if self.imageUrls else [],
#             "projectUrl": self.projectUrl,
#             "clientName": self.clientName,
#             "completionYear": self.completionYear,
#             "tags": json.loads(self.tags) if self.tags else [],
#             "isFeatured": self.isFeatured,
#             "createdAt": self.createdAt.isoformat(),
#             "updatedAt": self.updatedAt.isoformat() if self.updatedAt else None
#         }

# # Initialize DB (create tables)
# @app.before_first_request
# def create_tables():
#     db.create_all()

# # Routes
# @app.route('/api/projects', methods=['GET'])
# def get_projects():
#     # query params for filter/search
#     category = request.args.get('category')
#     tool = request.args.get('tool')
#     year = request.args.get('year')
#     q = request.args.get('q')  # search term
    
#     query = Project.query
#     if category:
#         query = query.filter_by(category=category)
#     if year:
#         try:
#             y = int(year)
#             query = query.filter_by(completionYear=y)
#         except:
#             pass
#     if tool:
#         # naive contains: convert tools JSON -> string check
#         query = query.filter(Project.tools.like(f'%{tool}%'))
#     if q:
#         qlike = f'%{q}%'
#         query = query.filter((Project.title.ilike(qlike)) | (Project.description.ilike(qlike)) | (Project.tags.like(f'%{q}%')))

#     projects = query.order_by(Project.createdAt.desc()).all()
#     return jsonify([p.to_dict() for p in projects]), 200

# @app.route('/api/projects/<int:pid>', methods=['GET'])
# def get_project(pid):
#     p = Project.query.get_or_404(pid)
#     return jsonify(p.to_dict()), 200

# @app.route('/api/projects', methods=['POST'])
# def create_project():
#     data = request.get_json()
#     required = ['title', 'description']
#     for r in required:
#         if r not in data or not data[r]:
#             return jsonify({"error": f"{r} is required"}), 400

#     def js(v):
#         return json.dumps(v) if v is not None else json.dumps([])

#     p = Project(
#         title = data.get('title'),
#         description = data.get('description'),
#         category = data.get('category'),
#         tools = js(data.get('tools', [])),
#         imageUrls = js(data.get('imageUrls', [])),
#         projectUrl = data.get('projectUrl'),
#         clientName = data.get('clientName'),
#         completionYear = data.get('completionYear'),
#         tags = js(data.get('tags', [])),
#         isFeatured = bool(data.get('isFeatured', False))
#     )
#     db.session.add(p)
#     db.session.commit()
#     return jsonify(p.to_dict()), 201

# @app.route('/api/projects/<int:pid>', methods=['PUT'])
# def update_project(pid):
#     p = Project.query.get_or_404(pid)
#     data = request.get_json()
#     # update fields if present
#     for field in ['title', 'description', 'category', 'projectUrl', 'clientName']:
#         if field in data:
#             setattr(p, field, data[field])
#     if 'tools' in data:
#         p.tools = json.dumps(data['tools'] or [])
#     if 'imageUrls' in data:
#         p.imageUrls = json.dumps(data['imageUrls'] or [])
#     if 'tags' in data:
#         p.tags = json.dumps(data['tags'] or [])
#     if 'completionYear' in data:
#         p.completionYear = data.get('completionYear')
#     if 'isFeatured' in data:
#         p.isFeatured = bool(data.get('isFeatured'))
#     db.session.commit()
#     return jsonify(p.to_dict()), 200

# @app.route('/api/projects/<int:pid>', methods=['DELETE'])
# def delete_project(pid):
#     p = Project.query.get_or_404(pid)
#     db.session.delete(p)
#     db.session.commit()
#     return jsonify({"message":"deleted"}), 200

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
# backend/app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)

# ---- DB config (SQLite file in same folder) ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "projects.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Allow frontend on another port (5500) to call this API
CORS(app, resources={r"/api/*": {"origins": "*"}})


# ---- Model ----
class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))
    tools = db.Column(db.Text)        # JSON string list
    imageUrls = db.Column(db.Text)    # JSON string list
    projectUrl = db.Column(db.String(300))
    clientName = db.Column(db.String(200))
    completionYear = db.Column(db.Integer)
    tags = db.Column(db.Text)         # JSON string list
    isFeatured = db.Column(db.Boolean, default=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self):
        # convert JSON strings back to lists
        def parse_list(s):
            if not s:
                return []
            try:
                return json.loads(s)
            except Exception:
                return []

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "tools": parse_list(self.tools),
            "imageUrls": parse_list(self.imageUrls),
            "projectUrl": self.projectUrl,
            "clientName": self.clientName,
            "completionYear": self.completionYear,
            "tags": parse_list(self.tags),
            "isFeatured": bool(self.isFeatured),
            "createdAt": self.createdAt.isoformat() if self.createdAt else None,
            "updatedAt": self.updatedAt.isoformat() if self.updatedAt else None,
        }


# ---- Helper for encoding list fields ----
def to_json_list(value):
    if value is None:
        return json.dumps([])
    # if frontend accidentally sends string instead of list, wrap it
    if isinstance(value, str):
        return json.dumps([value])
    return json.dumps(value)


# ---- API Endpoints ----

# GET /api/projects  (with optional filters and search)
@app.route("/api/projects", methods=["GET"])
def get_projects():
    category = request.args.get("category")
    year = request.args.get("year")
    q = request.args.get("q")
    tool = request.args.get("tool")

    query = Project.query

    if category:
        query = query.filter_by(category=category)

    if year:
        try:
            y = int(year)
            query = query.filter_by(completionYear=y)
        except ValueError:
            pass

    if tool:
        # naive text search in JSON string
        like = f"%{tool}%"
        query = query.filter(Project.tools.like(like))

    if q:
        like_q = f"%{q}%"
        query = query.filter(
            (Project.title.ilike(like_q))
            | (Project.description.ilike(like_q))
            | (Project.tags.like(like_q))
        )

    projects = query.order_by(Project.createdAt.desc()).all()
    return jsonify([p.to_dict() for p in projects]), 200


# GET /api/projects/:id
@app.route("/api/projects/<int:pid>", methods=["GET"])
def get_project(pid):
    p = Project.query.get_or_404(pid)
    return jsonify(p.to_dict()), 200


# POST /api/projects
@app.route("/api/projects", methods=["POST"])
def create_project():
    data = request.get_json() or {}
    title = data.get("title")
    description = data.get("description")

    if not title or not description:
        return jsonify({"error": "title and description are required"}), 400

    p = Project(
        title=title,
        description=description,
        category=data.get("category"),
        tools=to_json_list(data.get("tools", [])),
        imageUrls=to_json_list(data.get("imageUrls", [])),
        projectUrl=data.get("projectUrl"),
        clientName=data.get("clientName"),
        completionYear=data.get("completionYear"),
        tags=to_json_list(data.get("tags", [])),
        isFeatured=bool(data.get("isFeatured", False)),
    )
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201


# PUT /api/projects/:id
@app.route("/api/projects/<int:pid>", methods=["PUT"])
def update_project(pid):
    p = Project.query.get_or_404(pid)
    data = request.get_json() or {}

    if "title" in data and data["title"]:
        p.title = data["title"]
    if "description" in data and data["description"]:
        p.description = data["description"]

    if "category" in data:
        p.category = data.get("category")

    if "tools" in data:
        p.tools = to_json_list(data.get("tools"))

    if "imageUrls" in data:
        p.imageUrls = to_json_list(data.get("imageUrls"))

    if "projectUrl" in data:
        p.projectUrl = data.get("projectUrl")

    if "clientName" in data:
        p.clientName = data.get("clientName")

    if "completionYear" in data:
        p.completionYear = data.get("completionYear")

    if "tags" in data:
        p.tags = to_json_list(data.get("tags"))

    if "isFeatured" in data:
        p.isFeatured = bool(data.get("isFeatured"))

    db.session.commit()
    return jsonify(p.to_dict()), 200


# DELETE /api/projects/:id
@app.route("/api/projects/<int:pid>", methods=["DELETE"])
def delete_project(pid):
    p = Project.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200


# ---- Run app ----
if __name__ == "__main__":
    # create tables if not exist
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
    # app.run(debug=True, port=5000)
