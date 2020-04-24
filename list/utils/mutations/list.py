import uuid
from datetime import datetime

from django.template.defaultfilters import slugify

from framework.graphql.utils import APIException
from list.utils.mutations.item import create_item, update_item, delete_item
from list.models import List, Position
from user.models import User


def exclude_position(item):
    try:
        deletedItemPos = Position.objects.get(item=item)
        try:
            prevItemPos = Position.objects.get(next=item)
            prevItemPos.next = deletedItemPos.next
            prevItemPos.save()
        # if the first element is to be deleted
        except Position.DoesNotExist:
            listObj = item.list
            listObj.firstItem = deletedItemPos.next
            listObj.save()
    except Position.DoesNotExist:
        raise(AttributeError, 'Item position cannot be determined')


def insert_at_position(i, pos):
    listObj = i.list
    if pos == 1:
        Position.objects.create(
            item=i,
            list=i.list,
            next=listObj.firstItem,
        )
        listObj.firstItem = i
        listObj.save()
    else:
        counter = 1
        try:
            itemPos = Position.objects.get(list=listObj, item=listObj.firstItem)
            while counter + 1 != pos:
                itemPos = Position.objects.get(list=listObj, item=itemPos.next)
                counter += 1
            prevPos = itemPos
            nextItem = itemPos.next
            Position.objects.create(
                item=i,
                list=i.list,
                next=nextItem,
            )
            prevPos.next = i
            prevPos.save()

        except Position.DoesNotExist:
            raise APIException("Position of items of this list cannot be determined.", code='LIST_CORRUPTED')


def get_position(listObj, itemObj):
    counter = 0
    ItemPos = None
    while ItemPos is None or ItemPos.next is not None:
        if ItemPos is None:
            ItemPos = Position.objects.get(list=listObj, item=listObj.firstItem)
        else:
            ItemPos = Position.objects.get(list=listObj, item=ItemPos.next)
        if itemObj == ItemPos.item:
            return counter + 1
        counter += 1
    return -1


def move_item_up(i):
    listObj = i.list
    itemPos = Position.objects.get(list=listObj, item=i)

    if listObj.firstItem != itemPos.item:
        nextPos = Position.objects.get(list=listObj, next=i)
        nextPos.next = itemPos.next
        nextPos.save()

        if listObj.firstItem == nextPos.item:
            listObj.firstItem = itemPos.item
            listObj.save()
        else:
            prevPos = Position.objects.get(list=listObj, next=nextPos.item)
            prevPos.next = itemPos.item
            prevPos.save()

        itemPos.next = nextPos.item
        itemPos.save()
        return True
    else:
        raise APIException("Cannot move item further upwards.", code='CANNOT_MOVE_UP')


def move_item_down(i):
    listObj = i.list
    itemPos = Position.objects.get(list=listObj, item=i)

    if itemPos.next is not None:
        newPrevPos = Position.objects.get(list=listObj, item=itemPos.next)
        if listObj.firstItem == itemPos.item:
            listObj.firstItem = newPrevPos.item
            listObj.save()
        else:
            oldPrevPos = Position.objects.get(list=listObj, next=itemPos.item)
            oldPrevPos.next = newPrevPos.item
            oldPrevPos.save()

        itemPos.next = newPrevPos.next
        itemPos.save()

        newPrevPos.next = itemPos.item
        newPrevPos.save()
        return True
    else:
        raise APIException("Cannot move item further down.", code='CANNOT_MOVE_DOWN')


def move_to_position(i, pos):
    listObj = i.list
    currPos = get_position(listObj, i)
    if currPos != pos:
        move_item_up(i) if currPos > pos else move_item_down(i)


def save_positions(i):
    # sorting the given list based on the positions provided
    items = sorted(i, key=lambda x: x[0])
    index = 0

    while index < len(items):
        itemObj = items[index][1]
        # Computing the next item in the list
        if index + 1 < len(items):
            nextItem = items[index + 1][1]
        else:
            nextItem = None
        try:
            # checking if the position obj for the item already exists
            # if exists, they need to be updated.
            pos = Position.objects.get(item=itemObj)
            if pos.list == itemObj.list:
                if pos.next != nextItem:
                    pos.next = nextItem
                    pos.save()
            else:
                raise Exception(ValueError, 'Mismatch between list of provided item vs the list in records.')
        # if position obj doesnt exist for the item, we create one
        except Position.DoesNotExist:
            Position.objects.create(
                item=itemObj,
                list=itemObj.list,
                next=nextItem,
            )
        index += 1
    return items[0][1]


def create_list(o):
    # A valid user obj must be passed along in order to create a list, and the user must be a active user.
    if hasattr(o, "user") and User.objects.filter(is_active=True, id=o.user.id).exists():
        # obtain the slug, slugify the list's name if slug is not provided in the obj
        slug = o.slug if hasattr(o, "slug") and o.slug is not None else slugify(o.name)
        # check if the slug already exits, append an uuid if exists to make it unique
        while List.objects.filter(slug=slug).exists():
            slug = slug + '-' + uuid.uuid4().hex[:8]

        listObj = List(
            name=o.name,
            slug=slug,
            curator=o.user,
        )
        if hasattr(o, "description") and o.description is not None:
            listObj.description = o.description
        # add list properties to the newly created obj, if provided
        if o.properties:
            for p in o.properties.items():
                setattr(listObj, p[0], p[1])

        # save and write the obj to db
        listObj.save()

        # create items belonging to the list, if provided
        if o.items:
            items = []
            for i in o.items:
                i.list = listObj
                itemCr = create_item(i)
                items.append((i.position, itemCr))
            firstItem = save_positions(items)
            listObj.firstItem = firstItem
        listObj.save()
        return listObj
    raise Exception(AttributeError, "Valid user obj must be provided to create list.")


def update_list(o):
    listObj = List.objects.get(slug=o.slug)

    listObj.name = o.name
    listObj.description = o.description

    if o.properties:
        for p in o.properties.items():
            setattr(listObj, p[0], p[1])

    if o.items:
        items = []
        updated_item_keys = []
        for i in o.items:
            i.list = listObj
            if listObj.items.filter(key=i.key).exists():
                itemUp = update_item(i)
                updated_item_keys.append(i.key)
                items.append((i.position, itemUp))
            else:
                itemCr = create_item(i)
                updated_item_keys.append(i.key)
                items.append((i.position, itemCr))
        for i in listObj.items.exclude(key__in=updated_item_keys):
            i.list = listObj
            exclude_position(i)
            delete_item(i.key)
        firstItem = save_positions(items)
        listObj.firstItem = firstItem

    listObj.save()
    return listObj
