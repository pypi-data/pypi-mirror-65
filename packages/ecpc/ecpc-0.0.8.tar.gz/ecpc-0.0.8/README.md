# EcPc: Simple creation and managment of EC2 instances

EcPc provides a small collection of command-line tools to launch, list,
log in to, and terminate EC2 (spot) instances. 

It's deliberately a basic
tool with few parameters for a user to tweak.

## Prerequisites:

You need to have an AWS account, and have you ACCESS_KEY and SECRET_ACCESS_KEYs to hand. Then install boto3 according to the 
instructions [here](https://pypi.org/project/boto3/)

## Installation:

Via `pip`:

```
% pip install ecpc
```

## Usage:

To launch an instance, use `ecpc create`:

```
% ecpc create my_instance
creating a t2.small instance in region eu-west-1 with ID my_instance
key pair created
security group created
required ami identified
launching instance - this may take some time...
instance launched
%
```

You can change the instance type, and the region it is launched into:

```
% ecpc create my_c5 -r us-west-1 -t c5.large
creating a c5.large instance in region eu-west-1 with ID my_c5
key pair created
security group created
required ami identified
launching instance - this may take some time...
instance launched
%
```

To list your instances:

```
% ecpc list
ID            region     type      up_time   state       cost($)
my_c5         us-west-1  c5.large  00:00:00  booting-up  0.00   
my_instance   eu-west-1  t2.small  00:04:00  ready       0.00 
```
    
**Note: the "cost" value is approximate**

To log in to an instance, use `ecpc login`:

```
% ecpc login my_instance
Warning: Permanently added '52.19.207.118' (ECDSA) to the list of known hosts.
Welcome to Ubuntu 18.04.1 LTS (GNU/Linux 4.15.0-1029-aws x86_64)

    * Documentation:  https://help.ubuntu.com
    * Management:     https://landscape.canonical.com       
    * Support:        https://ubuntu.com/advantage

  System information as of Fri Dec  7 17:07:20 UTC 2018
  System load:  0.0               Processes:           82
      Usage of /:   13.4% of 7.69GB   Users logged in:     0
      Memory usage: 6%                IP address for eth0: 172.31.21.191
      Swap usage:   0%

      Get cloud support with Ubuntu Advantage Cloud Guest:
        http://www.ubuntu.com/business/services/cloud

    0 packages can be updated.
    0 updates are security updates.



    The programs included with the Ubuntu system are free software;
    the exact distribution terms for each program are described in the
    individual files in /usr/share/doc/*/copyright.

    Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
    applicable law.

    To run a command as administrator (user "root"), use "sudo <command>".
    See "man sudo_root" for details.

    ubuntu@my_instance:~$ 
```

To transfer files and directories to/from your instance, use `ecpc transfer`:
```
% ecpc transfer my_local_directory my_c5:./
% ecpc transfer my_c5:./results/result.log . 
```

To terminate an instance, use `ecpc terminate`:

```
% ecpc terminate my_instance
instance terminated
security group deleted
key pair deleted
.pem file deleted
%
```


