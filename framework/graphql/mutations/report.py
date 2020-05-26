import graphene
from django.db.models import Q

from framework.graphql.inputs import ListSelectInput
from list.models import List
from log.models import ListReport, UserReport
from user.models import User


class ReportUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        subject = graphene.String(required=True)
        remarks = graphene.String()

    Output = graphene.Boolean

    @staticmethod
    def mutate(self, info, username, subject, remarks=''):
        userObj = User.objects.get(username=username)
        UserReport.objects.create(
            user=userObj,
            subject=subject,
            remarks=remarks,
        )
        return True


class ReportList(graphene.Mutation):
    class Arguments:
        list = ListSelectInput()
        subject = graphene.String(required=True)
        remarks = graphene.String()

    Output = graphene.Boolean

    @staticmethod
    def mutate(self, info, list, subject, remarks=''):
        listObj = List.objects.get(Q(slug=list.slug) | Q(id=list.id))
        ListReport.objects.create(
            list=listObj,
            subject=subject,
            remarks=remarks,
        )
        return True


class ReportMutations(graphene.ObjectType):
    reportUser = ReportUser.Field()
    reportList = ReportList.Field()
