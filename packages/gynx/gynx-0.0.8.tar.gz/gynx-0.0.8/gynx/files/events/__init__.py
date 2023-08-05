import logging

ACTIONS = {
    'CREATE': ['CREATING', 'CREATED'],
    'DELETE': ['DELETING', 'DELETED'],
    'MODIFY': ['MODIFYING', 'MODIFIED'],
    'MOVE': ['MOVING', 'MOVED'],
}


class GynxEvent:
    '''
    Standard event class for all sync operations
    '''

    def __init__(
        self, action, ftype, path, dest=None, remote_id=None, parent_id=None,
        target='remote'
    ):
        self.action = action
        self.ftype = ftype
        self.path = path
        self.dest = dest
        self.remote_id = remote_id
        self.parent_id = parent_id
        self.logger = logging.getLogger('gynx.files.events')

    def __str__(self):
        return '%s %s %s in local. %s remote' % (
            ACTIONS[self.action.upper()][1].title(),
            self.ftype.lower(),
            self.path if self.action.upper() != 'MOVE' else 'from %s to %s' % (
                self.path, self.dest
            ),
            ACTIONS[self.action.upper()][0].title()
        )
