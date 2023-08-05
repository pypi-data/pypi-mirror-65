from localstack.utils.aws import aws_models
idYPH=super
idYPA=None
idYPE=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  idYPH(LambdaLayer,self).__init__(arn)
  self.cwd=idYPA
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,idYPE,env=idYPA):
  idYPH(RDSDatabase,self).__init__(idYPE,env=env)
 def name(self):
  return self.idYPE.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
