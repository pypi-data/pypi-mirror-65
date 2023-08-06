import uuid

from sqlalchemy import TIMESTAMP, Column, DateTime, ForeignKey, String, text
from sqlalchemy.orm import relationship

from ..base import UUID, Base, indent, json_test
from .zone_generale import MultimediaZoneGenerale


class Multimedia(Base):
    # définitions de table
    __tablename__ = "Multimedia"

    id = Column("Multimedia_Id", UUID, primary_key=True, nullable=False, default=uuid.uuid4)

    id_zone_generale = Column("Multimedia_ZoneGenerale_Id", UUID, ForeignKey("MultimediaZoneGenerale.MultimediaZoneGenerale_Id"), nullable=False)
    id_zone_donnees_techniques = Column("Multimedia_ZoneDonneesTechniques_Id", UUID, nullable=True)
    id_zone_donnees_administratives = Column("Multimedia_ZoneDonneesAdministratives_Id", UUID, nullable=True)
    id_zone_informations_systeme = Column("Multimedia_ZoneInformationsSysteme_Id", UUID, nullable=True)

    t_write = Column("_trackLastWriteTime", DateTime, nullable=False, server_default=text("(getdate())"))
    t_creation = Column("_trackCreationTime", DateTime, nullable=False, server_default=text("(getdate())"))
    t_write_user = Column("_trackLastWriteUser", String(64), nullable=False)
    t_creation_user = Column("_trackCreationUser", String(64), nullable=False)
    t_version = Column("_rowVersion", TIMESTAMP, nullable=False)

    # liaisons

    zone_generale = relationship(MultimediaZoneGenerale, foreign_keys=[id_zone_generale], post_update=True)

    @property
    def json(self):
        data = {}
        data['_type'] = self.__class__.__name__
        data['id'] = self.id
        
        data['zone_generale'] = json_test(self.zone_generale)
        data['id_zone_donnees_techniques'] = self.id_zone_donnees_techniques
        data['id_zone_donnees_administratives'] = self.id_zone_donnees_administratives
        data['id_zone_informations_systeme'] = self.id_zone_informations_systeme

        data['t_write'] = self.t_write.isoformat()
        data['t_creation'] = self.t_creation.isoformat()
        data['t_write_user'] = self.t_write_user
        data['t_creation_user'] = self.t_creation_user
        data['t_version'] = self.t_version.hex()
        
        return data
