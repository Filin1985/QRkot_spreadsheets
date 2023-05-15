from datetime import datetime


def investment_process(
    target,
    sources,
) -> None:
    result_objects = []
    for source in sources:
        incoming_objects = [target, source]
        amount = min(
            source.full_amount - (source.invested_amount or 0),
            target.full_amount - (target.invested_amount or 0))
        for object in incoming_objects:
            object.invested_amount = (object.invested_amount or 0) + amount
            if object.full_amount == object.invested_amount:
                object.fully_invested = True
                object.close_date = datetime.now()
        result_objects.append(source)
        if target.fully_invested:
            break
    return result_objects
