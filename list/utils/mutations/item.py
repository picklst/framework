from datetime import datetime

from django.utils import timezone

from list.models import List, Item, ItemMedia
from media.models import Media
from poll.models import PollOption
from taxonomy.models import Tag


def create_item(o):
    if hasattr(o, "list") and List.objects.filter(id=o.list.id).exists():
        if hasattr(o, "position"):
            itemObj = Item(
                name=o.name,
                list=o.list,
            )

            if hasattr(o, "contributor") and o.contributor is not None:
                itemObj.contributor = o.contributor

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

            if hasattr(o, "mediaID") and o.mediaID is not None:
                try:
                    mediaObj = Media.objects.get(id=o.mediaID)
                    ItemMedia.objects.create(
                        item=itemObj,
                        media=mediaObj
                    )
                except Media.DoesNotExist:
                    pass

            if hasattr(o, "poll") and o.poll is not None:
                for option in o.poll.options:
                    obj = PollOption(name=option.name)
                    if option.mediaID:
                        obj.media = Media.objects.get(id=option.mediaID)
                    obj.save()
                    itemObj.pollOptions.add(obj)
                    if option.id == o.poll.answerID:
                        itemObj.correctOption = obj

            return itemObj
        raise Exception(AttributeError, "Item position required, and be unique for the list.")
    raise Exception(AttributeError, "Valid list obj needs to be provided.")


def update_item(o):
    if hasattr(o, "id"):
        try:
            item = Item.objects.get(id=o.id)
            if item.list == o.list:

                if hasattr(o, "tags") and o.tags is not None and len(o.tags):
                    item.hashTags.clear()
                    for t in o.tags:
                        tObj, cr = Tag.objects.get_or_create(
                            name=t[1:].lower()
                        )
                        item.hashTags.add(tObj.id)

                if hasattr(o, "mediaID") and o.mediaID is not None:
                    try:
                        existing = ItemMedia.objects.get(media_id=o.mediaID, item=item)
                    except ItemMedia.DoesNotExist:
                        try:
                            mediaObj = Media.objects.get(id=o.mediaID)
                            ItemMedia.objects.create(
                                item=item,
                                media=mediaObj
                            )
                        except Media.DoesNotExist:
                            pass

                if hasattr(o, "poll") and o.poll is not None:
                    # handle deletion of poll options
                    if item.pollOptions.all().count() > 0:
                        for option in item.pollOptions.all():
                            flag = 0
                            for op in o.poll.options:
                                if int(op['id']) == option.id:
                                    flag = 1
                            if flag == 0:
                                option.delete()
                    for option in o.poll.options:
                        # option already exists = handle updation
                        if option.id.isdigit() and PollOption.objects.filter(id=option.id).exists():
                            obj = PollOption.objects.get(id=option.id)
                            if option.name != obj.name:
                                obj.name = option.name
                            if option.mediaID:
                                obj.media = Media.objects.get(id=option.mediaID)
                            obj.save()
                        # option doesnt exist - handle creation
                        else:
                            obj = PollOption(name=option.name)
                            if option.mediaID:
                                obj.media = Media.objects.get(id=option.mediaID)
                            obj.save()
                            item.pollOptions.add(obj)
                        # update / add correct Option
                        if option.id == o.poll.answerID:
                            item.correctOption = obj

                if hasattr(o, "name") and o.name is not None:
                    item.name = o.name
                if hasattr(o, "comment") and o.comment is not None:
                    item.comment = o.comment
                if hasattr(o, "url") and o.url is not None:
                    item.url = o.url

                item.timestampLastEdited = timezone.now()

                item.save()

                return item
            else:
                raise Exception(ValueError, "Item list passed does not match records.")
        except Item.DoesNotExist:
            raise Exception(AttributeError, "Item does not exist.")


def delete_item(id):
    try:
        item = Item.objects.get(id=id)
        item.delete()
    except Item.DoesNotExist:
        raise Exception(AttributeError, "Item does not exist.")
