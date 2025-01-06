from .user import StudentRepository, ProfessorRepository, AdminRepository
from .student_courses import StudentCoursesRepository
from .activities import ActivitiesRepository
from .courses import CoursesRepository
from .lessons import LessonsRepository
from .exercises import ExercisesRepository
from .student_lessons import StudentLessonsRepository
from .student_exercises import StudentExercisesRepository
from .documents import DocumentsRepository
from .modules import ModulesRepository
from .quiz_exercises import QuizExercisesRepository
from .recommend_documents import RecommendDocumentsRepository
from .learning_paths import LearningPathsRepository
from .recommend_lessons import RecommendLessonsRepository
__all__ = [
    "StudentRepository",
    "ProfessorRepository",
    "AdminRepository",
    "StudentCoursesRepository",
    "ActivitiesRepository",
    "CoursesRepository",
    "LessonsRepository",
    "ExercisesRepository",
    "StudentLessonsRepository",
    "StudentExercisesRepository",
    "DocumentsRepository",
    "ModulesRepository",
    "QuizExercisesRepository",
    "RecommendDocumentsRepository",
    "LearningPathsRepository",
    "RecommendLessonsRepository",
]
