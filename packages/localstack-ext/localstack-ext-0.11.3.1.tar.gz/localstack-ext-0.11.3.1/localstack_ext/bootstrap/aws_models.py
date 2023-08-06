from localstack.utils.aws import aws_models
zifuL=super
zifuK=None
zifuq=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  zifuL(LambdaLayer,self).__init__(arn)
  self.cwd=zifuK
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,zifuq,env=zifuK):
  zifuL(RDSDatabase,self).__init__(zifuq,env=env)
 def name(self):
  return self.zifuq.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
