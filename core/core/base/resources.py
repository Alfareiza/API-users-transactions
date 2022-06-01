from typing import Dict, List

from django.db.models.query import RawQuerySet

from core.base.models import Transaction


def calc_summary_user(queryset_user: Transaction) -> Dict[dict, dict]:
    """
    This function receive a queryset of transaction according
     to a specific user.
    :param transaction: Queryset with the all the
     transaction of an specific user.
    :return: Dict of dicts that depicts the summary
    of an specific user.
    """
    inflow, outflow = dict(), dict()
    for field in queryset_user:
        if field.type == "inflow":
            if inflow.get(field.category):
                inflow[field.category] += field.amount
            else:
                inflow[field.category] = field.amount
        elif field.type == "outflow":
            if outflow.get(field.category):
                outflow[field.category] += field.amount
            else:
                outflow[field.category] = field.amount
    return {"inflow": inflow, "outflow": outflow}


def group_types_by_user_email(raw_query: RawQuerySet) -> List[dict]:
    """
    From the result of an raw_queryset. Calculates how much is
    the total of inflow and outflow of every user.
    :param raw_query: RawQuerySet that is the result of
     a query execucted previously.
    :return: List of dicts that depicts the total inflow
    and outflow of every user_email.
    """
    result = []
    for t in raw_query:
        dict_transaction = {
            "user_email": t.user_email,
            "total_inflow": t.total_inflow,
            "total_outflow": t.total_outflow,
        }
        result.append(dict_transaction.copy())
    return result
