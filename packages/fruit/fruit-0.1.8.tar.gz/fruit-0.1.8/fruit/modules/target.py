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

class TargetParseError(Exception):
    """Error while parsing a target"""
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

            self.__load_glob(yaml_dict=yaml_dict) # Load globals via a loader function

            if type(self.name) is not str:
                raise TypeError("name is not a string")
            if type(self.desc) is not str:
                raise TypeError("desc is not a string")

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
        self.__load_glob(yaml_dict=yaml_dict)

        self.__load_lists(yaml_dict=yaml_dict)

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

    def __load_glob(self, yaml_dict: dict):
        """
        Load the global variables into `self.glob` when the field is found.
        
        Parameters
        ----------
        `yaml_dict` : dict
            YAML dictionary of the target
        """

        if 'glob' in yaml_dict.keys():
            glob = yaml_dict['glob']

            if type(glob) is not dict:
                raise TargetParseError("The field glob must be a dictionary!")

            for each_key in glob:
                if type(glob[each_key]) is not str:
                    raise TargetParseError("The glob field is not formatted correctly!")
            
            # All test were successful
            self.glob = glob
        else:
            # When the field is nonexistent, use an empty dict
            self.glob = {}

    def __load_lists(self, yaml_dict: dict) -> None:
        """
        Load the lists from the yaml dictionary. Use an empty list when the
        field was left empty.
        
        Parameters
        ----------
        `yaml_dict` : dict
            YAML dictionary of the target
        """
        if 'lists' in yaml_dict.keys():
            lst = yaml_dict['lists']

            if type(lst) is not dict:
                raise TargetParseError("The field lists must be a dictionary!")

            for each_key in lst:
                if type(lst[each_key]) is not list:
                    raise TargetParseError("The lists field is not formatted correctly!")

            self.lists = lst
        else:
            # Initialize with empty list
            self.lists = []
    
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
