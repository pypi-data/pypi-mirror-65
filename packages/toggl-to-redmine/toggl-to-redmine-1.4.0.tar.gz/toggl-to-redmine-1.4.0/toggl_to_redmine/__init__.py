from toggl_to_redmine.CLI import CLI
import toggl_to_redmine.options as options
import click

date_partial_help = "to get time entries. Defaults to today. Format: DD-MM-YYYY"


@click.command()
@click.option('-s', '--since', help=f"First date {date_partial_help}", callback=options.validate_date)
@click.option('-u', '--until', help=f"Last date {date_partial_help}", callback=options.validate_date)
def main(since, until):
    """ A convenient tool to import Toggl time entries to Redmine """
    cli_options = options.get_options_hash(since, until)
    CLI(cli_options).entry_point()


if __name__ == "__main__":
    main()
