# Database Design

## Database Name

internship_platform

## Main Entities

- Users
- Student Profiles
- Employers
- Skills
- Student Skills
- Internships
- Internship Skills
- Applications
- Match Scores

## Relationships

- One user can have one student profile.
- One user can have one employer profile.
- One employer can post many internships.
- One student can have many skills.
- One skill can belong to many students.
- One internship can require many skills.
- One skill can be required by many internships.
- One student can submit many applications.
- One internship can receive many applications.
- One student can have match scores for multiple internships.