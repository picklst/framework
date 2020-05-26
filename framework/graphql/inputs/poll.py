import graphene


class OptionInput(graphene.InputObjectType):
    id = graphene.String(required=True)
    name = graphene.String(required=True)
    mediaID = graphene.String()


class PollInput(graphene.InputObjectType):
    answerID = graphene.String()
    options = graphene.List(
        OptionInput,
        required=True,
    )
