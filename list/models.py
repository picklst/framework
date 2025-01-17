from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver

from framework.utils.cornflakes.decorators import model_config
from framework.utils.cornflakes.fields import ShadedIDField
from media.fields import MediaField
from media.models import Media
from media.storages import ListCoverStorage
from poll.models import PollOption
from taxonomy.models import Topic, Tag

User = settings.AUTH_USER_MODEL


@model_config()
class List(models.Model):
    # unsigned INT64, auto incremented, Primary Key
    id = ShadedIDField(primary_key=True, null=False)

    # varchar(127), unique, url-friendly slug for the list based on `name` or user's choice
    # publicly exposed to uniquely identify a list
    slug = models.SlugField(
        max_length=127,
        unique=True,
        verbose_name='Slug'
    )

    # foreign key to creator / owner of the list
    curator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,   # a list without its creator/owner is deleted
        verbose_name='Curator',
    )
    # foreign key to the topic of the list, as set by the user
    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,  # a list's topic is set to null, if the topic it belong is deleted
        null=True,
        blank=True
    )

    firstItem = models.ForeignKey(
        'Item',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='first_item'
    )
    # m2m relation to tags associated with this list
    hashTags = models.ManyToManyField(Tag, blank=True, db_table='list_tag')
    # m2m relations to items belonging to this list, referenced through the position table
    items = models.ManyToManyField('Item', through='Position', through_fields=('list', 'item'), related_name='item_lists')

    # boolean, true when the listing is active, set to false when listing is taken down, user acc. deactivated etc.
    isActive = models.BooleanField(default=True)
    # boolean, if set to true, only the curator and collaborators (if any) of this list will be able to view it
    isPrivate = models.BooleanField(default=False)

    # boolean, if set to true the items in this list will be displayed rank-wise
    isRanked = models.BooleanField(default=False)
    # boolean, if set to true, the items in this list will be always ranked as the curator had set,
    # on default, the rank of an items shall change based on votes>rating>curator algorithm.
    forceCuratorRanking = models.BooleanField(default=False)

    # boolean, whether the list is votable, i.e an item in this list can be voted for.
    isVotable = models.BooleanField(default=False)
    # boolean, whether the voting should be private.
    # if set to true, voter's choice is invisible for the curator / collaborator, and the public
    # however, the curator / public may still maybe able to view who all voted
    areVotesPrivate = models.BooleanField(default=False)
    # boolean, whether multiple items from the list can be voted upon.
    canVoteMultipleItems = models.BooleanField(default=False)

    # boolean, whether the list items are ratable, i.e if user can rate different items in this list
    isRateable = models.BooleanField(default=False)
    # boolean, whether the rating should be private.
    # if set to true, rater's rating is invisible for the curator / collaborator, and the public
    # however, the curator / public may still maybe able to view who all rated
    areRatingsPrivate = models.BooleanField(default=False)

    # boolean, whether others can suggest items to this list
    acceptEntries = models.BooleanField(default=False)

    # name of the list, supports upto 255 chars
    name = models.CharField(
        max_length=255,
        verbose_name='Name'
    )
    # description of the list, supports upto 511 chars
    description = models.CharField(
        max_length=511,
        default='',
        blank=True,
        verbose_name='Description'
    )
    # cover image for the list
    cover = MediaField(
        storage=ListCoverStorage(),
        max_size=1024 * 1024 * 8,
        content_types=[
            'image/png', 'image/jpeg', 'image/gif', 'image/bmp', 'image/webp',
        ],
        null=True, blank=True
    )

    timestampCreated = models.DateTimeField(auto_now=True)

    timestampLastEdited = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'list'
        verbose_name_plural = "Lists"
        verbose_name = "List"

    def __str__(self):
        return self.slug


# deletes the cover image from storage if the list is deleted
@receiver(post_delete, sender=List)
def submission_delete(sender, instance, **kwargs):
    instance.cover.delete(save=False)


class Collaborator(models.Model):
    # unsigned INT64, auto incremented, Primary Key
    # always kept secret
    id = models.BigAutoField(primary_key=True)
    # foreign key to the list where the user is a collaborator
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    # foreign key to the user who is the collaborator of this list
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # timestamp of when the user was added as collaborator
    timestampCreated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['list', 'user']]
        db_table = 'list_collaborator'
        verbose_name_plural = "Collaborators"
        verbose_name = "Collaborator"

    def __str__(self):
        return str(self.id)


@model_config()
class Item(models.Model):
    # unsigned INT64, auto incremented, Primary Key
    id = ShadedIDField(primary_key=True, null=False)

    # @todo creator of item through separate table maybe ??
    # foreign key to the list the item belongs to
    list = models.ForeignKey(
        List,
        on_delete=models.CASCADE,  # items belonging to a list are deleted if the list itself is deleted
        verbose_name='List'
    )

    # foreign key to the item from which this item was derived from
    source = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Source Item'
    )

    # contributor of this item
    contributor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='item_contributor'
    )

    # m2m relation to tags associated with this item
    hashTags = models.ManyToManyField(Tag, db_table='item_tag', blank=True)
    # m2m relation to users mentioned in this item
    mentions = models.ManyToManyField(User, db_table='item_mention', blank=True)
    # poll / question options
    pollOptions = models.ManyToManyField(PollOption, blank=True, db_table='item_poll_option')
    # correct option in case poll is used as a question / quiz
    correctOption = models.ForeignKey(
        PollOption,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='correct_option'
    )

    # varchar(127), name of the listed item
    name = models.CharField(max_length=127, verbose_name='Name')
    # varchar(255), comment or description about the listed item
    comment = models.CharField(max_length=255, default='', blank=True, verbose_name='Comment')
    # varchar(255), external url referenced in this item
    url = models.CharField(max_length=255, default='', blank=True, verbose_name='URL')

    timestampCreated = models.DateTimeField(auto_now=True)

    timestampLastEdited = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'item'
        verbose_name_plural = "Items"
        verbose_name = "Item"

    def __str__(self):
        return str(self.id)


class Position(models.Model):
    # foreign key to the item whose position is being defined
    item = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True, related_name='position_item')
    # foreign key to the list where the item belongs, and in which the position is to be defined
    # could have been accessed through item.list, but to avoid join and easy querying
    list = models.ForeignKey(List, on_delete=models.CASCADE)

    next = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, related_name='next_item')

    class Meta:
        db_table = 'item_position'
        verbose_name_plural = "List-Item Positions"
        verbose_name = "List-Item Position"

    def __str__(self):
        return str(self.item)


@model_config()
class Vote(models.Model):
    # unsigned INT64, auto incremented, Primary Key
    id = ShadedIDField(primary_key=True, null=False)
    # foreign key to the item which is being voted for
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    # foreign key to the user who is voting
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    # boolean, whether the vote is a down vote
    isNegative = models.BooleanField(default=False)
    # timestamp of the vote
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['item', 'voter']]
        db_table = 'item_vote'
        verbose_name_plural = "Item-User Vote"
        verbose_name = "Item-User Vote"

    def __str__(self):
        return str(self.id)


@model_config()
class Rating(models.Model):
    # unsigned INT64, auto incremented, Primary Key
    id = ShadedIDField(primary_key=True, null=False)
    # foreign key to the item which is being rated
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    # foreign key to the user who has given the rating
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    # integer representing rating from 0 to 100
    rating = models.PositiveSmallIntegerField()
    # timestamp of the rating
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['item', 'reviewer']]
        db_table = 'item_rating'
        verbose_name_plural = "Item-User Ratings"
        verbose_name = "Item-User Rating"

    def __str__(self):
        return str(self.id)


@model_config()
class ListVote(models.Model):
    # unsigned INT64, auto incremented, Primary Key
    id = ShadedIDField(primary_key=True, null=False)
    # foreign key to the user who is voting
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    # foreign key to the list whose items are being voted upon
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    # foreign key to the item which has been voted for
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    # timestamp of the vote
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['list', 'voter']]
        db_table = 'list_item_vote'
        verbose_name_plural = "List Votes"
        verbose_name = "List Vote"

    def __str__(self):
        return str(self.id)


class ItemMedia(models.Model):
    # foreign key to the media obj which is being linked in the referenced item
    # a media obj shall in all case be part of a single item, hence it will have a unique entry in this table
    media = models.ForeignKey(Media, on_delete=models.CASCADE, unique=True, primary_key=True)
    # foreign key to the item obj part of which the referenced media obj is part of
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        # implies an item cannot have more than media linked at any given time.
        unique_together = [['media', 'item']]
        db_table = 'item_media'
        verbose_name_plural = "Item Media"
        verbose_name = "Item Media"

    def __str__(self):
        return str(self.media)


# function to delete the connected media obj if the item it is part of is deleted
# when a item is deleted, all its ItemMedia objs are also deleted due to models.CASCADE property
# now, when ItemMedia obj is deleted, the associated media can also be safely deleted.
@receiver(post_delete, sender=ItemMedia)
def submission_delete(sender, instance, **kwargs):
    instance.media.asset.delete(save=False)


__all__ = [
    'List',
    'Collaborator',
    'Item',
    'Position',
    'Vote',
    'Rating',
    'ItemMedia'
]
