import argparese
import boto
from boto.ec2.regioninfo import RegionInfo
from boto.exception import EC2ResponseError
import time

#Connect to nectar
region = RegionInfo(name = 'melbourne', endpoint = 'nova.rc.nectar.org.au')

ACCESS_KEY = '0afe4df74d6547409fb4f23afd192895'
SECRET_KEY = 'c5a77a9d73064a4bbb3f8efde68cb862'
DEFAULT_AREA = 'melbourne-np'
image_id = 'ami-190a1773'
COUNT = 2

instance_list=[]
def connectNectar(access_key,secret_key):
    ec2_conn = boto.connect_ec2(aws_access_key_id = access_key,
                                aws_secret_access_key = secret_key,
                                is_secure = True,
                                region = region,
                                port = 8773,
                                path = '/services/Cloud',
                                validate_certs = False)
    return ec2_conn

#launch_instance
def launch_instance(image_id,ec2_conn,count):
    for i in range(count):
        try:
            reservation = ec2_conn.run_instances(image_id,
                                        key_name="assign",
                                        instance_type = 'm1.small',
                                        security_groups = ['default'],
                                        placement=DEFAULT_AREA)
        except EC2ResponseError as error:
            print(error.error_message)
        instance_list.append(reservation.instances[0])

def terminate_instance(ec2_conn,instance_id):
    ec2_conn.terminate_instances(instance_ids = [instance_id])
    print('New instance {} has been terminated.'.format(instance_id))

# set the size of volumn and attach it to the instance
def attach_volumn(ec2_conn,instance,volumn_size):
    try:
        vol = ec2_conn.create_volume(volumn_size, DEFAULT_AREA)
        vol.attach(instance.id, '/dev/vdb')
    except EC2ResponseError as error:
        print(error.error_message)

if __name__ == '__main__':
    #parser = argparse.ArgumentParser()
    #parser.add_argument('-n', type=int, default=1, help='instance count')
    #parser.add_argument('-s', type=int, default =250, help='volumn size')
    #args = parser.parse_args()
    ec2_conn = connectNectar(ACCESS_KEY, SECRET_KEY)
    launch_instance(image_id, ec2_conn, COUNT)
    time.sleep(20)
    for instance in instance_list:
        attach_volumn(ec2_conn, instance, int(50/COUNT))
