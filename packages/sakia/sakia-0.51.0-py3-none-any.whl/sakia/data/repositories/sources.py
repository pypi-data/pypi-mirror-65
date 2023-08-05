import attr

from ..entities import Source


@attr.s(frozen=True)
class SourcesRepo:
    """The repository for Communities entities.
    """

    _conn = attr.ib()  # :type sqlite3.Connection
    _primary_keys = (
        attr.fields(Source).currency,
        attr.fields(Source).pubkey,
        attr.fields(Source).identifier,
        attr.fields(Source).noffset,
    )

    def insert(self, source):
        """
        Commit a source to the database
        :param sakia.data.entities.Source source: the source to commit
        """
        source_tuple = attr.astuple(source)
        values = ",".join(["?"] * len(source_tuple))
        self._conn.execute(
            "INSERT INTO sources VALUES ({0})".format(values), source_tuple
        )

    def get_one(self, **search):
        """
        Get an existing not consumed source in the database

        :param ** search: the criterions of the lookup
        :rtype: sakia.data.entities.Source
        """
        filters = []
        values = []
        for k, v in search.items():
            filters.append("{k}=?".format(k=k))
            values.append(v)

        request = "SELECT * FROM sources WHERE used_by is NULL AND {filters}".format(
            filters=" AND ".join(filters)
        )

        c = self._conn.execute(request, tuple(values))
        data = c.fetchone()
        if data:
            return Source(*data)

    def get_all(self, **search):
        """
        Get all existing not consumed source in the database corresponding to the search

        :param ** search: the criterions of the lookup
        :rtype: [sakia.data.entities.Source]
        """
        filters = []
        values = []
        for k, v in search.items():
            value = v
            filters.append("{key} = ?".format(key=k))
            values.append(value)

        request = "SELECT * FROM sources WHERE used_by is NULL AND {filters}".format(
            filters=" AND ".join(filters)
        )

        c = self._conn.execute(request, tuple(values))
        datas = c.fetchall()
        if datas:
            return [Source(*data) for data in datas]
        return []

    def drop(self, source):
        """
        Drop an existing source from the database
        :param sakia.data.entities.Source source: the source to update
        """
        where_fields = attr.astuple(
            source, filter=attr.filters.include(*SourcesRepo._primary_keys)
        )
        self._conn.execute(
            """DELETE FROM sources
                              WHERE
                              currency=? AND
                              pubkey=? AND
                              identifier=? AND
                              noffset=?""",
            where_fields,
        )

    def drop_all(self, **filter):
        filters = []
        values = []
        for k, v in filter.items():
            value = v
            filters.append("{key} = ?".format(key=k))
            values.append(value)

        request = "DELETE FROM sources WHERE {filters}".format(
            filters=" AND ".join(filters)
        )
        self._conn.execute(request, tuple(values))

    def consume(self, source, tx_hash):
        """
        Consume a source by setting the used_by column with the tx hash

        :param Source source: Source instance to consume
        :param str tx_hash: Hash of tx
        :return:
        """
        where_fields = attr.astuple(
            source, filter=attr.filters.include(*SourcesRepo._primary_keys)
        )
        fields = (tx_hash,) + where_fields
        self._conn.execute(
            """UPDATE sources SET used_by=?
                              WHERE
                              currency=? AND
                              pubkey=? AND
                              identifier=? AND
                              noffset=?""",
            fields,
        )

    def restore_all(self, tx_hash):
        """
        Restore all sources released by tx_hash setting the used_by column with null

        :param Source source: Source instance to consume
        :param str tx_hash: Hash of tx
        :return:
        """
        self._conn.execute(
            """UPDATE sources SET used_by=NULL
                              WHERE
                              used_by=?""",
            (tx_hash,),
        )
