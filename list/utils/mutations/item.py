import uuid

from list.models import List, Item, ItemMedia
from media.models import Media
from taxonomy.models import Tag


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

            if hasattr(o, "tags") and o.tags is not None and len(o.tags):
                itemObj.hashTags.clear()
                for t in o.tags:
                    tObj, cr = Tag.objects.get_or_create(
                        name=t[1:].lower()
                    )
                    itemObj.hashTags.add(tObj.id)

            if hasattr(o, "comment") and o.comment is not None:
                itemObj.comment = o.comment
            if hasattr(o, "url") and o.url is not None:
                itemObj.url = o.url

            # save and the obj to db
            itemObj.save()

            return itemObj
        raise Exception(AttributeError, "Item position required, and be unique for the list.")
    raise Exception(AttributeError, "Valid list obj needs to be provided.")


def update_item(o):
    if hasattr(o, "key"):
        try:
            item = Item.objects.get(key=o.key)
            if item.list == o.list:

                if hasattr(o, "tags") and o.tags is not None and len(o.tags):
                    item.hashTags.clear()
                    for t in o.tags:
                        tObj, cr = Tag.objects.get_or_create(
                            name=t[1:].lower()
                        )
                        item.hashTags.add(tObj.id)

                if hasattr(o, "media") and o.media is not None:
                    try:
                        mediaObj = Media.objects.get(key=o.media)
                        ItemMedia.objects.create(
                            item=item,
                            media=mediaObj
                        )
                    except Media.DoesNotExist:
                        pass

                if hasattr(o, "name") and o.name is not None:
                    item.name = o.name
                if hasattr(o, "comment") and o.comment is not None:
                    item.comment = o.comment
                if hasattr(o, "url") and o.url is not None:
                    item.url = o.url
                item.save()

                return item
            else:
                raise Exception(ValueError, "Item list passed does not match records.")
        except Item.DoesNotExist:
            raise Exception(AttributeError, "Item does not exist.")


def delete_item(key):
    try:
        item = Item.objects.get(key=key)
        item.delete()
    except Item.DoesNotExist:
        raise Exception(AttributeError, "Item does not exist.")
