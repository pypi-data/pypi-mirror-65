from sspo_db.config.base import Entity
from sqlalchemy import Column, Boolean ,ForeignKey, Integer, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
from sspo_db.model.stakeholder.models import Person

class Organization(Entity):
    is_instance_of = "eo.organization" 
    __tablename__ = "organization"
    serialize_rules =('-id', "-uuid", 
        "-scrum_project.organization.scrum_project", 
        "-team.organization.team",
        "-people.organization.person",
        "-configuration", )
    
    scrum_project = relationship("ScrumProject", back_populates="organization")
    team = relationship("Team", back_populates="organization")
    people = relationship(Person, back_populates="organization")
    configuration = relationship("Configuration", back_populates="organization") 


class Team(Entity):
    is_instance_of = "eo.team"
    __tablename__ = "team"

    type = Column(String(50))
    
    organization_id = Column(Integer, ForeignKey('organization.id'))
    organization = relationship("Organization", back_populates="team")
    team_members = relationship("TeamMember", back_populates="team")

    __mapper_args__ = {
        'polymorphic_identity':'team',
        'polymorphic_on':type
    }

class ScrumTeam(Team):
    is_instance_of = "eo.team.complex"
    __tablename__ = "scrum_team"
    
    id = Column(Integer, ForeignKey('team.id'), primary_key=True)
    scrum_project = Column(Integer, ForeignKey('scrum_project.id'))
    
    __mapper_args__ = {
        'polymorphic_identity':'scrum_team',
    }

class DevelopmentTeam(Team):
    is_instance_of = "eo.team.atomic"
    __tablename__ = "development_team"

    id = Column(Integer, ForeignKey('team.id'), primary_key=True)
    scrum_team_id = Column(Integer, ForeignKey('scrum_team.id'))
    
    
    __mapper_args__ = {
        'polymorphic_identity':'development_team',
    }
