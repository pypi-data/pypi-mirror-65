from localstack.utils.aws import aws_models
juyRN=super
juyRF=None
juyRz=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  juyRN(LambdaLayer,self).__init__(arn)
  self.cwd=juyRF
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,juyRz,env=juyRF):
  juyRN(RDSDatabase,self).__init__(juyRz,env=env)
 def name(self):
  return self.juyRz.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
