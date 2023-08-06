from .base import Base

class NumeroDoc(Base):

    def __init__(self, authorize, environment):

        super(NumeroDoc, self).__init__(authorize)

        self.environment = environment

    def execute(self):

        uri = '%snumerodoc' % (self.environment.apidoc)

        return self.request_numerodoc("POST", uri)