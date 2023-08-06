import click

from eisen_cli.train import eisen_training


@click.group()
def cli():
    pass


@click.command()
@click.argument('configuration')
@click.argument('epochs', default=10)
@click.option('--data_dir', default='./data', help='base directory where to data is placed')
@click.option('--artifact_dir', default='./artifacts', help='base directory where to store/read the artifacts')
@click.option('--resume', default=False, help='resume training from specified model training artifacts')
def train(configuration, epochs, data_dir, artifact_dir, resume):
    eisen_training(configuration, epochs, data_dir, artifact_dir, resume)


@click.command()
@click.argument('configuration')
@click.option('--data_dir', default='./data', help='base directory where to data is placed')
@click.option('--artifact_dir', default='/results/experiment', help='directory where model training artifacts reside')
def validate(configuration, data_dir, artifact_dir):
    pass


@click.command()
@click.argument('configuration')
@click.option('--data_dir', default='./data', help='base directory where to data is placed')
@click.option('--artifact_dir', default='/results/experiment', help='directory where model training artifacts reside')
def test(configuration, data_dir, artifact_dir):
    pass


@click.command()
@click.argument('configuration')
@click.option('--artifact_dir', default='/results/experiment', help='directory where model training artifacts reside')
def serve(configuration, artifact_dir):
    pass


cli.add_command(train)
cli.add_command(validate)
cli.add_command(test)
cli.add_command(serve)


if __name__ == '__main__':
    cli()
