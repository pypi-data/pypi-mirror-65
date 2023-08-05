#/bin/python

def get_public_ip():
    from urllib.request import urlopen
    import re
    data = str(urlopen('http://checkip.dyndns.com/').read())
    # data = '<html><head><title>Current IP Check</title></head><body>Current IP Address: 65.96.168.198</body></html>\r\n'
    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)

def get_sg(sg_name: str, profile: str):
    import boto3
    sg_name = sg_name or 'jakub'
    profile = profile or 'default'

    ec2 = boto3.session.Session(profile_name=profile, region_name='eu-west-1').client('ec2')
    resp = ec2.describe_security_groups()
    target_sg_str = list(filter(lambda x: x['GroupName']==sg_name, resp['SecurityGroups']))
    return target_sg_str

def update_sg_to_ip(sg_name='jakub', # ip='2.222.105.71/32',
                    ports=[22, 8888], profile='default'):
    import boto3

    ip = f"{get_public_ip()}/32"

    ec2 = boto3.session.Session(profile_name=profile, region_name='eu-west-1').client('ec2')
    profile = profile or 'default'

    target_sg_str = get_sg(sg_name, profile=profile)[0]
    ec2_res = boto3.session.Session(profile_name=profile, region_name='eu-west-1').resource('ec2')
    sg_res = ec2_res.SecurityGroup(target_sg_str['GroupId'])

    # TODO: make into a loop using ports
    # Removes all previous permissions from this group (hence `jakub`)
    if sg_res.ip_permissions!=[]:
        sg_res.revoke_ingress(IpPermissions=sg_res.ip_permissions)


    description = 'Jakub Aux Jupyter'
    description2 = 'Jakub Aux SSH'
    description3 = 'Jakub Aux Streamlit'
    data = ec2.authorize_security_group_ingress(
            GroupId=target_sg_str['GroupId'],
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 8888,
                'ToPort': 8888,
                'IpRanges': [{'CidrIp': ip, 'Description': description}] },
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': ip, 'Description': description2}]},
                {'IpProtocol': 'tcp',
                'FromPort': 8501,
                'ToPort': 8501,
                'IpRanges': [{'CidrIp': ip, 'Description': description2}]}
            ])
    print('Ingress Successfully Set %s' % data)
