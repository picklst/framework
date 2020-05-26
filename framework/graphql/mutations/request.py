import graphene
from django.db.models import Q
from graphql_jwt.decorators import login_required

from framework.graphql.utils import APIException
from list.models import List, Position
from list.utils.decorators import list_accepts_entries
from list.utils.mutations.item import create_item
from list.utils.mutations.list import insert_at_position
from log.models import ItemChangeLog
from request.models import FollowUserRequest, ListRequest, ListEntry
from user.models import UserSubscription, User

from framework.graphql.inputs import ItemInput, ListSelectInput


class RequestFollowUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    Output = graphene.Boolean

    @login_required
    def mutate(self, info, username):
        if username == info.context.user.username:
            raise APIException('User cannot follow self.', code='CANNOT_FOLLOW_SELF')
        if UserSubscription.objects.filter(user__username=username, subscriber=info.context.user).exists():
            raise APIException('Already following User', code='ALREADY_FOLLOWING_USER')
        else:
            try:
                user = User.objects.get(username=username)
                if not User.isProfilePrivate:
                    raise APIException('Respondent profile is public, directly follow the user.', code='PUBLIC_PROFILE')
                if FollowUserRequest.objects.get(requester=info.context.user, respondent=user).exists():
                    raise APIException('Request already sent to the user.', code='ALREADY_REQUESTED')
                FollowUserRequest.objects.create(
                    requester=info.context.user,
                    respondent=user
                )
                return True
            except User.DoesNotExist:
                raise APIException('User does not exist.', code='USER_DOES_NOT_EXIST')


class RequestList(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        subject = graphene.String()

    Output = graphene.Boolean

    @login_required
    def mutate(self, info, username, subject=''):
        if username == info.context.user.username:
            raise APIException('User cannot request self.', code='CANNOT_REQUEST_SELF')
        else:
            try:
                user = User.objects.get(username=username)
                if not UserSubscription.objects.filter(user=user, subscriber=info.context.user).exists():
                    raise APIException('User can only request lists from people following.', code='NOT_FOLLOWING')
                ListRequest.objects.create(
                    requester=info.context.user,
                    respondent=user,
                    subject=subject
                )
                return True
            except User.DoesNotExist:
                raise APIException('User does not exist.', code='USER_DOES_NOT_EXIST')


class SubmitListEntry(
    graphene.Mutation,
    description='Submit a item entry for a list which is accepting entries, subject to approval.'
):
    class Arguments:
        object = graphene.Argument(
            ItemInput,
            required=True,
            description='Item object'
        )
        list = ListSelectInput()
        position = graphene.Int(
            required=False,
            description='Requested position in the list for the submitted entry be added'
        )

    Output = graphene.Boolean

    @login_required
    @list_accepts_entries
    def mutate(self, info, list, object, position=None):
        lists = List.objects.filter((Q(slug=list.slug) | Q(id=list.id)) & Q(isActive=True))
        if lists.count() == 1:
            object.list = lists.first()
            object.contributor = info.context.user

            # create an item (normally like in ItemCreate API)
            obj = create_item(object)
            ItemChangeLog.objects.create(
                user=info.context.user,
                item=obj
            )
            # we dont insert it into the list, because we wait for approval
            ListEntry.objects.create(
                list=obj.list,
                item=obj,
                contributor=info.context.user,
                positionRequested=position,
            )
            return True
        else:
            raise APIException("Invalid list passed", code='LIST_NOT_FOUND')


class ReviewListEntry(
    graphene.Mutation,
    description='Accept or reject item entries received for the list, using their respective IDs'
):
    class Arguments:
        isApproved = graphene.Boolean(
            required=True,
            description='Whether to accept or reject the entry. If entry is rejected, it is also deleted.'
        )
        entryID = graphene.String(
            required=True,
            description='ID of the ListEntry'
        )
        position = graphene.Int(
            required=False,
            description='The list position at which the entry item should be inserted if approved.'
        )

    Output = graphene.Boolean

    @login_required
    def mutate(self, info, isApproved, entryID, position=None):
        try:
            entry = ListEntry.objects.get(id=entryID)
            if entry.position is None:
                if isApproved:
                    # if position is none, add item at the end
                    if position is None:
                        count = Position.objects.filter(list=entry.list).count()
                        position = count + 1

                    # Insert item at position
                    pObj = insert_at_position(entry.item, position)

                    # update ListEntry Obj
                    entry.approver = info.context.user
                    entry.position = pObj
                    entry.save()
                    return True
                # if rejected (i.e. isApproved=False), delete the entry
                else:
                    entry.item.delete()
                    return True
            else:
                raise APIException('Entry already approved', code='ALREADY_APPROVED')
        except ListEntry.DoesNotExist:
            raise APIException('Entry not found', code='ENTRY_NOT_FOUND')


class RequestMutations(graphene.ObjectType):
    requestFollowUser = RequestFollowUser.Field()
    requestList = RequestList.Field()
    listEntrySubmit = SubmitListEntry.Field()
    listEntryReview = ReviewListEntry.Field()
