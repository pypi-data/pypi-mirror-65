import uuid

from sqlalchemy import (BIGINT, DATETIME, INTEGER, TIMESTAMP, VARBINARY,
                        Column, DateTime, ForeignKey, String, text)
from sqlalchemy.orm import relationship

from ..base import UUID, Base, indent, json_test, json_loop


class Specimen(Base):
    __tablename__ = "Specimen"

    id = Column("Specimen_Id", UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    
    from .zone_identification import SpecimenZoneIdentification as t_zone_identification
    id_zone_identification = Column("Specimen_ZoneIdentification_Id", UUID, ForeignKey(t_zone_identification.id), nullable=False)
    from .zone_discipline import SpecimenZoneDiscipline as t_zone_discipline
    id_zone_discipline = Column("Specimen_ZoneDiscipline_Id", UUID, ForeignKey(t_zone_discipline.id), nullable=True)
    id_zone_description_physique = Column("Specimen_ZoneDescriptionPhysique_Id", UUID, nullable=True)
    from .zone_collecte import SpecimenZoneCollecte as t_zone_collecte
    id_zone_collecte = Column("Specimen_ZoneCollecte_Id", UUID, ForeignKey(t_zone_collecte.id), nullable=True)
    from .zone_datation_geologique import SpecimenZoneDatationGeologique as t_zone_datation_geologique
    id_zone_datation_geologique = Column("Specimen_ZoneDatationGeologique_Id", UUID, ForeignKey(t_zone_datation_geologique.id), nullable=True)
    id_zone_donnees_patrimoniales = Column("Specimen_ZoneDonneesPatrimoniales_Id", UUID, nullable=True)
    from .zone_constantes_conservation import SpecimenZoneConstantesConservation as t_zone_constantes_conservation
    id_zone_constantes_conservation = Column("Specimen_ZoneConstantesConservation_Id", UUID, ForeignKey(t_zone_constantes_conservation.id), nullable=True)
    id_zone_reproduction = Column("Specimen_ZoneReproduction_Id", UUID, nullable=True)
    id_zone_objet_associe = Column("Specimen_ZoneObjetAssocie_Id", UUID, nullable=True)
    from .zone_informations_systeme import SpecimenZoneInformationsSysteme as t_zone_informations_systeme
    id_zone_informations_systeme = Column("Specimen_ZoneInformationsSysteme_Id", UUID, ForeignKey(t_zone_informations_systeme.id), nullable=True)

    t_write = Column("_trackLastWriteTime", DateTime, nullable=False, server_default=text("(getdate())"))
    t_creation = Column("_trackCreationTime", DateTime, nullable=False, server_default=text("(getdate())"))
    t_write_user = Column("_trackLastWriteUser", String(64), nullable=False)
    t_creation_user = Column("_trackCreationUser", String(64), nullable=False)
    t_version = Column("_rowVersion", TIMESTAMP, nullable=False)

    # 
    # liens internes
    #

    zone_identification = relationship(t_zone_identification, foreign_keys=[id_zone_identification])    
    zone_discipline = relationship(t_zone_discipline, foreign_keys=[id_zone_discipline])
    zone_collecte = relationship(t_zone_collecte, foreign_keys=[id_zone_collecte])
    zone_datation_geologique = relationship(t_zone_datation_geologique, foreign_keys=[id_zone_datation_geologique])
    zone_constantes_conservation = relationship(t_zone_constantes_conservation, foreign_keys=[id_zone_constantes_conservation])
    zone_informations_systeme = relationship(t_zone_informations_systeme, foreign_keys=[id_zone_informations_systeme])

    #
    # Liens externes
    #  

    from .zone_determination import SpecimenZoneDetermination as t_zone_determination
    zones_determination = relationship(t_zone_determination, back_populates="specimen", order_by="SpecimenZoneDetermination.ordre")
    zones_multimedia = relationship("SpecimenZoneMultimedia", back_populates="specimen", order_by="SpecimenZoneMultimedia.ordre")    

    #
    #
    #

    @property
    def json(self):
        data = {}
        data['_type'] = self.__class__.__name__
        data['id'] = self.id

        # many-to-one fields
        

        # one-to-one data segments

        data['zone_identification'] = json_test(self.zone_identification)
        data['zone_discipline'] = json_test(self.zone_discipline)
        data['id_zone_description_physique'] = self.id_zone_description_physique
        data['zone_collecte'] = json_test(self.zone_collecte)
        data['zone_datatation_geologique'] = json_test(self.zone_datation_geologique)
        data['id_zone_donnees_patrimoniales'] = self.id_zone_donnees_patrimoniales
        data['zone_constantes_conservation'] = json_test(self.zone_constantes_conservation)      
        data['id_zone_reproduction'] = self.id_zone_reproduction
        data['id_zone_objet_associe'] = self.id_zone_objet_associe
        data['zone_informations_systeme'] = json_test(self.zone_informations_systeme)

        # many-to-many data segments

        data['zones_determination'] = json_loop(self.zones_determination)
        data['zones_multimedia'] = json_loop(self.zones_multimedia)

        data['t_write'] = self.t_write.isoformat()
        data['t_creation'] = self.t_creation.isoformat()
        data['t_write_user'] = self.t_write_user
        data['t_creation_user'] = self.t_creation_user
        data['t_version'] = self.t_version.hex()

        return data

