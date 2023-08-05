from localstack.utils.aws import aws_models
qiXec=super
qiXek=None
qiXej=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  qiXec(LambdaLayer,self).__init__(arn)
  self.cwd=qiXek
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,qiXej,env=qiXek):
  qiXec(RDSDatabase,self).__init__(qiXej,env=env)
 def name(self):
  return self.qiXej.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
