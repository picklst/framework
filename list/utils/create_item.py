import uuid

from list.models import List, Position, Item


def create_item(o):
    if hasattr(o, "list") and List.objects.filter(id=o.list.id).exists():
        if hasattr(o, "position") and not Position.objects.filter(list=o.list, position=o.position).exists():
            # obtain the item key, generate a uuid if key is not provided in the obj
            key = o.key if hasattr(o, "key") and o.key is not None else uuid.uuid4().hex[:8]
            while Item.objects.filter(key=key).exists():
                key = uuid.uuid4().hex[:8]

            itemObj = Item(
                name=o.name,
                key=key,
                list=o.list,
            )
            if hasattr(o, "comment") and o.comment is not None:
                itemObj.comment = o.comment
            if hasattr(o, "url") and o.url is not None:
                itemObj.url = o.url

            # save and the obj to db
            itemObj.save()

            # create and save position for the item in the list
            Position.objects.create(
                item=itemObj,
                list=o.list,
                position=o.position
            )
            return itemObj
        raise Exception(AttributeError, "Item position required, and be unique for the list.")
    raise Exception(AttributeError, "Valid list obj needs to be provided.")
