"""
AI Matching Service
Calculate match scores between students and jobs/mentors
"""


def calculate_job_match_score(student, job):
    """
    Calculate AI match score between student and job
    Returns score between 0-100

    Algorithm considers:
    - Skill matching
    - Education relevance
    - Experience alignment
    - Location preferences
    """
    score = 0
    max_score = 100

    # 1. Skill Matching (40 points)
    student_skills = {skill.skill_name.lower() for skill in student.skills.filter_by(deleted_at=None)}
    job_skills = {skill.skill_name.lower() for skill in job.skills_required.filter_by(deleted_at=None)}

    if job_skills:
        skill_match_ratio = len(student_skills & job_skills) / len(job_skills)
        score += skill_match_ratio * 40

    # 2. Education Relevance (20 points)
    # Check if field of study is relevant to job
    education = student.education.filter_by(deleted_at=None, is_current=True).first()
    if education:
        # Simple keyword matching (can be enhanced with NLP)
        job_keywords = job.title.lower().split() + (job.description or '').lower().split()
        education_field = education.field_of_study.lower()

        if any(keyword in education_field for keyword in job_keywords[:5]):
            score += 20
        else:
            score += 10  # Partial credit for having education

    # 3. Experience Level (20 points)
    experience_count = student.experience.filter_by(deleted_at=None).count()
    if job.job_type == 'internship':
        score += min(experience_count * 10, 20)  # Internships don't need much experience
    elif job.job_type == 'full-time':
        if experience_count >= 2:
            score += 20
        elif experience_count == 1:
            score += 15
        else:
            score += 5

    # 4. Location Match (10 points)
    if job.work_mode == 'remote':
        score += 10
    elif student.location and job.location:
        if student.location.lower() in job.location.lower() or job.location.lower() in student.location.lower():
            score += 10
        else:
            score += 5  # Partial credit for being willing to relocate

    # 5. Profile Completeness Bonus (10 points)
    completeness = 0
    if student.bio:
        completeness += 2
    if student.resume_url:
        completeness += 3
    if student.portfolio_url or student.github_url:
        completeness += 3
    if student.skills.count() >= 3:
        completeness += 2

    score += completeness

    return min(int(score), max_score)


def calculate_mentor_match_score(student, mentor):
    """
    Calculate AI match score between student and mentor
    Returns score between 0-100

    Algorithm considers:
    - Career interests alignment
    - Skill overlap
    - Industry match
    - Experience level
    """
    score = 0

    # 1. Skill Overlap (35 points)
    student_skills = {skill.skill_name.lower() for skill in student.skills.filter_by(deleted_at=None)}
    mentor_expertise = {exp.expertise_area.lower() for exp in mentor.expertise.filter_by(deleted_at=None)}

    if mentor_expertise:
        overlap_ratio = len(student_skills & mentor_expertise) / len(mentor_expertise)
        score += overlap_ratio * 35

    # 2. Career Path Alignment (25 points)
    # Check if student's target roles align with mentor's experience
    recent_experience = student.experience.filter_by(deleted_at=None).order_by('-start_date').first()
    if recent_experience:
        if mentor.current_role.lower() in recent_experience.position.lower() or \
           recent_experience.position.lower() in mentor.current_role.lower():
            score += 25
        else:
            score += 10

    # 3. Mentor Quality (25 points)
    # Based on rating and experience
    if mentor.rating:
        score += (float(mentor.rating) / 5.0) * 15
    if mentor.total_sessions >= 10:
        score += 10
    elif mentor.total_sessions >= 5:
        score += 5

    # 4. Education Relevance (15 points)
    education = student.education.filter_by(deleted_at=None, is_current=True).first()
    if education:
        # If mentor's company or role relates to student's field
        if education.field_of_study.lower() in (mentor.current_role + ' ' + mentor.current_company).lower():
            score += 15
        else:
            score += 5

    return min(int(score), 100)


def get_recommended_jobs(student, limit=10):
    """
    Get top recommended jobs for student
    """
    from app.models.job import Job

    active_jobs = Job.query.filter_by(status='active', deleted_at=None).all()

    # Calculate match scores
    job_scores = []
    for job in active_jobs:
        match_score = calculate_job_match_score(student, job)
        job_scores.append((job, match_score))

    # Sort by score and return top matches
    job_scores.sort(key=lambda x: x[1], reverse=True)

    return [
        {**job.to_dict(include_skills=True), 'match_score': score}
        for job, score in job_scores[:limit]
    ]


def get_recommended_mentors(student, limit=10):
    """
    Get top recommended mentors for student
    """
    from app.models.mentor import MentorProfile

    mentors = MentorProfile.query.filter_by(deleted_at=None).all()

    # Calculate match scores
    mentor_scores = []
    for mentor in mentors:
        match_score = calculate_mentor_match_score(student, mentor)
        mentor_scores.append((mentor, match_score))

    # Sort by score and return top matches
    mentor_scores.sort(key=lambda x: x[1], reverse=True)

    return [
        {**mentor.to_dict(include_expertise=True), 'match_score': score}
        for mentor, score in mentor_scores[:limit]
    ]
