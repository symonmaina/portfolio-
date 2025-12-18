from app import app, db
from models import User, Skill, Project, Profile, Education
from werkzeug.security import generate_password_hash

def seed_data():
    with app.app_context():
        db.create_all()

        # Create Admin User
        if not User.query.filter_by(username='simonmaina').first():
            user = User(username='simonmaina', password=generate_password_hash('simonmaina2399'))
            db.session.add(user)
            print("Admin user created.")

        # Seed Profile
        if not Profile.query.first():
            profile = Profile(
                name="SIMON KAMAU MAINA",
                bio="Motivated and detail-oriented Computer Science student seeking to build practical experience and strengthen my career. I am also open to networking and general IT support roles, leveraging my CCNA training and strong technical foundation.",
                phone="0745744806",
                email="simonkamau924@gmail.com",
                residence="Meru, Kenya",
                image_file="simon_profile.jpg" 
            )
            db.session.add(profile)
            print("Profile seeded.")

        # Seed Education
        if not Education.query.first():
            edu1 = Education(
                degree="Bachelor of Science in Computer Science",
                institution="Meru University of Science and Technology",
                year="Expected Graduation: 2027",
                description="Year of Study: Third Year"
            )
            db.session.add(edu1)
            print("Education seeded.")

        # Seed Skills
        if not Skill.query.first():
            skills = [
                Skill(name="Python", description="Programming Language", image_file="python.png"),
                Skill(name="Java", description="Programming Language", image_file="java.png"),
                Skill(name="JavaScript", description="Web Development", image_file="js.png"),
                Skill(name="PHP", description="Web Development", image_file="php.png"),
                Skill(name="Flask", description="Web Framework", image_file="flask.png"),
                Skill(name="MySQL", description="Database", image_file="mysql.png"),
                Skill(name="Data Science", description="Pandas, NumPy, Matplotlib", image_file="datascience.png"),
                Skill(name="Networking", description="CCNA 1 & 2 Completed", image_file="networking.png"),
                Skill(name="Git & GitHub", description="Version Control", image_file="git.png")
            ]
            db.session.add_all(skills)
            print("Skills seeded.")

        # Seed Projects
        if not Project.query.first():
            projects = [
                Project(title="High School Management System", description="Web-Based system for managing students, staff, and academic records.", image_file="school_sys.jpg", link="#"),
                Project(title="Class Schedule App", description="Android app for managing class schedules and reminders.", image_file="android_app.jpg", link="#"),
                Project(title="Personal Profile Website", description="Built a personal profile website using Python Flask.", image_file="portfolio.jpg", link="#")
            ]
            db.session.add_all(projects)
            print("Projects seeded.")

        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()
