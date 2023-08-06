import uuid

from sqlalchemy import (BIGINT, DATETIME, INTEGER, TIMESTAMP, VARBINARY,
                        Column, DateTime, ForeignKey, String, text)
from sqlalchemy.orm import relationship


from ...base import UUID, Base, indent, json_test

class ChampSpecimenZoneMultimediaMultimedia(Base):
    # définition de table
    __tablename__ = "ChampSpecimenZoneMultimediaMultimedia"

    id = Column("ChampSpecimenZoneMultimediaMultimedia_Id", UUID, primary_key=True, nullable=False, default=uuid.uuid4)

    from ..zone_multimedia import SpecimenZoneMultimedia
    id_zone_multimedia = Column("ChampSpecimenZoneMultimediaMultimedia_SpecimenZoneMultimedia_Id", UUID, ForeignKey(SpecimenZoneMultimedia.id), nullable=True)
    from ...multimedia.multimedia import Multimedia as t_multimedia
    id_multimedia = Column("ChampSpecimenZoneMultimediaMultimedia_Multimedia_Id", UUID, ForeignKey(t_multimedia.id), nullable=True)
    ordre = Column("ChampSpecimenZoneMultimediaMultimedia_Ordre", INTEGER, nullable=True)

    t_write = Column("_trackLastWriteTime", DateTime, nullable=False, server_default=text("(getdate())"))
    t_creation = Column("_trackCreationTime", DateTime, nullable=False, server_default=text("(getdate())"))
    t_write_user = Column("_trackLastWriteUser", String(64), nullable=False)
    t_creation_user = Column("_trackCreationUser", String(64), nullable=False)

    # liaisons

    multimedia = relationship(t_multimedia, foreign_keys=[id_multimedia], post_update=True)
    zone_multimedia = relationship(SpecimenZoneMultimedia, foreign_keys=[id_zone_multimedia])

    @property
    def json(self):
        data = {}
        data['_type'] = self.__class__.__name__
        data['id'] = self.id

        data['multimedia'] = json_test(self.multimedia)
        data['ordre'] = self.ordre

        data['t_write'] = self.t_write.isoformat()
        data['t_creation'] = self.t_creation.isoformat()
        data['t_write_user'] = self.t_write_user
        data['t_creation_user'] = self.t_creation_user

        return data
