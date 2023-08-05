#!/usr/bin/env python

"""start or stop (depending on current state) ec2 instances with tag Name:example"""

import argparse
from argparse import RawTextHelpFormatter as rawtxt
import sys
from os.path import expanduser
import signal
import json
import subprocess
import time
import os
import configparser
import pkg_resources
import inquirer
from stringcolor import cs, bold, underline

def signal_handler(sig, frame):
    """handle control c"""
    print('\nuser cancelled')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def query_yes_no(question, default="yes"):
    '''confirm or decline'''
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("\nPlease respond with 'yes' or 'no' (or 'y' or 'n').\n")

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which
    return which(name) is not None

def config_keyfile(force=None):
    """write a new keyfile"""

    newconfig = """[default]
keyfile = {}
"""
    home = expanduser('~')
    trafficlight_config = os.path.join(home, ".trafficlight.ini")
    config_exists = False
    kf = "unknown"
    if os.path.exists(trafficlight_config):
        config = configparser.ConfigParser()
        config.read(trafficlight_config)
        if "keyfile" in config['default']:
            config_exists = True
            kf = config['default']['keyfile']

    # config doesn't exist. creating a new one.
    if not config_exists or force:
        while True:
            kf = input("Full path to .pem keyfile ["+str(underline(kf))+"] : ") or kf
            if not kf.endswith(".pem"):
                try:
                    kf = config['default']['keyfile']
                except:
                    kf = "unknown"
                print(cs("ERROR:", "red"), cs("keyfile name must be .pem", "yellow"))
                continue
            elif not os.path.isfile(kf):
                try:
                    kf = config['default']['keyfile']
                except:
                    kf = "unknown"
                print(cs("ERROR:", "red"), cs("file does not exist", "yellow"))
                continue
            else:
                break
        newconfig = newconfig.format(kf)
        print(cs("for your convenience,", "PaleTurquoise"), cs("writing keyfile path to ~/.trafficlight.ini", "pink"))
        with open(trafficlight_config, 'w+') as f:
            f.write(newconfig)
    return kf

def check_tag_for_hint(hint, tag_value):
    """return true if hint in tag value"""
    if hint.lower() in tag_value.lower():
        return True
    return False

def get_instance_info(instances, class_instance):
    """takes a list of instances"""
    """get and print instance info to the screen"""
    # collect info
    state_code = 0
    matching_hint = False
    matching_hints = 0
    for instance in instances:
        matching_hint = False
        instance_id = instance['Instances'][0]['InstanceId']
        image_id = instance['Instances'][0]['ImageId']
        instance_key_name = instance['Instances'][0]['KeyName']
        class_instance.start_instance_id = instance_id
        class_instance.start_image_id = image_id
        state_code = instance['Instances'][0]['State']['Code']
        state_name = instance['Instances'][0]['State']['Name']
        instance_type = instance['Instances'][0]['InstanceType']
        try:
            instance_tags = instance['Instances'][0]['Tags']
        except KeyError as e:
            instance_tags = []
        tags_list = ""
        for instance_tag in instance_tags:
            # call a function to check tags and hints
            if check_tag_for_hint(class_instance.tag, instance_tag['Value']):
                matching_hint = True
                matching_hints += 1
            tags_list += instance_tag['Key']+":"+instance_tag['Value']+", "
        tags_list = tags_list[:-2]
        try:
            instance_sgs = instance_tags = instance['Instances'][0]['SecurityGroups']
        except KeyError as e:
            instance_sgs = []
        sgs_list = ""
        for sg in instance_sgs:
            sgs_list += sg['GroupName']+", "
        sgs_list = sgs_list[:-2]
        if state_code == 16:
            state_color = "green"
            instance_ip = instance['Instances'][0]['PublicIpAddress']
            instance_host = instance['Instances'][0]['PublicDnsName']
            class_instance.start_instance_ip = instance_ip
            class_instance.start_instance_host = instance_host
            if class_instance.host:
                description = instance_id+" - "+instance_type+" - "+instance_host
            else:
                description = instance_id+" - "+instance_type+" - "+instance_ip
        elif state_code == 80:
            state_color = "red"
            description = instance_id+" - "+instance_type
        else:
            state_color = "yellow"
            description = instance_id+" - "+instance_type

        # output one instance's info
        if class_instance.pipe:
            description = description.replace(" - ", " ")

            if class_instance.hint:
                if matching_hint:
                    sys.stdout.write(description + '\n')
            else:
                sys.stdout.write(description + '\n')
        else:
            if class_instance.hint:
                if matching_hint:
                    print(cs(state_name+"\n"+description+"\nKey Name: "+instance_key_name+"\nSecurity Groups: "+sgs_list+"\nTags: "+tags_list, state_color))
                    print("-------")
            else:
                print(cs(state_name+"\n"+description+"\nKey Name: "+instance_key_name+"\nSecurity Groups: "+sgs_list+"\nTags: "+tags_list, state_color))
                print("-------")
    if class_instance.hint:
        if matching_hints < 1:
            # no instances found with hint
            class_instance.set_number_of_instances(0)
            class_instance.no_instances_found()

def stop_and_start(instances, class_instance):
    """stop and start instances"""
    state_code = 0
    tmp_switch = ""
    connect_to_started = False
    for instance in instances:
        instance_id = instance['Instances'][0]['InstanceId']
        state_code = instance['Instances'][0]['State']['Code']
        if state_code == 16  or state_code == 80:
            if state_code == 16:
                tmp_switch = "stop-instances"
                tmp_verbing = cs("stopping", "red")
            else:
                tmp_switch = "start-instances"
                tmp_verbing = cs("starting", "green")
            if class_instance.switch:
                cmd = "aws ec2 "+class_instance.switch+" --instance-ids "+instance_id+" "+class_instance.selected_region
                run = subprocess.check_output(cmd, shell=True)
            else:
                cmd = "aws ec2 "+tmp_switch+" --instance-ids "+instance_id+" "+class_instance.selected_region
                if tmp_switch == "stop-instances" and class_instance.connect:
                    connect_to_started = True
                else:
                    run = subprocess.check_output(cmd, shell=True)
            if class_instance.verbing:
                print(class_instance.verbing, instance_id)
            elif not connect_to_started:
                print(tmp_verbing, instance_id)
        else:
            print(cs(instance_id+" not in a state to be "+class_instance.verb, "yellow"))
    return connect_to_started

def connect_to_instance(connect_to_started, class_instance):
    """connect to instance"""
    # handle key file config
    keyfile = config_keyfile()

    # calculate ssh username with ami
    # https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connection-prereqs.html#connection-prereqs-get-info-about-instance
    ami_types = {
        "Amazon Linux 2":"ec2-user",
        "CentOS":"centos",
        "Debian":"root",
        "Fedora":"ec2-user",
        "RHEL":"ec2-user",
        "SUSE":"ec2-user",
        "Ubuntu":"ubuntu",
    }
    image_cmd = "aws ec2 describe-images --image-ids \""+class_instance.start_image_id+"\" {}--output json".format(class_instance.selected_region)
    # custom ami-* ids don't have an OS desription!!!
    #
    #
    image_json = subprocess.check_output(image_cmd, shell=True).decode("utf-8").strip()
    image_json = json.loads(image_json)
    os_descrip = False
    if "Description" in image_json["Images"][0]:
        os_descrip = image_json["Images"][0]["Description"]
        
    if not os_descrip:
        username = input("username:")
    else:
        username = False
        for k, v in ami_types.items():
            if k in os_descrip:
                username = v
        if not username:
            username = input("username:")

    # case: instance starting wait for a ready state then get IP
    if not connect_to_started:
        print(cs("please wait while the instance finishes starting...", "IndianRed"))
        start_time = time.time()
        state_code = 0
        while state_code != 16:
            cmd = "aws ec2 describe-instances --instance-ids {} {}--output json".format(class_instance.start_instance_id, class_instance.selected_region)
            instances = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
            instances = json.loads(instances)
            instances = instances['Reservations']
            for instance in instances:
                state_code = instance['Instances'][0]['State']['Code']
            elapsed_time = time.time() - start_time
            elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            elapsed_time = str(elapsed_time)
            print(cs("[ Time Elapsed:", "grey"), cs(elapsed_time+" ]      ", "grey"), end="\r")
        countdown = 20
        while countdown > 0:
            time.sleep(1)
            elapsed_time = time.time() - start_time
            elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            elapsed_time = str(elapsed_time)
            print(cs("[ Time Elapsed:", "grey"), cs(elapsed_time+" ]      ", "grey"), end="\r")
            countdown -= 1
        cmd = "aws ec2 describe-instances --instance-ids {} {}--output json".format(class_instance.start_instance_id, class_instance.selected_region)
        instances = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
        instances = json.loads(instances)
        instances = instances['Reservations']
        for instance in instances:
            instance_ip = instance['Instances'][0]['PublicIpAddress']
            instance_host = instance['Instances'][0]['PublicDnsName']
        print("[ Time Elapsed:", elapsed_time+" ]      ")
    # lets do some actual connecting
    if class_instance.host:
        cmd = cmd = "ssh -o \"StrictHostKeyChecking no\" -i {} {}@{}".format(keyfile, username, class_instance.start_instance_host)
    else:
        cmd = "ssh -o \"StrictHostKeyChecking no\" -i {} {}@{}".format(keyfile, username, class_instance.start_instance_ip)
    subprocess.call(cmd, shell=True)

class ArgHandler:
    """handle arguments, messaging, and options"""

    number_of_instances = 0    

    def __init__(self, tag, key, region, green, red, host, yes, connect, pipe, dokey, leave, hint):
        self.tag = tag
        self.key = key
        self.region = region
        self.green = green
        self.red = red
        self.host = host
        self.yes = yes
        self.connect = connect
        self.pipe = pipe
        self.dokey = dokey
        self.leave = leave
        self.hint = hint
        self.switch = False
        self.verbing = False
        self.verb = "continue"
        self.question = "continue?"
        self.start_instance_id = ""
        self.start_image_id = ""
        self.start_instance_ip = ""
        self.start_instance_host = ""

    @property
    def selected_region(self):
        selected_region = ""
        if self.region is not None:
            selected_region = "--region {} ".format(self.region)
        return selected_region

    @property
    def do_nothing(self):
        do_nothing = False
        if self.leave:
            do_nothing = True
        return do_nothing
    @do_nothing.setter
    def do_nothing(self, value):
        if value:
            self.leave = True
        else:
            self.leave = False

    @classmethod
    def set_number_of_instances(cls, number):
        cls.number_of_instances = number

    def error_check(self):
        """do error checking"""
        # check for aws
        if not is_tool("aws"):
            print(cs("this program requires aws cli", "yellow"))
            print("to install it run", cs("pip3 install awscli --upgrade --user", "fuchsia"))
            exit()
        # error checking for both stop and start and no flags.
        if self.green and self.red:
            print(cs("you cannot both start and stop.", "yellow"))
            print("either", cs("--green", "green"), "to start instances or", cs("--red", "red"), "to stop.")
            exit()
        # error checking for both stop and connect flags.
        if self.red and self.connect:
            print(cs("you cannot connect to an instance you're stopping.", "yellow"))
            exit()

    def multiple_connect_check(self):
        # cannot connect to more than one instance
        if self.connect and self.number_of_instances > 1:
            print(cs("you've passed the --connect flag but there are more than one instances to list.", "yellow"))
            print(cs("if you'd like to use traffic light to connect to this instance, use a unique tag", "orange"), cs("Name", "orange").bold(), cs("or another tag with the --key flag.", "orange"))
            print()
            print(cs("for more information try:", "lightgrey2"), cs("trafficlight -h", "pink"))
            exit()

    def no_instances_found(self):
        if self.number_of_instances == 0:
            if self.pipe:
                sys.stdout.write('no instances found.\n')
            else:
                print(cs("no instances found.", "yellow"))
            exit()

    def get_instances(self):
        """get instances"""
        # if there's no positional arg output info for all instances and do nothing
        if self.tag == "none" or self.hint:
            cmd = "aws ec2 describe-instances {}--output json".format(self.selected_region)
            instances = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
            if not self.red and not self.green:
                self.do_nothing = True
        # else get info for instances with tag name
        else:
            cmd = "aws ec2 describe-instances --filters 'Name=tag:{},Values={}' {}--output json"
            instances = subprocess.check_output(cmd.format(self.key, self.tag, self.selected_region), shell=True).decode("utf-8").strip()
        instances = json.loads(instances)
        instances = instances['Reservations']
        return instances

    def set_messaging(self):
        if self.green:
            if self.connect:
                self.question = "start instances and connect?"
            else:
                self.question = "start instances?"
            self.switch = "start-instances"
            self.verb = "started"
            self.verbing = cs("starting", "green")
        elif self.red:
            self.question = "stop instances?"
            self.switch = "stop-instances"
            self.verb = "stopped"
            self.verbing = cs("stopping", "red")
        else:
            if self.connect:
                self.question = "connect?"
            else:
                self.question = "switch instance state?"
            self.verb = "switched"


def main():
    '''starts and stops ec2 instances with tag names.'''
    version = pkg_resources.require("trafficlight")[0].version
    parser = argparse.ArgumentParser(
        description='start or stop (depending on current state) ec2 instances with tag Name:example',
        prog='trafficlight',
        formatter_class=rawtxt
    )

    #parser.print_help()
    parser.add_argument(
        "tag",
        help="""starts and stops ec2 instances with tag names.\n\n
    $ trafficlight example\n
    where example is the value for the tag with key Name""",
        nargs='?',
        default='none'
    )
    parser.add_argument('--key', help="optional. use a tag key besides Name", default="Name")
    parser.add_argument("-R", "--region", help="specify a different region", default=None)
    parser.add_argument('-g', '--green', action='store_true', help='start.')
    parser.add_argument('-r', '--red', action='store_true', help='stop.')
    parser.add_argument('--hint', action='store_true', help='attempt to find instances with tag hint or partial tag.')
    parser.add_argument('-L', '--leave', action='store_true', help='do not change instance state.')
    parser.add_argument('-y', '--yes', action='store_true', help='automatically approve all y/n prompts.')
    parser.add_argument('-H', '--host', action='store_true', help='use hostnames instead of ip addresses.')
    parser.add_argument('-c', '--connect', action='store_true', help='begin an ssh session.')
    parser.add_argument('-K', '--keyfile', action='store_true', help='write pem keyfile to trafficlight config.')
    parser.add_argument('-p', '--pipe', action='store_true', help='output instance ip or hostname via standard out to pipe into other commands.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+version)
    args = parser.parse_args()
    tag = args.tag
    key = args.key
    region = args.region
    green = args.green
    red = args.red
    host = args.host
    yes = args.yes
    connect = args.connect
    pipe = args.pipe
    dokey = args.keyfile
    leave = args.leave
    hint = args.hint

    # instantiate ArgHandler class
    shell = ArgHandler(tag, key, region, green, red, host, yes, connect, pipe, dokey, leave, hint)

    #initial error checking
    shell.error_check()

    # do keyfile flag
    if shell.dokey:
        force = True
        config_keyfile(force)
        exit()

    # starter message (move to class?)
    if not shell.pipe:
        print("checking for instances...")

    # get instances
    instances = shell.get_instances()

    # set number of instances
    shell.set_number_of_instances(len(instances))

    # no instances found with the tag name given
    shell.no_instances_found()
    
    # check for multiple instances before connecting
    shell.multiple_connect_check()

    # get and print instance info
    get_instance_info(instances, shell)

    # set messaging
    shell.set_messaging()

    # switch instance states
    if not shell.do_nothing and not shell.pipe:
        if shell.yes or query_yes_no(shell.question, "yes"):
            # start and stop instances
            connect_to_started = stop_and_start(instances, shell)

            # connect to ec2 via ssh
            if connect:
                connect_to_instance(connect_to_started, shell)

if __name__ == "__main__":
    main()
