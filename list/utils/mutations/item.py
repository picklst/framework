import uuid

from list.models import List, Position, Item


def create_item(o):
    if hasattr(o, "list") and List.objects.filter(id=o.list.id).exists():
        if hasattr(o, "position"):
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

            # if any other object is at the position, set it to null.
            # hopefully, it will be correctly put into place in other edit  @todo improve logic
            if Position.objects.filter(list=o.list, position=o.position).exists():
                exist = Position.objects.get(list=o.list, position=o.position)
                exist.position = None
                exist.save()
            # create and save position for the item in the list
            try:
                p = Position.objects.create(
                    item=itemObj,
                    list=o.list,
                    position=o.position
                )
            except Exception:
                raise Exception(AttributeError, "Failed to created position obj")
            return itemObj
        raise Exception(AttributeError, "Item position required, and be unique for the list.")
    raise Exception(AttributeError, "Valid list obj needs to be provided.")


def update_item(o):
    if hasattr(o, "key"):
        try:
            item = Item.objects.get(key=o.key)
            if item.list == o.list:
                print(o.name)
                if hasattr(o, "name") and o.name is not None:
                    item.name = o.name
                if hasattr(o, "comment") and o.comment is not None:
                    item.comment = o.comment
                if hasattr(o, "url") and o.url is not None:
                    item.url = o.url
                item.save()

                thisItem = Position.objects.get(list=item.list, item__key=o.key)
                # @todo updation of position logic needs to be optimzed improved
                if hasattr(o, "position") and o.position != thisItem.position:
                    if Position.objects.filter(list=item.list, position=o.position).exists():
                        existingItem = Position.objects.get(list=item.list, position=o.position)
                        existingItem.position = None
                        existingItem.save()
                        oldPos = thisItem.position
                        thisItem.position = o.position
                        existingItem.position = oldPos
                        thisItem.save()
                        existingItem.save()
                    else:
                        thisItem = Position.objects.get(list=item.list, item__key=o.key)
                        thisItem.position = o.position
                        thisItem.save()

                return item
            else:
                raise Exception(ValueError, "Item list passed does not match records.")
        except Item.DoesNotExist:
            raise Exception(AttributeError, "Item does not exist.")


def delete_item(o):
    if hasattr(o, "key"):
        try:
            item = Item.objects.get(key=o.key, list=o.list)
            item.delete()
        except Item.DoesNotExist:
            raise Exception(AttributeError, "Item does not exist.")
