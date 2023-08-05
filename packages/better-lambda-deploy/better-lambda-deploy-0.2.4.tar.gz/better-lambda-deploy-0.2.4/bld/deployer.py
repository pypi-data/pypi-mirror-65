from .lambda_function import LambdaFunction
from .api_function import APIFunction
from jinja2 import Environment, FileSystemLoader
import os
import subprocess
import boto3
import shutil


class Deployer(object):
    def __init__(self, name, dir, docker=False, environment="prod", local=False):
        self.dir = dir
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.jinja = Environment(loader=FileSystemLoader(script_dir))
        self.project_name = name
        self.environment = environment
        self.docker = docker
        self.local = local

        # Appending the current path to grab any other files.
        os.sys.path.append(self.dir)

    def _get_env_vars(self):
        # Getting environment variables.
        env_vars = []
        for name, value in os.environ.items():
            if name[0:4] == "BLD_":
                env_vars.append(
                    {
                        "name": name[4:],
                        "alpha_name": name[4:].replace("_", ""),
                        "value": value,
                        "type": "String",
                    }
                )
        return env_vars

    def _install_reqs(self):
        reqs = os.path.abspath(f"{self.dir}/requirements.txt")
        subprocess.run(["pip", "install", "-r", reqs], check=True)

    def _build_template(self, output_dir=None):
        # Checking custom output directory.
        output_file = f"{output_dir}/bld.yml" if output_dir else "bld.yml"

        # Installing requirements so everything is importable.
        self._install_reqs()

        # Running files to create subclasses.
        # TODO: Change these from hardcoded to dynamic.
        exec(open("function.py").read())
        exec(open("api.py").read())

        # Get all Lambda Functions.
        # TODO: Check to make sure ignoring the first one is safe.
        lambda_functions = []
        lambda_classes = LambdaFunction.__subclasses__()
        lambda_classes = lambda_classes[1:]
        for lambda_class in lambda_classes:
            # inst = lambda_class()
            lambda_functions.append({"name": lambda_class.__name__})

        # Get all APIFunctions.
        api_functions = []
        api_classes = APIFunction.__subclasses__()
        for api in api_classes:
            inst = api()
            methods = inst.get_methods()
            api_functions.append(
                {"name": api.__name__, "endpoint": api.endpoint, "methods": methods}
            )

        # Creating SAM template.
        template = self.jinja.get_template("sam.j2")

        env_vars = self._get_env_vars()

        rendered = template.render(
            description="Test",
            functions=lambda_functions,
            api_functions=api_functions,
            environment_variables=env_vars,
            dynamo_tables=[],
            subdomain=self.project_name,
        )
        f = open(output_file, "w")
        f.write(rendered)
        f.close()

    def _local_build(self):
        build_path = os.path.abspath(f"{self.dir}/.aws-sam/build")
        if os.path.exists(build_path):
            shutil.rmtree(build_path)

        os.makedirs(build_path, exist_ok=True)

        # Install requirements.
        pip_cmd = ["pip", "install", "-r", "requirements.txt", "-t", build_path]
        subprocess.run(pip_cmd, cwd=self.dir)

        # Copy template in there.
        shutil.copyfile("bld.yml", f"{build_path}/template.yml")

        # Copying Python code to build directory.
        # TODO: Add symlinks for all Python files so live updated works.
        for (dirpath, dirnames, filenames) in os.walk(self.dir):
            files = list(filter(lambda x: x.endswith(".py"), filenames))
            break

        for f in files:
            shutil.copyfile(os.path.abspath(f"{dirpath}/{f}"), f"{build_path}/{f}")

    def _sam_build(self):
        # Run the SAM CLI to build and deploy.
        sam_build = ["sam", "build", "--debug", "--template-file", "bld.yml"]
        if self.docker:
            sam_build.append("--use-container")
        subprocess.run(sam_build, cwd=self.dir, check=True)

    def _build(self):
        if self.local:
            self._local_build()
        else:
            self._sam_build()

    def deploy(self):
        self._build_template()

        # Creating S3 bucket for SAM.
        # TODO: Set this to create a random bucket if the name is taken or something.
        s3 = boto3.client("s3")
        s3.create_bucket(
            ACL="private", Bucket=f"{self.project_name}-{self.environment}"
        )
        self._build()
        env_vars = self._get_env_vars()
        overrides = [
            f"ParameterKey={x['alpha_name']},ParameterValue={x['value']}"
            for x in env_vars
        ]
        sam_deploy = [
            "sam",
            "deploy",
            "--stack-name",
            f"{self.project_name}-{self.environment}",
            "--capabilities",
            "CAPABILITY_NAMED_IAM",
            "--s3-bucket",
            f"{self.project_name}-{self.environment}",
            "--template-file",
            ".aws-sam/build/template.yml",
            "--parameter-overrides",
            f"ENVIRONMENT={self.environment}",
        ]
        if len(overrides) > 0:
            sam_deploy.append(",".join(overrides))
        subprocess.run(sam_deploy, cwd=self.dir, check=True)

        print("Deployed successfully.")

    def start_api(self):
        self._build_template()
        self._build()

        env_vars = self._get_env_vars()
        overrides = [f"{x['alpha_name']}={x['value']}" for x in env_vars]
        overrides.append("ENVIRONMENT=sam")
        sam_start = [
            "sam",
            "local",
            "start-api",
            "-d 5858",
            "--template-file",
            ".aws-sam/build/template.yml",
        ]
        if len(overrides) > 0:
            sam_start.append("--parameter-overrides")
            sam_start.append(",".join(overrides))

        subprocess.run(sam_start, cwd=self.dir, check=True)

    def invoke(self, function):
        self._build_template()
        self._build()
        subprocess.run(["sam", "local", "invoke", function], cwd=self.dir, check=True)
