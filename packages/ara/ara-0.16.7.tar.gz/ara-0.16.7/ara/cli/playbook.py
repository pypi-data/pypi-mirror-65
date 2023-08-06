#  Copyright (c) 2018 Red Hat, Inc.
#
#  This file is part of ARA Records Ansible.
#
#  ARA is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  ARA is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with ARA.  If not, see <http://www.gnu.org/licenses/>.

import logging

from ara import models
from ara.models import db
from ara.fields import Field
from cliff.lister import Lister
from cliff.show import ShowOne
from cliff.command import Command

LIST_FIELDS = (
    Field('ID'),
    Field('Path'),
    Field('Time Start'),
    Field('Duration'),
    Field('Complete'),
    Field('Ansible Version'),
)

SHOW_FIELDS = (
    Field('ID'),
    Field('Path'),
    Field('Time Start'),
    Field('Time End'),
    Field('Duration'),
    Field('Complete'),
    Field('Ansible Version'),
    Field('Parameters', 'options',
          template='{{ value | to_nice_json | safe }}')
)


class PlaybookList(Lister):
    """ Returns a list of playbooks """
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(PlaybookList, self).get_parser(prog_name)
        parser.add_argument(
            '--incomplete', '-I',
            action='store_true',
            help='Only show incomplete playbook runs',
        )
        parser.add_argument(
            '--complete', '-C',
            action='store_true',
            help='Only show complete playbook runs',
        )
        return parser

    def take_action(self, args):
        playbooks = models.Playbook.query.order_by(models.Playbook.time_start)

        if args.incomplete:
            playbooks = playbooks.filter_by(complete=False)
        if args.complete:
            playbooks = playbooks.filter_by(complete=True)

        return [[field.name for field in LIST_FIELDS],
                [[field(playbook) for field in LIST_FIELDS]
                 for playbook in playbooks]]


class PlaybookShow(ShowOne):
    """ Show details of a playbook """
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(PlaybookShow, self).get_parser(prog_name)
        parser.add_argument(
            'playbook_id',
            metavar='<playbook-id>',
            help='Playbook to show',
        )
        return parser

    def take_action(self, args):
        playbook = models.Playbook.query.get(args.playbook_id)
        if playbook is None:
            raise RuntimeError('Playbook %s could not be found' %
                               args.playbook_id)
        return [[field.name for field in SHOW_FIELDS],
                [field(playbook) for field in SHOW_FIELDS]]


class PlaybookDelete(Command):
    """ Delete playbooks from the database. """
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(PlaybookDelete, self).get_parser(prog_name)
        parser.add_argument(
            '--ignore-errors', '-i',
            action='store_true',
            help='Do not exit if a playbook cannot be found')
        parser.add_argument(
            '--incomplete', '-I',
            action='store_true',
            help='Delete all incomplete playbook runs',
        )
        parser.add_argument(
            'playbook_id',
            nargs='*',
            metavar='<playbook-id>',
            help='Playbook(s) to delete',
        )
        return parser

    def take_action(self, args):
        if not args.playbook_id and not args.incomplete:
            raise RuntimeError('Nothing to delete')

        if args.playbook_id and args.incomplete:
            raise RuntimeError('You may not use --incomplete with '
                               'a list of playbooks')

        if args.incomplete:
            pids = (playbook.id for playbook in
                    models.Playbook.query.filter_by(complete=False))
        else:
            pids = []
            for pid in args.playbook_id:
                res = models.Playbook.query.get(pid)
                if res is None:
                    if args.ignore_errors:
                        self.log.warning('Playbook %s does not exist '
                                         '(ignoring)' % pid)
                    else:
                        raise RuntimeError('Playbook %s does not exist' % pid)
                else:
                    pids.append(pid)

        for pid in pids:
            self.log.warning('deleting playbook %s', pid)
            playbook = models.Playbook.query.get(pid)
            db.session.delete(playbook)

        db.session.commit()
