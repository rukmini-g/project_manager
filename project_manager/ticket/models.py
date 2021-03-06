from __future__ import unicode_literals

from django.db import models

from base.models import TimeStamp

TICKET_TYPE = (
    (1, "Jira Ticket"),
    (2, "Learning"),
    (3, "Training"),
    (4, "Internal Product"),
    (5, "Other"),

)


STATUS = (
    (1, "Not Started"),
    (2, "Completed"),
    (3, "In-Process"),
    (4, "Under-Review"),
)


class Ticket(TimeStamp):

    ticket_type = models.IntegerField(choices=TICKET_TYPE)
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=1000)
    due_date = models.DateField()
    status = models.IntegerField(choices=STATUS)
    assigned_to = models.ManyToManyField('auth.User')

    def __unicode__(self):
        return "{}".format(self.title)

class MileStone(TimeStamp):

    ticket = models.ForeignKey(
        'ticket.Ticket', related_name="milestones")
    comment = models.CharField(max_length=500)
    contribution = models.IntegerField(default=0)

    def __unicode__(self):
        return "{}".format(self.ticket.title)