import uuid

from sqlalchemy import (BIGINT, DATETIME, INTEGER, TIMESTAMP, VARBINARY,
                        Column, DateTime, ForeignKey, String, text)
from sqlalchemy.orm import relationship

from ..base import UUID, Base, indent, json_test, json_loop
from ..reference.type_information import TypeInformation

class SpecimenZoneMultimedia(Base):
    # définition de table
    __tablename__ = "SpecimenZoneMultimedia"

    id = Column("SpecimenZoneMultimedia_Id", UUID, primary_key=True, nullable=False, default=uuid.uuid4)

    id_specimen = Column("SpecimenZoneMultimedia_Specimen_Id", UUID, ForeignKey("Specimen.Specimen_Id"), nullable=True)
    id_type_information = Column("SpecimenZoneMultimedia_TypeInformation_Id", UUID, ForeignKey("TypeInformation.Reference_Id"), nullable=True)
    notes = Column("SpecimenZoneMultimedia_Notes", String, nullable=True)
    ordre = Column("SpecimenZoneMultimedia_Ordre", INTEGER, nullable=True)

    t_write = Column("_trackLastWriteTime", DateTime, nullable=False, server_default=text("(getdate())"))
    t_creation = Column("_trackCreationTime", DateTime, nullable=False, server_default=text("(getdate())"))
    t_write_user = Column("_trackLastWriteUser", String(64), nullable=False)
    t_creation_user = Column("_trackCreationUser", String(64), nullable=False)
    t_version = Column("_rowVersion", TIMESTAMP, nullable=False)

    # liaisons
    from .specimen import Specimen as t_specimen
    specimen = relationship(t_specimen, foreign_keys=[id_specimen], post_update=True)
    type_information = relationship(TypeInformation, foreign_keys=[id_type_information])
    
    multimedias = relationship("ChampSpecimenZoneMultimediaMultimedia", order_by="ChampSpecimenZoneMultimediaMultimedia.ordre")

    @property
    def json(self):
        data = {}
        data['_type'] = self.__class__.__name__
        data['id'] = self.id

        data['type_information'] = json_test(self.type_information)
        data['notes'] = self.notes
        data['ordre'] = self.ordre
        data['multimedias'] = json_loop(self.multimedias)

        data['t_write'] = self.t_write.isoformat()
        data['t_creation'] = self.t_creation.isoformat()
        data['t_write_user'] = self.t_write_user
        data['t_creation_user'] = self.t_creation_user
        data['t_version'] = self.t_version.hex()

        return data
