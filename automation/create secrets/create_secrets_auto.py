"""

### Goal to create secrets by updating generate_env.py
# Python Script modification:          .secrets-creator-template-base/create_secrets_auto.py

Script for creating templated terragrunt.hcl files to be used to provision new
secrets. This script should be run in the root of the infrastructure-live
repo as shown below, updating values accordingly.



#TODO 1): Want script to look through direction. Check if folder/file exists. Print exists. else create it. Print created

# For example, for kms-ci
if os.path.exists(f"{os.getcwd()}/{args.aws_account_name}/{args.environment_name}/{args.aws_default_region}/{args.environment_name}/kms-ci-key"):
        print(
            f"Configuration already exists for {args.aws_account_name}/{args.environment_name}/{args.aws_default_region}/{args.environment_name}/kms-ci-key"
        )
         else:
                    output_file = "terragrunt.hcl"

                with open(f"{path}/{output_file}", "w") as _file:
                    print(f"Writing templated values to '{path}/{output_file}'")
                    _file.write(f"{parsed_template}\n")





#TODO 2): Look through all the main files in the environment 









python .account-template-base/generate_env.py \
    --aws-account-id 1234567890 \
    --aws-account-name test \
    --aws-admin-role AWSReservedSSO_Administrator_abc123 \
    --aws-deploy-role allow-auto-deploy-from-other-accounts \
    --data-custodian "John Doe" \
    --environment-name stage \
    --vpc-cidr-range "10.0.0.0/18" \
    --module-version v1.2.3
"""

import argparse
import json
import os
import sys
from shutil import copytree, ignore_patterns, move, rmtree

import requests
from jinja2 import Environment, FileSystemLoader, Template

TEMPLATE_DIR = ".account-template-base"


def cleanup(temp_dir):
    """Reset the .account-template-base directory and remove extra directories"""
    print("Cleaning up")

    for path, _, _files in os.walk(TEMPLATE_DIR):
        for _file in _files:
            if _file.endswith(".hcl") or _file.endswith(".json"):
                os.remove(os.path.join(path, _file))

    if os.path.isdir(temp_dir):
        rmtree(temp_dir, ignore_errors=True)


def get_inf_modules_release():
    """Get the current infrastructure-modules release"""
    release = requests.get(
        "https://api.github.com/repos/healthline/infrastructure-modules/releases/latest",
        auth=(None, os.getenv("GITHUB_OAUTH_TOKEN")),
    )

    json_response = json.loads(release.content.decode("utf-8"))

    return json_response["tag_name"]


def parse_args():
    """Parse arguments to build template file"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--aws-account-id",
        required=True,
        action="store",
        dest="aws_account_id",
        help="The aws account ID",
    )

    parser.add_argument(
        "--aws-account-name",
        required=True,
        action="store",
        dest="aws_account_name",
        help="The aws account Name",
    )

    parser.add_argument(
        "--aws-admin-role",
        required=True,
        action="store",
        dest="aws_admin_role",
        help="The aws admin role name",
    )

    parser.add_argument(
        "--aws-deploy-role",
        required=True,
        action="store",
        dest="aws_deploy_role",
        help="The aws auto-deploy role name",
    )

    parser.add_argument(
        "--data-custodian",
        required=True,
        action="store",
        dest="data_custodian",
        help="The data custodian for the account",
    )

    parser.add_argument(
        "--environment-name",
        required=True,
        action="store",
        dest="environment_name",
        help="The name of the environment to deploy, e.g. stage, prod",
    )

    parser.add_argument(
        "--module-version",
        required=False,
        action="store",
        dest="module_version",
        help="The default infrastructure-modules version to use",
    )

    parser.add_argument(
        "--vpc-cidr-range",
        required=True,
        action="store",
        dest="vpc_cidr_range",
        help="The vpc cidr to use for the environment (default is 10.0.0.0/18)",
    )

    args = parser.parse_args()
    # print(args)
    return args


def render_template(args, dir_path):
    """Populate template file with variables given in the script"""

    if not args.module_version:
        module_version = get_inf_modules_release()
    else:
        module_version = args.module_version

    base_arn = f"arn:aws:iam::{args.aws_account_id}"

    # Render all template files and move to correct location
    for path, _, _files in os.walk(dir_path):
        for _file in _files:
            if _file.endswith("j2"):
                env = Environment(loader=FileSystemLoader(path))
                template = env.get_template(os.path.join(_file))
                parsed_template = template.render(
                    aws_account_id=args.aws_account_id,
                    aws_account_name=args.aws_account_name,
                    admin_role=f"{base_arn}:role/aws-reserved/sso.amazonaws.com/{args.aws_admin_role}",
                    data_custodian=args.data_custodian,
                    deploy_role=f"{base_arn}:role/{args.aws_deploy_role}",
                    environment_name=args.environment_name,
                    module_version=module_version,
                    vpc_cidr_range=args.vpc_cidr_range,
                )
                if "vars.j2" in _file:
                    output_file = "_env/vars.json"
                else:
                    output_file = "terragrunt.hcl"

                with open(f"{path}/{output_file}", "w") as _file:
                    print(f"Writing templated values to '{path}/{output_file}'")
                    _file.write(f"{parsed_template}\n")


def update_dir_name(dir_path, old, new):
    """Rename config directories to the desired environment and move in to place"""
    print("Updating directory names")
    for path, subdirs, _files in os.walk(dir_path, topdown=False):
        for name in subdirs:
            if old.lower() == name.lower():
                os.rename(f"{path}/{name}", f"{path}/{new}")


def main():
    """Entrypoint"""
    args = parse_args()

    print(
        f"Setting up configuration for {args.aws_account_name}/{args.environment_name}"
    )

    if os.path.exists(f"{os.getcwd()}/{args.aws_account_name}/{args.environment_name}"):
        print(
            f"Configuration already exists for {args.aws_account_name}/{args.environment_name}"
        )
        sys.exit(0)

    # TODO Check if the cidr_range has already been used and fail if is has

    render_template(args, TEMPLATE_DIR)

    temp_dir = f"/tmp/{args.aws_account_name}"

    copytree(
        TEMPLATE_DIR,
        temp_dir,
        ignore=ignore_patterns("*.j2", "*.py"),
    )

    # Rename directory sturcture to match environment
    update_dir_name(temp_dir, "_env", args.environment_name)

    # Create base directory if it doesn't exist
    os.makedirs(f"{os.getcwd()}/{args.aws_account_name}", exist_ok=True)

    # Move rendered configs into correct location
    move(
        f"{temp_dir}/{args.environment_name}",
        f"{os.getcwd()}/{args.aws_account_name}",
    )

    print(
        f"Finished writing configurations. Check {args.aws_account_name}/{args.environment_name}/vars.json file for errors."
    )

    cleanup(temp_dir)


if __name__ == "__main__":
    main()






# Create kms-ci-key folder
if os.path.exists(f"{os.getcwd()}/{args.aws_account_name}/{args.environment_name}/{args.aws_default_region}/{args.environment_name}/kms-ci-key"):
        print(
            f"Configuration already exists for {args.aws_account_name}/{args.environment_name}/{args.aws_default_region}/{args.environment_name}/kms-ci-key"
        )
        else
