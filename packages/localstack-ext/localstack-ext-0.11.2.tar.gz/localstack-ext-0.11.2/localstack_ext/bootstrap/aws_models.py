from localstack.utils.aws import aws_models
IkGWA=super
IkGWx=None
IkGWf=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  IkGWA(LambdaLayer,self).__init__(arn)
  self.cwd=IkGWx
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,IkGWf,env=IkGWx):
  IkGWA(RDSDatabase,self).__init__(IkGWf,env=env)
 def name(self):
  return self.IkGWf.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
