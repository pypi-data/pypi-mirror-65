from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
from pprint import pprint as pp
import os

VERSION_BANNER = """
ML & data helper code! %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'ML & data helper code!'

        # text displayed at the bottom of --help output
        epilog = 'Usage: dt command [args] [kwargs]'

        # controller level arguments. ex: 'dt --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } ),
        ]


    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

    @ex(
        help='AWS Security Groups helper functions',
        arguments=[
            (['action'],{
                "help" : "One of {update, show}",
                "action": "store"
            }),
            (['-n','--name'],{
                "help" : "Name of the SG to act on",
                "action": "store"
            }),
            (['-ip'],{
                "help" : "IP to add to security group",
                "action": "store"
            }),
            (['-p','--proifle'],{
                "help" : "Which AWS profile should boto3 use",
                "action" : "store"
            })
        ]
    )
    def sg(self):
        from ..ext.aws_sg import get_sg, update_sg_to_ip
        profile = self.app.pargs.__dict__.get('profile') or self.app.pargs.__dict__.get('p') or 'default'

        if self.app.pargs.action=='show':
            pp(get_sg(self.app.pargs.name, profile))

        elif self.app.pargs.action=='update':
            update_sg_to_ip(sg_name=self.app.pargs.name, profile=profile)

        else:
            raise NotImplementedError('As action, chose one of {update, show}')

    @ex(
        help="AWS EC2 helper commands.",
        arguments=[
            (['action'],{
                    "help" : "To show one of {ls, update}.",
                    "action" : "store"
                }),
            (['-p','--profile'],{
                "help" : "Which AWS profile should boto3 use.",
                "action": "store"
            }),
            (['-f','--filter'],{
                "help" : "One of {live, all}. Default: live",
                "action": "store"
            }),
            (['-id'],{
                "help": "InstanceId to be passed to ec2 start/stop",
                "action": "store"
            })
        ]
    )
    def ec2(self):
        from ..ext.aws_ec2 import get_ec2, start_ec2, stop_ec2, update_ec2_ssh

        profile = self.app.pargs.profile or 'default'
        filt = self.app.pargs.filter or "live"

        if self.app.pargs.action=='ls':
            print(get_ec2('live', profile, filt))

        elif self.app.pargs.action=='update':
            print(update_ec2_ssh(profile))

        elif self.app.pargs.action=='start':
            start_ec2(self.app.pargs.id, profile)

        elif self.app.pargs.action=='stop':
            stop_ec2(self.app.pargs.id, profile)

        else:
            raise NotImplementedError("Choose one of {ls, update, start, stop}")

    @ex(
        help="Display all available Fluidstack nodes.",
        arguments=[
            (['action'],{
                "help" : "To show one of {avail, ls, start, stop}.",
                "action" : "store"
            }),
            (['-stats'],{
            "help" : "One of {all, gpu} to show either all (df) or gpu (json)",
            "action": "store"
            }),
            (['-n_gpu'],{
                "help" : "# of gpus required to be on the machine",
                "action" : "store"
            }),
            (['-id'],{
                "help" : "ID of the container to work with",
                "action" : "store"
            })
        ]
    )
    def fls(self):
        from ..ext.fluidstack import avail_fl_nodes, show_running, \
            stop_container, start_container


        args = self.app.pargs
        if args.action=='avail':
            avail_fl_nodes(args.stats, args.n_gpu)

        elif args.action=='ls':
            show_running()

        elif args.action=='stop':
            stop_container(args.id)

        elif args.action=='start':
            start_container(args.id)

        else:
            raise NotImplementedError('Set the first parg to one of {avail, ls, start, stop}')


    @ex(
        help='Monitor (lack of) GPU activity. Remeber to add & at the end',
        arguments=[
            (['-freq'],{
                "help" : "Second frequency between checks",
                "action" : "store"
            }),
            (['-n'], {
                "help" : "Number of checks before alert",
                "action" : "store"
            })
        ]
    )
    def monitor(self):
        from ..ext.monitor import Monitor
        delay = self.app.pargs.freq or 10
        alert_threshold = self.app.pargs.freq or 60

        monitor = Monitor(int(delay), int(alert_threshold))
        print(f'Monitor is running with d={delay} and thershold={alert_threshold}')


    # number of files
    @ex(
        help='Displays the number of files',
        arguments=[
            (['-d'], {
            "help" : "which directory to show",
            "action" : "store" } )
        ]
    )
    def nf(self):
        loc = self.app.pargs.d or '.'
        os.system(f'ls {loc} | wc -l')

    @ex(
        help="Copies things from zshrc.txt to ~/.bashrc or ~/zshrc",
        arguments = [
            (['shell'], {
                "help" : "One of {sh, zsh}. Imports a DT version of zshrc into bashrc or zshrc.",
                "action": "store"
            })
        ]
    )
    def load(self):
        zshrc = os.path.abspath(__file__).split('/')[:-2] + ['ext', 'zshrc.txt']
        zshrc_path = os.path.join('/'.join(zshrc))
        if self.app.pargs.shell == 'sh':
            os.system(f'cat {zshrc_path} >> ~/.bashrc ')
        if self.app.pargs.shell == 'zsh':
            os.system(f'cat {zshrc_path} >> ~/.zshrc ')
        else:
            raise NotImplementedError("Try one of {sh, zsh}")


    @ex(
        help='Operations on the SSH config',
        arguments=[
            (['action'],{
                "help" : "To show one of {set, ls, update}.",
                "action" : "store"
            }),
            (['-host'],{
            "help" : "Which SSH config host to change",
            "action": "store"
            }),
            (['-ip'],{
                "help" : "The IP to update in the ssh config as HostName",
                "action" : "store"
            })
        ]
    )
    def ssh(self):
        #TODO: missing servers
        from ..ext.sshconf import read_ssh_config
        if self.app.pargs.action=='set':
            ssh_config_obj = read_ssh_config('/Users/jakub/.ssh/config')
            ssh_config_obj.set(self.app.pargs.host, HostName=self.app.pargs.ip)
            ssh_config_obj.write('/Users/jakub/.ssh/config')
            print(ssh_config_obj.config())

        elif self.app.pargs.action=='update':
            from ..ext.aws_ec2 import update_ec2_ssh
            profile ='default' # or  self.app.pargs
            print(update_ec2_ssh(profile))

        else:
            # raise NotImplementedError()
            print('Arg out of {set, update} provided assuming an SSH command.')
            ssh_config_obj = read_ssh_config('/Users/jakub/.ssh/config')
            target = self.app.pargs.action
            if not target in ssh_config_obj.hosts_: raise Exception(f'Host {target} not in configured hosts.')
            else:
                os.system('dt sg update')
                os.system(f'ssh {target}')


    @ex(
        help='Operations with config.',
        arguments = [
            (['action'], {
                "help" : "One of {show, set, loc}: \
                *show*: show configs Sentry DNS etc. \
                *set*: Resets the config from CLI. \
                *loc*: shows the location of the config",
                'action' : "store",
            })
        ]
    )
    def config(self):
        from ..ext.config_cmd import config
        args = self.app.pargs

        # shows config
        if args.action=='show':
            for attr in dir(config):
                if not attr.startswith('_'):
                    print(f"{attr}: {getattr(config,attr)}")

        # shows the path of the config
        if args.action=='loc':
            print(os.path.abspath(__file__))

        # resets the config
        # TODO this config method needs programmatic acces for spot instances
        if args.action=='set':
            initialize(overwrite=True)

        else:
            raise NotImplementedError("Try one of {show, set, loc}")


    @ex(
        help='Tracks your ML code till finish',
        arguments=[
            (['flags'], {
                'help' : 'Which  script + flags you want to pass to the underlying python.'
                         'e.g. train.py --parallel --batch_size 256',
                'action' : "store"
            }),
            (['-ns'], {
                'help' : 'Shuts down the computer between in the shutdown_hours.'
                        'Set to 22-08. Default: True',
                "action" : 'store'
            }),
            (['-t'], {
                'help' : 'If we are testing / doing a dry run. Default: False',
                "action" : "store"
            }),
            (['-cfg'],{
                'help': "location of the config file",
                "action" : "store",
            }),
            (['-p'],{
                "help": "which Python interpreter to use."
                        " Default is determined by `which python3`",
                "action" : "store"
            })
        ]
    )
    def track(self):
        from ..ext.tracking import tracking, initialize, test_sentry
        ''' 'Tracks experiments by making a Sentry alert when a script finishes. '''
        args = self.app.pargs
        if self.app.pargs is not None:
            tracking(args.flags, args.t, args.ns, args.p)

    @ex(
        help='Test if sentry DSN is set up correctly.'
    )
    def test(self):
        from ..ext.tracking import initialize, test_sentry
        test_sentry()

    @ex(
        help='All Github related operations',
        arguments=[
             (['action'],{
                "help" : "To show one of {forks}.",
                "action" : "store"
            }),
            (['-url'],{
                # TODO: what if there's no forks to give?
                "help" : "Github URL to search for forks."
            })
        ]
    )
    def gh(self):
        from ..ext.github import find_forks
        if self.app.pargs.action=='forks':
            print(find_forks(self.app.pargs.url))

    @ex(
        help='Manage TODOs using Google Keep',
        arguments=[
            (['action'],{
                "help" : "One of {add, ls, dn}",
                "action": "store"
            }),
            (['-t'],{
                "help": "Text of the TODO",
                "action": "store"
            }),
            (['-l'],{
                "help": "Length of time in hours this is expected to take",
                "action": "store"
            }),
            (['-p'],{
                "help" : "Project name. One of {DA, SL}",
                "action" : 'store'
            }),
            (['-i'],{
                "help" : "Id of the finished task",
                "action": "store"
            }),
            (['-f'],{
                "help" : "Filter TODOs for ls",
                "action": "store"
            })
        ]
    )
    def td(self):
        from ..ext.gkeep import add_todo, list_todos, done_todo
        project = self.app.pargs.p or 'SL'

        if self.app.pargs.action=='add':
            add_todo(self.app.pargs.t, self.app.pargs.l, self.app.pargs.p)
        elif self.app.pargs.action=='ls':
            list_todos(self.app.pargs.f or True,
                       self.app.pargs.p)
        elif self.app.pargs.action=='dn':
            done_todo(self.app.pargs.i)

        else:
            raise NotImplemented("Action must be one of {add, ls, dn}")

    @ex(
        help='Execute a Python command across all files in current dir.',
        arguments=[
            (['command'],{
                "help": "what python command to run",
                "action": "store"
            }),
            (['-f'],{
                "help" : "filter all files in in this directory and below by this expression.",
                "action" : "store"
            })
        ]
    )
    def py(self):
        from ..ext.python_exec import execute
        execute(self.app.pargs.command, self.app.pargs.f)