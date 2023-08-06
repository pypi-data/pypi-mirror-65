from sspo_db.application import factories as application_factories
from sspo_db.model import factories as model_factories
import re
from pprint import pprint
from tfs.tfs import TFS
import logging
logging.basicConfig(level=logging.INFO)

class BaseEntity():

    def __init__(self):
        
        self.organization = None
        
    def config (self, data):
        
        self.data = data

        self.organization_uuid = self.data['organization_uuid']
        self.tfs_key = self.data['secret']
        self.tfs_url = self.data['url']
        self.configuration_uuid = self.data['configuration_uuid']
        
        self.retrive_tfs()
        
        self.application_application_reference = application_factories.ApplicationReferenceFactory()
        self.application_configuration = application_factories.ConfigurationFactory()
        self.application_organization = application_factories.OrganizationFactory()
        
        self.organization = self.application_organization.get_by_uuid(self.organization_uuid)
        self.configuration = self.application_configuration.get_by_uuid(self.configuration_uuid)
        
    
    def retrive_tfs(self):
        self.tfs =  TFS(self.tfs_key, self.tfs_url) 
        
    def check_value (self, work_item, key):
        return work_item.fields[key] if key in work_item.fields else None

    def create_application_reference(self,external_id, external_url,external_type_entity, internal_uuid, entity_name ):
        #application reference
        application_reference = model_factories.ApplicationReferenceFactory(
                                                    name = None,
                                                    description = None,
                                                    configuration = self.configuration.id,
                                                    external_id = external_id,
                                                    external_url = external_url,
                                                    external_type_entity = external_type_entity,
                                                    internal_uuid = internal_uuid,
                                                    entity_name = entity_name
                                                )

        self.application_application_reference.create(application_reference)
    
    