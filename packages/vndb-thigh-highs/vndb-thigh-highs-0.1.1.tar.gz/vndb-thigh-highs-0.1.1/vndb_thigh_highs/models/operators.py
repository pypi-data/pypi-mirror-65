from .table import Operator

def and_(left, right):
    return Operator.AND.make_filter(left, right)
def or_(left, right):
    return Operator.OR.make_filter(left, right)
def search(left, right):
    return Operator.SEARCH.make_filter(left, right)
