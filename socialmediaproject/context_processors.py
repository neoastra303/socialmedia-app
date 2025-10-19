from datetime import datetime

def global_context(request):
    """
    إضافة متغيرات عامة متاحة لجميع القوالب
    """
    return {
        'current_year': datetime.now().year
    } 