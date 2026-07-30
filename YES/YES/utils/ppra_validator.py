def validate_ppra_code(code, category=None):
    from models.ppra_code import PPRACode
    query = PPRACode.query.filter_by(code=code, is_active=True)
    if category:
        query = query.filter_by(category=category)
    return query.first() is not None

def get_eligibility_requirements(code):
    from models.ppra_code import PPRACode
    pcode = PPRACode.query.filter_by(code=code).first()
    if pcode:
        return {'min_turnover': pcode.min_turnover, 'min_experience': pcode.min_experience_years,
                'certifications': pcode.required_certifications}
    return None
