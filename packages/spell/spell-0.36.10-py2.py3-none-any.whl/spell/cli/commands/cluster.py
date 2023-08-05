# -*- coding: utf-8 -*-
import click

from spell.cli.commands.cluster_aws import (
    create_aws,
    eks_init,
    add_s3_bucket,
    update_aws_cluster,
    delete_aws_cluster,
)
from spell.cli.commands.cluster_aws import add_ec_registry, delete_ec_registry
from spell.cli.commands.cluster_gcp import (
    create_gcp,
    gke_init,
    add_gs_bucket,
    update_gcp_cluster,
    delete_gcp_cluster,
)
from spell.cli.commands.cluster_gcp import add_gc_registry, delete_gc_registry
from spell.cli.commands.machine_type import (
    add_machine_type,
    scale_machine_type,
    delete_machine_type,
)
from spell.cli.utils import cluster_utils, tabulate_rows, HiddenOption
from spell.cli.exceptions import api_client_exception_handler, ExitException


@click.group(
    name="cluster",
    short_help="Manage external clusters",
    help="Manage external clusters on Spell\n\n"
    "With no subcommand, display all your external clusters",
    invoke_without_command=True,
)
@click.pass_context
def cluster(ctx):
    """
    List all external clusters for current owner
    """
    if ctx.invoked_subcommand:
        return

    spell_client = ctx.obj["client"]
    # TODO(ian) Allow read access to 'member' role
    cluster_utils.validate_org_perms(spell_client, ctx.obj["owner"])
    clusters = spell_client.list_clusters()
    if len(clusters) == 0:
        click.echo("There are no external clusters to display.")
        return

    def create_row(cluster):
        provider = cluster["cloud_provider"]
        networking = cluster["networking"][provider.lower()]
        vpc = networking["vpc_id"] if provider == "AWS" else networking["vpc"]
        return (
            cluster["name"],
            provider,
            cluster["storage_uri"],
            vpc,
            networking["region"],
            cluster["version"],
            cluster["has_kube_config"],
        )

    tabulate_rows(
        [create_row(c) for c in clusters],
        headers=[
            "NAME",
            "PROVIDER",
            "BUCKET NAME",
            "VPC",
            "REGION",
            "CLUSTER VERSION",
            "MODEL SERVING ENABLED",
        ],
    )


@click.command(name="add-bucket", short_help="Adds a cloud storage bucket to SpellFS")
@click.pass_context
@click.option("--bucket", "bucket_name", help="Name of bucket")
@click.option(
    "--cluster-name", default=None, help="Name of cluster to add bucket permissions to"
)
@click.option(
    "-p",
    "--profile",
    "profile",
    default=u"default",
    help="This AWS profile will be used to get your Access Key ID and Secret as well as your Region. "
    "You will be prompted to confirm the Key and Region are correct before continuing. "
    "This key will be used to adjust IAM permissions of the role associated with the cluster "
    "that the bucket is being added to.",
)
def add_bucket(ctx, bucket_name, cluster_name, profile):
    """
    This command adds a cloud storage bucket (S3 or GS) to SpellFS, which enables interaction with the bucket objects
    via ls, cp, and mounts. It will also updates the permissions of that bucket to allow Spell read access to it
    """
    cluster = deduce_cluster(ctx, cluster_name)

    cluster_type = cluster["cloud_provider"]
    if cluster_type == "AWS":
        ctx.invoke(
            add_s3_bucket, bucket_name=bucket_name, cluster=cluster, profile=profile
        )
    elif cluster_type == "GCP":
        if profile != "default":
            click.echo("--profile is not a valid option for adding a gs bucket")
            return
        ctx.invoke(add_gs_bucket, bucket_name=bucket_name, cluster=cluster)
    else:
        raise Exception(
            "Unknown cluster with provider {}, exiting.".format(cluster_type)
        )


@click.command(
    name="add-docker-registry",
    short_help="Configures your cluster to enable runs with docker images in the private registry"
    " hosted by your cloud provider (ECR or GCR respectively)",
)
@click.pass_context
@click.option(
    "--cluster-name",
    default=None,
    help="Name of cluster to add registry permissions to",
)
@click.option("--repo", "repo_name", help="Name of repository. ECR only")
@click.option(
    "-p",
    "--profile",
    "profile",
    default=u"default",
    help="This AWS profile will be used to get your Access Key ID and Secret as well as your Region. "
    "You will be prompted to confirm the Key and Region are correct before continuing. "
    "This key will be used to adjust IAM permissions of the role associated with the cluster "
    "that needs access to the registry.",
)
def add_docker_registry(ctx, cluster_name, repo_name, profile):
    """
    This command enables pulling docker images from a private registry.
    Read permissions to the registry will be added to the IAM role associated with the cluster.
    """
    cluster = deduce_cluster(ctx, cluster_name)

    cluster_type = cluster["cloud_provider"]
    if cluster_type == "AWS":
        ctx.invoke(
            add_ec_registry, repo_name=repo_name, cluster=cluster, profile=profile
        )
    elif cluster_type == "GCP":
        if profile != "default":
            click.echo("--profile is not a valid option for adding a gs bucket")
            return
        ctx.invoke(add_gc_registry, cluster=cluster)
    else:
        raise ExitException(
            "Unknown cluster with provider {}, exiting.".format(cluster_type)
        )


@click.command(
    name="delete-docker-registry",
    short_help="Removes your cluster's access to docker images in the private registry"
    " hosted by your cloud provider (ECR or GCR respectively).",
)
@click.pass_context
@click.option("--repo", "repo_name", help="Name of repository. ECR only")
@click.option(
    "--cluster-name",
    default=None,
    help="Name of cluster to remove registry permissions from",
)
@click.option(
    "-p",
    "--profile",
    "profile",
    default=u"default",
    help="This AWS profile will be used to get your Access Key ID and Secret as well as your Region. "
    "You will be prompted to confirm the Key and Region are correct before continuing. "
    "This key will be used to adjust IAM permissions of the role associated with the cluster "
    "that has access to the registry.",
)
def delete_docker_registry(ctx, cluster_name, repo_name, profile):
    """
    This command removes your cluster's access to docker images in the private registry hosted by your cloud provider.
    """
    cluster = deduce_cluster(ctx, cluster_name)

    cluster_type = cluster["cloud_provider"]
    if cluster_type == "AWS":
        ctx.invoke(
            delete_ec_registry, repo_name=repo_name, cluster=cluster, profile=profile
        )
    elif cluster_type == "GCP":
        if profile != "default":
            click.echo("--profile is not a valid option for adding a gs bucket")
            return
        ctx.invoke(delete_gc_registry, cluster=cluster)
    else:
        raise ExitException(
            "Unknown cluster with provider {}, exiting.".format(cluster_type)
        )


def deduce_cluster(ctx, cluster_name):
    spell_client = ctx.obj["client"]
    cluster_utils.validate_org_perms(spell_client, ctx.obj["owner"])

    clusters = spell_client.list_clusters()
    if len(clusters) == 0:
        click.echo(
            "No clusters defined, please run `spell cluster init aws` or `spell cluster init gcp`"
        )
        return
    while len(clusters) != 1:
        if cluster_name is not None:
            clusters = [c for c in clusters if c["name"] == cluster_name]
        if len(clusters) == 0:
            click.echo("No clusters with the name {}, please try again.")
            return
        elif len(clusters) > 1:  # two or more clusters
            cluster_names = [c["name"] for c in clusters]
            cluster_name = click.prompt(
                "You have multiple clusters defined. Please select one.",
                type=click.Choice(cluster_names),
            ).strip()
    cluster = clusters[0]

    return cluster


@click.command(
    name="update",
    short_help="Makes sure your Spell cluster is fully up to date and able to support the latest features",
)
@click.pass_context
@click.option("--cluster-name", default=None, help="Name of cluster to update")
@click.option(
    "-p",
    "--profile",
    "profile",
    default=u"default",
    help="This AWS profile will be used to get your Access Key ID and Secret as well as your Region. "
    "You will be prompted to confirm the Key and Region are correct before continuing. "
    "This key will be used to adjust IAM permissions of the role associated with the cluster "
    "that the bucket is being added to.",
)
def update(ctx, cluster_name, profile):
    """
    This command makes sure your Spell cluster is fully up to date and able to support the latest features
    """
    cluster = deduce_cluster(ctx, cluster_name)

    cluster_type = cluster["cloud_provider"]
    if cluster_type == "AWS":
        ctx.invoke(update_aws_cluster, cluster=cluster, profile=profile)
    elif cluster_type == "GCP":
        if profile != "default":
            click.echo("--profile is not a valid option for adding a gs bucket")
            return
        ctx.invoke(update_gcp_cluster, cluster=cluster)
    else:
        raise Exception(
            "Unknown cluster with provider {}, exiting.".format(cluster_type)
        )


@click.command(
    name="init-model-server",
    short_help="Sets up a GKE/EKS cluster to host model servers",
    help="Sets up a GKE or EKS cluster to host model servers",
)
@click.pass_context
@click.option(
    "-c",
    "--cluster",
    "cluster_name",
    type=str,
    help="The name of the Spell cluster that you would like to configure this "
    "model serving cluster to work with. If it's not specified, it will default to "
    "the ONE cluster the current owner has, or fail if the current owner has more than one cluster.",
)
@click.option(
    "--model-serving-cluster",
    type=str,
    default="spell-model-serving",
    help="Name of the newly created GKE/EKS cluster",
)
@click.option(
    "--auth-api-url",
    cls=HiddenOption,
    type=str,
    help="URL of the spell API server used by Ambassador for authentication. "
    "This must be externally accessible",
)
@click.option(
    "--nodes-min",
    type=int,
    default=1,
    help="Minimum number of nodes in the model serving cluster (default 1)",
)
@click.option(
    "--nodes-max",
    type=int,
    default=2,
    help="Minimum number of nodes in the model serving cluster (default 2)",
)
@click.option(
    "--node-disk-size",
    type=int,
    default=50,
    help="Size of disks on each node in GB (default 50GB)",
)
@click.option(
    "--aws-zones",
    type=str,
    default=None,
    help="Allows AWS clusters to explicitly list the availability zones used for the EKS cluster. "
    "List the desired AZs as comma separated values, ex: 'us-east-1a,us-east-1c,us-east-1d'. "
    "NOTE: Most users will NOT have to do this. This is useful if there are problems with "
    "one or more of the AZs in the region of your cluster.",
)
def init_model_server(
    ctx,
    cluster_name,
    model_serving_cluster,
    auth_api_url,
    nodes_min,
    nodes_max,
    node_disk_size,
    aws_zones,
):
    """
    Deploy a GKE or EKS cluster for model serving
    by auto-detecting the cluster provider.
    """
    spell_client = ctx.obj["client"]
    cluster_utils.validate_org_perms(spell_client, ctx.obj["owner"])
    with api_client_exception_handler():
        cluster = cluster_utils.get_spell_cluster(
            spell_client, ctx.obj["owner"], cluster_name
        )
    if cluster["cloud_provider"] == "AWS":
        eks_init(
            ctx,
            cluster,
            auth_api_url,
            model_serving_cluster,
            nodes_min,
            nodes_max,
            node_disk_size,
            aws_zones,
        )
    elif cluster["cloud_provider"] == "GCP":
        gke_init(
            ctx,
            cluster,
            auth_api_url,
            model_serving_cluster,
            nodes_min,
            nodes_max,
            node_disk_size,
        )
    else:
        raise ExitException(
            "Unsupported cloud provider: {}".format(cluster["cloud_provider"])
        )


@click.command(
    name="delete",
    short_help="Deletes a given cluster",
    help="Facilitates the deletion of your Spell cluster by removing the associated "
    "infrastructure on Spell as well as deleting all associated cloud resources. "
    "It will OPTIONALLY delete the data in your output bucket - including run outputs.",
)
@click.pass_context
@click.option(
    "-c",
    "--cluster",
    "cluster_name",
    type=str,
    help="The name of the Spell cluster that you would like to delete. "
    "If it's not specified, it will default to the ONE cluster the current owner has, "
    "or prompt if the current owner has more than one cluster.",
)
@click.option(
    "-p",
    "--profile",
    "profile",
    help="This AWS profile will be used to get your Access Key ID and Secret as well as your Region. "
    "You will be prompted to confirm the Key and Region are correct before continuing. "
    "This key will be used to destroy the VPC, IAM Roles, and optionally the S3 bucket "
    "created for the cluster.",
)
# If this cluster was constructed in an existing VPC (likely in on-prem mode) this option will prevent
# the vpc from being deleted
@click.option("--keep-vpc", "keep_vpc", is_flag=True, hidden=True)
def delete(ctx, cluster_name, profile, keep_vpc):
    cluster = deduce_cluster(ctx, cluster_name)
    if cluster is None:
        return

    cluster_type = cluster["cloud_provider"]
    if cluster_type == "AWS":
        delete_aws_cluster(ctx, cluster, profile, keep_vpc)
    elif cluster_type == "GCP":
        if keep_vpc:
            click.echo(
                "--keep-vpc is not currently supported for GCP. Contact Spell for support."
            )
        if profile:
            click.echo("--profile is not a valid option for deleting a GCP cluster")
            return
        delete_gcp_cluster(ctx, cluster)
    else:
        raise Exception(
            "Unknown cluster with provider {}, exiting.".format(cluster_type)
        )


@cluster.group(
    name="init",
    short_help="Create a cluster",
    help="Create a new aws/gcp cluster for your org account\n\n"
    "Set up a cluster to use machines in your own AWS/GCP account",
)
@click.pass_context
def init(ctx):
    pass


@cluster.group(
    name="machine-type",
    short_help="Manage machine types",
    help="Manage groups of similar machines which can be used for training runs and workspaces on Spell\n\n"
    "With no subcommand, display all your machine types",
    invoke_without_command=True,
)
@click.option(
    "-c", "--cluster", "cluster_name", type=str, help="The name of the Spell cluster"
)
@click.pass_context
def machine_type(ctx, cluster_name):
    # TODO(ian) Allow read access to 'member' role
    ctx.obj["cluster"] = deduce_cluster(ctx, cluster_name)
    if ctx.invoked_subcommand:
        return

    def create_row(machine_type):
        machines = machine_type["machines"]
        return (
            machine_type["name"],
            machine_type["spell_type"],
            machine_type["is_spot"],
            machine_type["instance_spec"]["storage_size"],
            ", ".join(machine_type["warm_frameworks"]),
            machine_type["created_at"].strftime("%b %d, %Y"),
            machine_type["updated_at"].strftime("%b %d, %Y"),
            machine_type["min_instances"],
            machine_type["max_instances"],
            machine_type["idle_timeout_seconds"] / 60,
            len([m for m in machines if m["status"] == "Starting"]),
            len([m for m in machines if m["status"] == "Idle"]),
            len([m for m in machines if m["status"] == "In use"]),
        )

    machine_types = ctx.obj["cluster"]["machine_types"]
    tabulate_rows(
        [create_row(mt) for mt in machine_types],
        headers=[
            "NAME",
            "TYPE",
            "SPOT",
            "DISK SIZE",
            "IMAGES",
            "CREATED",
            "LAST MODIFIED",
            "MIN",
            "MAX",
            "IDLE TIMEOUT",
            "STARTING",
            "IDLE",
            "IN USE",
        ],
    )


# register generic subcommands
cluster.add_command(add_bucket)
cluster.add_command(add_docker_registry)
cluster.add_command(delete_docker_registry)
cluster.add_command(update)
cluster.add_command(delete)
# register gke/eks subcommands
cluster.add_command(init_model_server)

# register init subcommands
init.add_command(create_aws)
init.add_command(create_gcp)

# register machine-type subcommands
machine_type.add_command(add_machine_type)
machine_type.add_command(scale_machine_type)
machine_type.add_command(delete_machine_type)
