from localstack.utils.aws import aws_models
IiGXK=super
IiGXf=None
IiGXs=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  IiGXK(LambdaLayer,self).__init__(arn)
  self.cwd=IiGXf
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,IiGXs,env=IiGXf):
  IiGXK(RDSDatabase,self).__init__(IiGXs,env=env)
 def name(self):
  return self.IiGXs.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
