import graphene
from graphql_jwt.decorators import login_required


class PasswordChange(
    graphene.Mutation,
    description='Change the password of the logged-in user'
):
    class Arguments:
        oldPassword = graphene.String(
            required=True,
            description='Old password of the user'
        )
        newPassword = graphene.String(
            required=True,
            description='New password of the user'
        )

    Output = graphene.Boolean

    @login_required
    def mutate(self, info, oldPassword, newPassword):
        # @todo implement API
        return False


class RequestPasswordReset(
    graphene.Mutation,
    description='Sends an email with the account password modification link'
):
    class Arguments:
        email = graphene.String(
            required=True,
            description='Email of the user'
        )

    Output = graphene.Boolean

    @staticmethod
    def mutate(self, info, email):
        # @todo implement API
        return False


class RequestResendEmailConfirmation(
    graphene. Mutation,
    description='Request email change of the logged-in user, a confirmation email is send to the new email'
):
    class Arguments:
        pass

    Output = graphene.Boolean

    @login_required
    def mutate(self, info):
        # @todo implement API
        return False


class RequestEmailChange(
    graphene. Mutation,
    description='Request email change of the logged-in user, a confirmation email is send to the new email'
):
    class Arguments:
        newEmail = graphene.String(
            required=True,
            description='New email address of the user'
        )
        password = graphene.String(
            required=True,
            description='Password of the user'
        )

    Output = graphene.Boolean

    @login_required
    def mutate(self, info, newEmail, password):
        # @todo implement API
        return False


class RequestAccountDeletion(
    graphene.Mutation,
    description='Sends an email with account deletion link to the logged-in user'
):
    class Arguments:
        password = graphene.String(
            required=True,
            description='Password of the user'
        )

    Output = graphene.Boolean

    @login_required
    def mutate(self, info, password):
        # @todo implement API
        return False


class ConfirmPasswordReset(
    graphene.Mutation,
    description='Confirm the password reset request, and update the user password. '
):
    class Arguments:
        confirmationToken = graphene.String(
            required=True,
            description='A one-time token required to reset the password sent to the user email.'
        )
        newPassword = graphene.String(
            required=True,
            description='New password to be set.'
        )

    Output = graphene.Boolean

    @staticmethod
    def mutate(self, info, confirmationToken, newPassword):
        # @todo implement API
        return False


class ConfirmEmailOwnership(
    graphene.Mutation,
    description='Confirm the ownership of the email by the user through a confirmation token sent to it. '
                'Used to confirm email on sign-up.'
                'Instead, if it arrived from a email change request, updates the records of the user with this email,.'
):
    class Arguments:
        confirmationToken = graphene.String(
            required=True,
            description='A one-time token required to change the email.'
        )

    Output = graphene.Boolean

    @staticmethod
    def mutate(self, info, password):
        # @todo implement API
        return False


class ConfirmAccountDeletion(
    graphene.Mutation,
    description='Confirm the account deletion of the user'
):
    class Arguments:
        confirmationToken = graphene.String(
            required=True,
            description='A confirmation token sent by email using requestAccountDeletion mutation, '
                        'is required to remove account.'
        )

    Output = graphene.Boolean

    @staticmethod
    def mutate(self, info, confirmationToken):
        # @todo implement API
        # try:
        #     user = info.context.user
        #     user.delete()
        #     return True
        # except User.DoesNotExist:
        #     raise APIException('User matching email does not exist', code='DOES_NOT_EXIST')
        return False


class AuthorizedMutations(graphene.ObjectType):
    passwordChange = PasswordChange.Field()
    requestResendEmailConfirmation = RequestResendEmailConfirmation.Field()
    requestPasswordReset = RequestPasswordReset.Field()
    requestEmailChange = RequestEmailChange.Field()
    requestAccountDeletion = RequestAccountDeletion.Field()
    confirmPasswordReset = ConfirmPasswordReset.Field()
    confirmEmailOwnership = ConfirmEmailOwnership.Field()
    confirmAccountDeletion = ConfirmAccountDeletion.Field()


__all__ = ['AuthorizedMutations']
