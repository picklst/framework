import graphene
from django.db.models import Q
from graphql_jwt.decorators import login_required

from framework.graphql.inputs.user import UserCreationInput, UserUpdationInput
from framework.graphql.types import User as UserObj
from framework.graphql.utils import APIException
from framework.utils.auth import generate_username_from_email, generate_password

from user.models import User, UserSubscription


class AccountCreationResponse(
    graphene.ObjectType,
    description='Response received on account creation mutation'
):
    returning = graphene.Field(
        UserObj,
        description='User fields to be returned'
    )
    generatedPassword = graphene.String(
        description='automatically generated password, if no password was provided'
    )


class AccountUpdationResponse(
    graphene.ObjectType,
    description='Response received on account updation mutation'
):
    returning = graphene.Field(
        UserObj,
        description='User fields to be returned'
    )


class AccountCreate(
    graphene.Mutation,
    description='Creates an user account'
):
    class Arguments:
        input = graphene.Argument(
            UserCreationInput,
            required=True,
            description='Fields accepted to create an user account'
        )

    Output = AccountCreationResponse

    @staticmethod
    def mutate(info, input=None):
        try:
            user = User.objects.get(Q(username=input.username) | Q(email=input.email))
            if user.username == input.username:
                raise APIException('Username already taken.', code='USERNAME_TAKEN')
            raise APIException('An account with this email already exist.', code='EMAIL_IN_USE')
        except User.DoesNotExist:
            username = input.username | generate_username_from_email(input.email)
            password = input.password | generate_password()
            user = User.objects.create(
                first_name=input.firstName | username,
                last_name=input.lastName | '',
                email=input.email,
                username=username,
            )
            user.set_password(password)
            user.save()
            return AccountCreationResponse(
                returning=user,
                generatedPassword=password if input.password is None else None,
                status=True
            )


class AccountUpdate(
    graphene.Mutation,
    description='Updates the account of the logged-in user'
):
    class Arguments:
        input = graphene.Argument(
            UserUpdationInput,
            required=True,
            description='Fields accepted for updation of the user'
        )

    Output = AccountUpdationResponse

    @login_required
    def mutate(self, info, input):
        try:
            if input.username == info.context.user.username:
                user = info.context.user
                if hasattr(input, "firstName") and input.firstName is not None:
                    user.first_name = input.firstName
                if hasattr(input, "lastName") and input.lastName is not None:
                    user.last_name = input.lastName
                if hasattr(input, "bio") and input.bio is not None:
                    user.bio = input.bio
                if hasattr(input, "url") and input.url is not None:
                    user.url = input.url
                user.save()
                return AccountUpdationResponse(
                    returning=user,
                )
            else:
                raise APIException('You can only update your own profile using this API', code='USER_MISMATCH')
        except User.DoesNotExist:
            raise APIException('User matching email does not exist', code='DOES_NOT_EXIST')


class FollowUser(graphene.Mutation):
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
                UserSubscription.objects.create(
                    user=user,
                    subscriber=info.context.user
                )
                return True
            except User.DoesNotExist:
                raise APIException('User does not exist.', code='USER_DOES_NOT_EXIST')


class UnfollowUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    Output = graphene.Boolean

    @login_required
    def mutate(self, info, username):
        if UserSubscription.objects.filter(user__username=username, subscriber=info.context.user).exists():
            UserSubscription.objects.get(
                user__username=username,
                subscriber=info.context.user
            ).delete()
            return True
        else:
            raise APIException('User is not being followed.', code='NOT_FOLLOWING_USER')


class UserMutations(graphene.ObjectType):
    accountCreate = AccountCreate.Field()
    accountUpdate = AccountUpdate.Field()
    followUser = FollowUser.Field()
    unfollowUser = UnfollowUser.Field()


__all__ = ['UserMutations']
