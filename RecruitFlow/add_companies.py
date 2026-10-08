#!/usr/bin/env python
"""Add 10 sample jobs to the configured RecruitFlow database."""

from app import create_app
from app.database.db import db
from app.models.job import Job

def main():
    app = create_app()
    
    # Sample companies with job data
    companies = [
        {
            "title": "Senior Software Engineer",
            "company": "TechCorp Solutions",
            "location": "San Francisco, CA",
            "salary": "$150,000 - $200,000",
            "experience": "5+ years",
            "skills": "Python, React, AWS, Docker, Kubernetes",
            "description": "We are looking for a Senior Software Engineer to join our growing team. You will be responsible for designing and implementing scalable backend services."
        },
        {
            "title": "Frontend Developer",
            "company": "Digital Innovations Inc",
            "location": "New York, NY",
            "salary": "$120,000 - $160,000",
            "experience": "3+ years",
            "skills": "React, TypeScript, Redux, CSS, HTML",
            "description": "Join our frontend team to build beautiful and responsive user interfaces for our SaaS platform."
        },
        {
            "title": "Data Scientist",
            "company": "Analytics Pro",
            "location": "Boston, MA",
            "salary": "$130,000 - $180,000",
            "experience": "4+ years",
            "skills": "Python, Machine Learning, SQL, TensorFlow, Pandas",
            "description": "We need a Data Scientist to analyze large datasets and build predictive models for our clients."
        },
        {
            "title": "DevOps Engineer",
            "company": "CloudScale Systems",
            "location": "Austin, TX",
            "salary": "$140,000 - $190,000",
            "experience": "4+ years",
            "skills": "AWS, Terraform, Kubernetes, CI/CD, Linux",
            "description": "Help us build and maintain our cloud infrastructure. Experience with AWS and Kubernetes required."
        },
        {
            "title": "Full Stack Developer",
            "company": "StartupXYZ",
            "location": "Remote",
            "salary": "$110,000 - $150,000",
            "experience": "3+ years",
            "skills": "Node.js, React, PostgreSQL, GraphQL, TypeScript",
            "description": "Early stage startup looking for a versatile Full Stack Developer to own features end-to-end."
        },
        {
            "title": "Mobile App Developer",
            "company": "MobileFirst Labs",
            "location": "Los Angeles, CA",
            "salary": "$125,000 - $170,000",
            "experience": "3+ years",
            "skills": "React Native, iOS, Android, Swift, Kotlin",
            "description": "Build cross-platform mobile applications for our enterprise clients."
        },
        {
            "title": "Backend Engineer",
            "company": "FinTech Solutions",
            "location": "Chicago, IL",
            "salary": "$145,000 - $195,000",
            "experience": "5+ years",
            "skills": "Java, Spring Boot, PostgreSQL, Kafka, Microservices",
            "description": "Design and develop high-performance backend services for financial applications."
        },
        {
            "title": "AI/ML Engineer",
            "company": "Intelligent Systems Co",
            "location": "Seattle, WA",
            "salary": "$160,000 - $220,000",
            "experience": "4+ years",
            "skills": "Python, PyTorch, TensorFlow, MLOps, Deep Learning",
            "description": "Work on cutting-edge AI/ML projects including NLP, computer vision, and recommendation systems."
        },
        {
            "title": "Security Engineer",
            "company": "CyberShield Technologies",
            "location": "Washington, DC",
            "salary": "$135,000 - $185,000",
            "experience": "4+ years",
            "skills": "Network Security, Penetration Testing, SIEM, Python, Compliance",
            "description": "Protect our infrastructure and applications from security threats. Certifications preferred."
        },
        {
            "title": "QA Automation Engineer",
            "company": "QualityFirst Inc",
            "location": "Denver, CO",
            "salary": "$100,000 - $140,000",
            "experience": "3+ years",
            "skills": "Selenium, Cypress, Python, Jenkins, TestNG",
            "description": "Build and maintain automated test frameworks for our web and mobile applications."
        }
    ]
    
    with app.app_context():
        existing_jobs = {
            (title, company)
            for title, company in db.session.query(Job.title, Job.company).all()
        }
        jobs_to_add = [
            Job(**job_data, status="Active")
            for job_data in companies
            if (job_data["title"], job_data["company"]) not in existing_jobs
        ]

        db.session.add_all(jobs_to_add)
        db.session.commit()

        print(f"Added {len(jobs_to_add)} jobs.")
        print(f"Total jobs: {Job.query.count()}")

if __name__ == "__main__":
    main()