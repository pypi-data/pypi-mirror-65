import boto3
import pandas as pd

def get_ec2(status: str, profile: str, filter: str):
    possible_filters = dict(
        live=[{"Name":"instance-state-name", "Values":["running"] }],
        all=[]
    )

    filters = possible_filters[filter]

    ec2 = boto3.session.Session(profile_name=profile, region_name='eu-west-1').client('ec2')
    live_inst = ec2.describe_instances(Filters=filters)
    df = pd.DataFrame(live_inst['Reservations'])
    df_list = [ pd.DataFrame.from_dict(x[0], orient='index') for x in df['Instances'].values ]
    full_df = pd.concat(df_list,axis=1, sort=True).T

    # TODO: parse tags
    target_columns = 'CpuOptions InstanceId InstanceType LaunchTime PublicIpAddress Tags PrivateIpAddress'.split(' ')
    return_df = full_df[target_columns]

    return_df['name'] = return_df.Tags.apply(lambda x:
        [ r['Value'] for r in x if r['Key']=='Name'][0])

    pd.set_option('display.max_colwidth', 40)

    return return_df

def update_ec2_ssh(profile: str):
    from .sshconf import read_ssh_config
    # get ec2 and ssh config to get hosts
    running_instances = get_ec2("running", profile=profile, filter='live').T
    ssh_config_obj = read_ssh_config('/Users/jakub/.ssh/config')
    hosts = ssh_config_obj.hosts()
    changes = {}

    for index, row in running_instances.T.iterrows():
        try:
            target_host = [ t['Value'] for t in row.Tags if t['Key']=='Name'][0]
        except IndexError as e:
            raise IndexError("You probably did not set up the EC2 tags correctly (there are empties)")
        target_ip = row.PublicIpAddress
        # change and write
        if target_host in ssh_config_obj.hosts_:
            ssh_config_obj.set(target_host, HostName=target_ip)
            changes[target_host] = target_ip
            ssh_config_obj.write('/Users/jakub/.ssh/config')
        else:
            print(f'Could not find {target_host} in SSH config.')

    print(f"Changed {changes.keys()} to {changes.items()} respectively.")


def start_ec2(instance_id: str, profile: str):
    ec2 = boto3.session.Session(profile_name=profile, region_name='eu-west-1').client('ec2')

    resp = ec2.start_instances(InstanceIds=[instance_id])
    print(resp)


def stop_ec2(inst_id: str, profile: str):
    ec2 = boto3.session.Session(profile_name=profile, region_name='eu-west-1').client('ec2')

    resp = ec2.stop_instances(InstanceIds=[instance_id])
    print(resp)

def change_inst_type(inst_id: str, profile: str):
    ec2 = boto3.session.Session(profile_name=profile, region_name='eu-west-1').client('ec2')

    resp = ec2.change