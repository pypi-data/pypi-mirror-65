from tinydb_base.getSet import GetSet

class Settings(GetSet):

    def __init__(self, salt, pw, file='ds.json', table=__name__):
        super().__init__(salt, pw, file=file, table=table)
        self.defaultRows({
            'foo': 'bar'
        })
