from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from models import db, File, Genre, Subgenre
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Initialize database
with app.app_context():
    db.create_all()

# Home route - renders the main page
@app.route('/')
def index():
    popular_files = File.query.order_by(File.download_count.desc()).limit(5).all()
    all_files = File.query.all()
    genres = Genre.query.all()
    return render_template('index.html', popular_files=popular_files, all_files=all_files, genres=genres)

# Route to upload files
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    description = request.form.get('description')
    genre_id = request.form.get('genre')
    subgenre_id = request.form.get('subgenre')

    if file:
        filepath = f"uploads/{file.filename}"
        file.save(filepath)

        new_file = File(
            filename=file.filename,
            path=filepath,
            description=description,
            size=len(file.read()),
            download_count=0,
            genre_id=genre_id,
            subgenre_id=subgenre_id
        )
        db.session.add(new_file)
        db.session.commit()

    return redirect(url_for('index'))

# Route to download a file
@app.route('/download/<int:file_id>')
def download(file_id):
    file = File.query.get(file_id)
    if file:
        file.download_count += 1
        db.session.commit()
        return send_file(file.path, as_attachment=True, download_name=file.filename)
    return "File not found", 404

# Route to filter files by genre, subgenre, and description
@app.route('/filter_files', methods=['POST'])
def filter_files():
    genre_id = request.json.get('genre_id')
    subgenre_id = request.json.get('subgenre_id')
    description = request.json.get('description')

    query = File.query
    if genre_id:
        query = query.filter_by(genre_id=genre_id)
    if subgenre_id:
        query = query.filter_by(subgenre_id=subgenre_id)
    if description:
        query = query.filter(File.description.contains(description))

    filtered_files = query.all()
    return jsonify([file.to_dict() for file in filtered_files])

if __name__ == "__main__":
    app.run(debug=True)
