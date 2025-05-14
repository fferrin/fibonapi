## Tasks

1. An endpoint that returns the value from the Fibonacci sequence for a given number.
2. An endpoint that returns a list of numbers and the corresponding values from the Fibonacci
sequence from 1 to N with support for pagination. Page size should be parameterized with a
default of 100.
3. An endpoint to blacklist a number to permanently stop it from being shown in Fibonacci results
when requested. The blacklisted numbers should persist in application state.
4. An endpoint to remove a number from the blacklist.

## Build

To build the backend, you can run:
```bash
$ docker build -t fibonapi:latest .
```

FibonAPI uses multistage builds to trim the final production image. To run only the tests, use the `base` target:
```bash
$ docker build --target base -t fibonapi:tests .
```

## Deploy

To deploy this into your AWS account, you will need to get IAM credentials in order to create the required resources.
For this, follow the following steps:

1. Install `awscli`:
```bash
$ sudo apt install awscli
```

2. In AWS IAM, create a new user with `Programmatic Access`. Then `Attach existing policies directly -> AdministratorAccess`.

3. Configure `awscli`:
```bash
$ PROFILE_NAME=fibonapi-prod-terraform
$ aws configure --profile $PROFILE_NAME
AWS Access Key ID [None]:
AWS Secret Access Key [None]:
Default region name [None]: us-east-1
Default output format [None]: json
```

4. Create a new SSH to log into the EC2 instance:
```bash
$ mkdir ~/.ssh/fibonapi
$ cd ~/.ssh/fibonapi
$ ssh-keygen -t ed25519
```

5. Creat Terraform workspace (make sense when dealing with multiple environments):
```bash
$ terraform workspace new prod
```

6. Deploy the changes:
```bash
$ terraform workspace select prod
$ terraform plan
$ terraform apply
```

7. Copy the code into the EC2 instance, log into it and run the containers:
```bash
$ scp -i ~/.ssh/fibonapi/prod -r backend ubuntu@<EC2 Public IP>:/home/ubuntu
$ ssh -i ~/.ssh/fibonapi/prod ubuntu@<EC2 Public IP> # You can also configure the host in ~/.ssh/config
$ cd /home/ubuntu/backend
$ docker-compose up -d
```

Note: Remember to set the proper email address and the domain for the SSL certificate

## TODO
- [ ] Add type checking with `mypy`
- [ ] Add `pre-commit` to prevent pushing non valid commits (tests fail)
- [ ] Add GitHum action to build and push into the Container Registry (DockerHub in this case)
- [ ] Change the code to support external storage (Redis/ValKey for example)
- [ ] Add Sentry for error tracking
- [ ] Add monitoring and alarms with Prometheus and Grafana
