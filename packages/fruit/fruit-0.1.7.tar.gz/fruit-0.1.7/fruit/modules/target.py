import fruit.modules.step as step
import fruit.modules.job as job
import yaml
import click
import fruit.config as config


class fruitError(Exception):
    pass


class JobNotFoundError(Exception):
    """The requested job cannot be found"""
    pass


class Target(object):
    """
    Target class for build target functionalities.
    """

    name: str = ""  # Name of the target (build-nane)
    desc: str = ""  # Description of the target
    glob: dict = None  # List of global variables in the target
    jobs: list = None  # List of pipeline steps
    lists: list = None  # List comprehensions for commands

    def __init__(self, yaml_string: dict):
        """
        Create a new target from a parsed yaml dictionary.
        
        Parameters
        ----------
        yaml_dict : dict
            Parsed YAML dictionary from .yaml file.
        """

        yaml_dict = yaml.load(yaml_string, Loader=yaml.BaseLoader)

        # Parse the mandatory parameters
        try:
            self.name = yaml_dict['name']
            self.desc = yaml_dict['desc']
            self.glob = yaml_dict['glob']
            
            __lists = yaml_dict['lists']  # Just to verify the index

            if type(self.name) is not str:
                raise TypeError("name is not a string")
            if type(self.desc) is not str:
                raise TypeError("desc is not a string")
            
            if type(self.glob) is not dict:
                raise TypeError("glob is not a dictionary")
            
            # Verify the list
            if type(__lists) is not dict:
                raise TypeError("lists is not a dictionary")

            # Verify the list items
            for lk in __lists:
                if type(__lists[lk]) is not list:
                    raise TypeError("lists.{} is not a list".format(lk))

        except KeyError as kerr:
            raise fruitError(
                "Rotten fruit! The field {} is not found.".format(str(kerr)))
        except TypeError as te:
            raise fruitError(
                "Rotten fruit! The field {}.".format(str(te)))

        # Global variable substitution
        for each_glob in self.glob:
            yaml_string = yaml_string.replace(
                config.GLOBAL_TOKEN_FMT.format(name=each_glob),
                self.glob[each_glob]
            )
        
        # Reparse yaml for globals in lists
        yaml_dict = yaml.load(yaml_string, Loader=yaml.BaseLoader)

        # Reload the global variables after the substitution
        self.glob = yaml_dict['glob']

        self.lists = yaml_dict['lists']

        # List expansions
        for each_list in self.lists:
            yaml_string = yaml_string.replace(
                config.GLOBAL_EXPAND_FMT.format(name=each_list),
                " ".join(self.lists[each_list])
            )

        # Parse yaml again
        yaml_dict = yaml.load(yaml_string, Loader=yaml.BaseLoader)

        self.jobs = []

        # TODO: Verify unique job names
        for each_job in yaml_dict['jobs']:
            jobname = each_job
            jobyaml = yaml_dict['jobs'][jobname]
            self.jobs.append(job.create(jobname, jobyaml, self.execute))

    def execute(self, job: str):
        """
        Execute the selected fruit job in fruit.yaml
        
        Parameters
        ----------
        job : str
            Name of the job to execute. job='all' will execute all available jobs
        """

        if job == 'all':
            click.secho('Ripening \'all\' fruits... 🍏🍎')
            click.echo()

            # Execute all jobs
            for each_job in self.jobs:
                each_job.execute()
        else:
            job_flt = filter(lambda j: j.name == job, self.jobs)
            list_jobs = list(job_flt)

            if(len(list_jobs)) < 1:
                raise JobNotFoundError(
                    "The job {job} is not found.".format(job=job))
            else:
                click.secho('Ripening \'{job}\'...'.format(job=job))
                click.echo()

                # Execute the selected job
                list_jobs[0].execute()
