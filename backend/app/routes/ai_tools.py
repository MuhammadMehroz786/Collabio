"""
AI Tools Routes
"""
from flask import Blueprint, request
from app.utils.auth import token_required, user_type_required, get_current_user
from app.utils.helpers import success_response, error_response, paginate
from app.models.all_models import AIToolUsage
from app.extensions import db

ai_tools_bp = Blueprint('ai_tools', __name__)


@ai_tools_bp.route('/usage-history', methods=['GET'])
@token_required
@user_type_required('student')
def get_usage_history():
    """Get AI tool usage history"""
    user = get_current_user()
    student = user.student_profile

    query = AIToolUsage.query.filter_by(
        student_id=student.student_id,
        deleted_at=None
    ).order_by(AIToolUsage.used_at.desc())

    # Filter by tool
    if 'tool_name' in request.args:
        query = query.filter_by(tool_name=request.args['tool_name'])

    result = paginate(query)
    return success_response(data=result)


@ai_tools_bp.route('/resume-builder', methods=['POST'])
@token_required
@user_type_required('student')
def resume_builder():
    """AI Resume Builder Tool"""
    user = get_current_user()
    student = user.student_profile
    data = request.get_json() or {}

    # Get student data
    education = [edu.to_dict() for edu in student.education.filter_by(deleted_at=None)]
    experience = [exp.to_dict() for exp in student.experience.filter_by(deleted_at=None)]
    skills = [skill.to_dict() for skill in student.skills.filter_by(deleted_at=None)]

    # AI Analysis (Placeholder - integrate with actual AI service)
    result = {
        'score': 85,
        'suggestions': [
            'Add more quantifiable achievements to your experience',
            'Include 2-3 more technical skills',
            'Add a professional summary at the top'
        ],
        'strengths': [
            'Strong educational background',
            'Relevant work experience',
            'Good skill diversity'
        ],
        'template_recommendations': ['modern', 'technical', 'minimal']
    }

    # Log usage
    try:
        usage = AIToolUsage(
            student_id=student.student_id,
            tool_name='resume_builder',
            result_data=result
        )
        usage.save()
    except:
        pass  # Don't fail if logging fails

    return success_response(data=result, message='Resume analysis complete')


@ai_tools_bp.route('/career-counselor', methods=['POST'])
@token_required
@user_type_required('student')
def career_counselor():
    """AI Career Counselor Tool"""
    user = get_current_user()
    student = user.student_profile
    data = request.get_json() or {}

    question = data.get('question', '')

    # AI Career Guidance (Placeholder - integrate with actual AI service)
    result = {
        'response': 'Based on your computer science background and interest in full-stack development, I recommend focusing on building projects that showcase both frontend and backend skills. Consider contributing to open-source projects and building a strong portfolio.',
        'related_jobs_count': 15,
        'suggested_skills': ['React', 'Node.js', 'Docker', 'AWS'],
        'recommended_courses': ['System Design', 'Advanced React Patterns']
    }

    # Log usage
    try:
        usage = AIToolUsage(
            student_id=student.student_id,
            tool_name='career_counselor',
            result_data={'question': question, 'response': result}
        )
        usage.save()
    except:
        pass

    return success_response(data=result, message='Career guidance generated')


@ai_tools_bp.route('/interview-prep', methods=['POST'])
@token_required
@user_type_required('student')
def interview_prep():
    """AI Interview Prep Tool"""
    user = get_current_user()
    student = user.student_profile
    data = request.get_json() or {}

    interview_type = data.get('interview_type', 'technical')

    # AI Interview Practice (Placeholder - integrate with actual AI service)
    result = {
        'questions': [
            {
                'question': 'Tell me about yourself',
                'category': 'behavioral',
                'tips': 'Focus on your journey, key achievements, and why you\'re interested in this role'
            },
            {
                'question': 'What is the difference between let, const, and var in JavaScript?',
                'category': 'technical',
                'tips': 'Explain scope, hoisting, and reassignment differences'
            },
            {
                'question': 'Describe a challenging project you worked on',
                'category': 'behavioral',
                'tips': 'Use the STAR method: Situation, Task, Action, Result'
            }
        ],
        'feedback': 'Practice answering these questions out loud. Record yourself to improve delivery.',
        'recommended_practice_time': '30 minutes daily'
    }

    # Log usage
    try:
        usage = AIToolUsage(
            student_id=student.student_id,
            tool_name='interview_prep',
            result_data={'interview_type': interview_type, 'result': result}
        )
        usage.save()
    except:
        pass

    return success_response(data=result, message='Interview questions generated')


@ai_tools_bp.route('/skill-gap', methods=['POST'])
@token_required
@user_type_required('student')
def skill_gap_analysis():
    """AI Skill Gap Analysis Tool"""
    user = get_current_user()
    student = user.student_profile
    data = request.get_json() or {}

    target_role = data.get('target_role', 'Software Engineer')

    # Get student skills
    student_skills = {skill.skill_name.lower() for skill in student.skills.filter_by(deleted_at=None)}

    # AI Skill Gap Analysis (Placeholder - integrate with actual AI service)
    required_skills = ['javascript', 'react', 'node.js', 'sql', 'git', 'rest api', 'testing']
    missing_skills = [skill for skill in required_skills if skill not in student_skills]

    result = {
        'target_role': target_role,
        'current_skills': list(student_skills),
        'required_skills': required_skills,
        'missing_skills': missing_skills,
        'skill_match_percentage': int((1 - len(missing_skills) / len(required_skills)) * 100),
        'recommendations': [
            {
                'skill': skill,
                'priority': 'high' if i < 2 else 'medium',
                'learning_resources': [
                    f'Learn {skill} - Online Course',
                    f'{skill} Documentation',
                    f'Practice {skill} Projects'
                ]
            }
            for i, skill in enumerate(missing_skills[:3])
        ]
    }

    # Log usage
    try:
        usage = AIToolUsage(
            student_id=student.student_id,
            tool_name='skill_gap',
            result_data={'target_role': target_role, 'result': result}
        )
        usage.save()
    except:
        pass

    return success_response(data=result, message='Skill gap analysis complete')


@ai_tools_bp.route('/available-tools', methods=['GET'])
@token_required
def get_available_tools():
    """Get list of available AI tools"""
    tools = [
        {
            'name': 'resume_builder',
            'title': 'Resume Builder',
            'description': 'AI-powered resume optimization with industry-specific templates and ATS scoring',
            'icon': 'file-text'
        },
        {
            'name': 'career_counselor',
            'title': 'Career Counselor',
            'description': 'Get personalized career advice and path recommendations based on your goals',
            'icon': 'message-square'
        },
        {
            'name': 'interview_prep',
            'title': 'Interview Prep',
            'description': 'Practice with AI-driven mock interviews and get instant feedback on your answers',
            'icon': 'video'
        },
        {
            'name': 'skill_gap',
            'title': 'Skill Gap Analysis',
            'description': 'Identify skills you need for your dream job and get learning recommendations',
            'icon': 'target'
        }
    ]

    return success_response(data=tools)
