FROM rhscl/python-27-rhel7

CMD yum update -y

ENTRYPOINT ['top', '-b']
