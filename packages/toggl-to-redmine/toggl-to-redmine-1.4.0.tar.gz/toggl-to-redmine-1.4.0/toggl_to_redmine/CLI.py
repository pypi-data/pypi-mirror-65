from pathlib import Path
from toggl_to_redmine_core.toggl_to_redmine import toggl_to_redmine
from toggl_to_redmine_core.exceptions import *
from .config_manager import ConfigManager
import click
import logging


class CLI():
    """ Concrete class to provide CLI functionality to Toggl to Redmine """

    def __init__(self, config_options):
        self.config_manager = ConfigManager(config_options)
        self.config = {}
        self.entries_saved = []

    def entry_point(self):
        try:
            self.config = self.config_manager.get_config()
            self.import_output = self.run_app()
            self.show_entries_saved()
            self.show_entries_not_saved()
        except ConfigException:
            self.handle_config_problem()
        except (TogglCommunicationException, RedmineServerError):
            self.handle_services_unavailable()
        except (TogglCredentialsException, RedmineAuthException) as e:
            self.handle_credentials_problem(e)
        except Exception as e:
            self.handle_the_unknown(e)

    def run_app(self):
        return toggl_to_redmine(self.config)

    def show_entries_saved(self):
        click.echo("\nRecords saved:")
        for entry in self.import_output['entries_saved']:
            click.echo(
                f'{entry.issue_id}: {entry.comment} ({entry.timestamp})')
        click.echo()
    
    def show_entries_not_saved(self):
        click.echo("\n\nRecords that were not saved:")
        for entry in self.import_output['entries_not_saved']:
            click.echo(
                f'{entry.id}: {entry.comment} ({entry.timestamp}) Message: {entry.message}')
        click.echo()

    def handle_config_problem(self):
        click.echo('\nHello! We need to setup your configs on Toggl-to-Redmine.')
        self.config_manager.reset_config()
        self.entry_point()

    def handle_services_unavailable(self):
        click.echo("\nIt looks like Toggl or Redmine App are not available.")
        click.echo("\nCheck if these services are online and try again.")

    def handle_credentials_problem(self, exception: Exception):
        message = exception.args[0]['error']['message']
        click.echo("\nThere was a problem with your credentials.")
        click.echo(f"Error message: {message}")

        if click.confirm("\nWould you like to inform your config data again?"):
            self.handle_config_problem()
        else:
            click.echo("\nYou could take a look in the config file, then.")

    def handle_the_unknown(self, exception: Exception):
        click.echo(
            "Something unexpected happened. Contact the package maintainer.\n")
        if click.confirm('Would you like to see the exception?'):
            logging.exception(exception)
