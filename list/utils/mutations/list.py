import uuid

from django.template.defaultfilters import slugify

from list.utils.mutations.item import create_item, update_item, delete_item
from list.models import List
from user.models import User


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
            for i in o.items:
                i.list = listObj
                create_item(i)
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
        updated_items = []
        for i in o.items:
            i.list = listObj
            if listObj.items.filter(key=i.key).exists():
                update_item(i)
                updated_items.append(i.key)
            else:
                create_item(i)
                updated_items.append(i.key)
        for i in listObj.items.exclude(key__in=updated_items):
            i.list = listObj
            delete_item(i)
    listObj.save()
    return listObj