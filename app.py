from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, Project, Skill, Profile, Education, Message
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///portfolio.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Context Processor to inject Profile into all templates
@app.context_processor
def inject_profile():
    profile = Profile.query.first()
    return dict(profile=profile)

@app.route("/")
def home_page():
    skills = Skill.query.all()
    education_list = Education.query.all()
    return render_template("home.html", skills=skills, education_list=education_list)

@app.route("/projects")
def projects_page():
    projects = Project.query.all()
    return render_template("projects.html", projects=projects)

@app.route("/contact", methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        msg = Message(name=name, email=email, message=message)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent!', 'success')
        return redirect(url_for('contact_page'))
    return render_template("contact.html")

# Admin Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))

@app.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.all()
    skills = Skill.query.all()
    education_list = Education.query.all()
    messages = Message.query.order_by(Message.date_posted.desc()).all()
    return render_template('dashboard.html', projects=projects, skills=skills, education_list=education_list, messages=messages)

# --- Project Routes ---
@app.route('/project/new', methods=['GET', 'POST'])
@login_required
def new_project():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        link = request.form.get('link')
        
        image_filename = 'default.jpg'
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filename = filename

        project = Project(title=title, description=description, link=link, image_file=image_filename)
        db.session.add(project)
        db.session.commit()
        flash('Project has been created!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_item.html', item_type='project', legend='New Project')

@app.route('/project/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.link = request.form.get('link')
        
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                project.image_file = filename
                
        db.session.commit()
        flash('Project has been updated!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_item.html', item_type='project', legend='Edit Project', item=project)

@app.route('/project/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project has been deleted!', 'success')
    return redirect(url_for('dashboard'))

# --- Skill Routes ---
@app.route('/skill/new', methods=['GET', 'POST'])
@login_required
def new_skill():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        image_filename = 'default.jpg'
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filename = filename
        
        skill = Skill(name=name, description=description, image_file=image_filename)
        db.session.add(skill)
        db.session.commit()
        flash('Skill has been added!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_item.html', item_type='skill', legend='New Skill')

@app.route('/skill/<int:skill_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if request.method == 'POST':
        skill.name = request.form.get('name')
        skill.description = request.form.get('description')
        
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                skill.image_file = filename
                
        db.session.commit()
        flash('Skill has been updated!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_item.html', item_type='skill', legend='Edit Skill', item=skill)

@app.route('/skill/<int:skill_id>/delete', methods=['POST'])
@login_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill has been deleted!', 'success')
    return redirect(url_for('dashboard'))

# --- Education Routes ---
@app.route('/education/new', methods=['GET', 'POST'])
@login_required
def new_education():
    if request.method == 'POST':
        degree = request.form.get('degree')
        institution = request.form.get('institution')
        year = request.form.get('year')
        description = request.form.get('description')
        
        edu = Education(degree=degree, institution=institution, year=year, description=description)
        db.session.add(edu)
        db.session.commit()
        flash('Education added!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_item.html', item_type='education', legend='New Education')

@app.route('/education/<int:edu_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_education(edu_id):
    edu = Education.query.get_or_404(edu_id)
    if request.method == 'POST':
        edu.degree = request.form.get('degree')
        edu.institution = request.form.get('institution')
        edu.year = request.form.get('year')
        edu.description = request.form.get('description')
        db.session.commit()
        flash('Education updated!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_item.html', item_type='education', legend='Edit Education', item=edu)

@app.route('/education/<int:edu_id>/delete', methods=['POST'])
@login_required
def delete_education(edu_id):
    edu = Education.query.get_or_404(edu_id)
    db.session.delete(edu)
    db.session.commit()
    flash('Education deleted!', 'success')
    return redirect(url_for('dashboard'))

# --- Profile Routes ---
@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    profile = Profile.query.first()
    if not profile:
        profile = Profile(name="New User", bio="Bio", image_file="default.jpg")
        db.session.add(profile)
        db.session.commit()
    
    if request.method == 'POST':
        profile.name = request.form.get('name')
        profile.bio = request.form.get('bio')
        profile.phone = request.form.get('phone')
        profile.email = request.form.get('email')
        profile.residence = request.form.get('residence')
        
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile.image_file = filename
                
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_item.html', item_type='profile', legend='Edit Profile', item=profile)

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)