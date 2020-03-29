import graphene
from django.db.models import Q
from graphql_jwt.decorators import login_required

from user.models import User
from framework.utils.auth import generate_username_from_email, generate_password
from framework.utils.graphql import APIException


class UserRegistrationObj(graphene.ObjectType):
    username = graphene.String()
    status = graphene.Boolean()


class RegisterUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=False)
        username = graphene.String(required=False)
        firstName = graphene.String(required=False)
        lastName = graphene.String(required=False)

    Output = UserRegistrationObj

    def mutate(self, info, email, password=None, username=None, firstName=None, lastName=None):
        try:
            user = User.objects.get(Q(username=username) | Q(email=email))
            if user.username == username:
                raise APIException('Username already taken.', code='USERNAME_TAKEN')
            raise APIException('An account with this email already exist.', code='EMAIL_IN_USE')
        except User.DoesNotExist:
            name = username
            if name is None:
                name = generate_username_from_email(email)
            pwd = password
            if password is None:
                pwd = generate_password()
            fn = firstName
            if fn is None:
                fn = name
            user = User.objects.create(
                first_name=fn,
                last_name=lastName,
                email=email,
                username=name,
            )
            user.set_password(pwd)
            user.save()
            return UserRegistrationObj(
                username=name,
                status=True
            )


class DeleteUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)

    Output = graphene.Boolean

    @login_required
    def mutate(self, info, email):
        try:
            user = User.objects.get(email=email)
            # A user can either delete his own account, or else should be a superuser
            if user == info.context.user or info.context.user.is_superuser:
                user.delete()
                return True
            else:
                raise APIException('You do not have the permission to perform this action.', code='FORBIDDEN')
        except User.DoesNotExist:
            raise APIException('User matching email does not exist', code='DOES_NOT_EXIST')


class Mutation(object):
    registerUser = RegisterUser.Field()
    deleteUser = DeleteUser.Field()
