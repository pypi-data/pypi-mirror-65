from aistac.components.abstract_component import AbstractComponent
from aistac.intent.master_ledger_intent_model import MasterLedgerIntentModel
from aistac.properties.abstract_properties import AbstractPropertyManager
from aistac.properties.master_ledger_property_manager import MasterLedgerPropertyManager

__author__ = 'Darryl Oatridge'


class MasterLedger(AbstractComponent):

    def __init__(self, property_manager: MasterLedgerPropertyManager, intent_model: MasterLedgerIntentModel,
                 default_save=None, reset_templates: bool=None, align_connectors: bool=None):
        """ Encapsulation class for the transition set of classes

        :param property_manager: The contract property manager instance for this component
        :param intent_model: the model codebase containing the parameterizable intent
        :param default_save: The default behaviour of persisting the contracts:
                    if False: The connector contracts are kept in memory (useful for restricted file systems)
        :param reset_templates: (optional) reset connector templates from environ variables (see `report_environ()`)
        :param align_connectors: (optional) resets aligned connectors to the template
        """
        super().__init__(property_manager=property_manager, intent_model=intent_model, default_save=default_save,
                         reset_templates=reset_templates, align_connectors=align_connectors)

    @classmethod
    def from_uri(cls, task_name: str, uri_pm_path: str, pm_file_type: str=None, pm_module: str=None,
                 pm_handler: str=None, pm_kwargs: dict=None, default_save=None, reset_templates: bool=None,
                 align_connectors: bool=None):
        """ Class Factory Method to instantiates the components application. The Factory Method handles the
        instantiation of the Properties Manager, the Intent Model and the persistence of the uploaded properties.
        See class inline docs for an example method

         :param task_name: The reference name that uniquely identifies a task or subset of the property manager
         :param uri_pm_path: A URI that identifies the resource path for the property manager.
         :param pm_file_type: (optional) defines a specific file type for the property manager
         :param pm_module: (optional) the module or package name where the handler can be found
         :param pm_handler: (optional) the handler for retrieving the resource
         :param pm_kwargs: (optional) a dictionary of kwargs to pass to the property manager
         :param default_save: (optional) if the configuration should be persisted. default to 'True'
         :param reset_templates: (optional) reset connector templates from environ variables. Default True
                                (see `report_environ()`)
         :param align_connectors: (optional) resets aligned connectors to the template. default Default True
         :return: the initialised class instance
         """
        pm_file_type = pm_file_type if isinstance(pm_file_type, str) else 'pickle'
        pm_module = pm_module if isinstance(pm_module, str) else 'aistac.handlers.python_handlers'
        pm_handler = pm_handler if isinstance(pm_handler, str) else 'PythonPersistHandler'
        _pm = MasterLedgerPropertyManager(task_name=task_name)
        _intent_model = MasterLedgerIntentModel(property_manager=_pm)
        super()._init_properties(property_manager=_pm, uri_pm_path=uri_pm_path, pm_file_type=pm_file_type,
                                 pm_module=pm_module, pm_handler=pm_handler, pm_kwargs=pm_kwargs)
        return cls(property_manager=_pm, intent_model=_intent_model, default_save=default_save,
                   reset_templates=reset_templates, align_connectors=align_connectors)

    @classmethod
    def from_env(cls, task_name: str=None, default_save=None, **kwargs):
        """

        :param task_name: (optional) a name option for the Master Ledger
        :param default_save: (optional) if the configuration should be persisted
        :return: the initialised class instance
        """
        task_name = task_name if isinstance(task_name, str) else 'ledger'
        return super().from_env(task_name=task_name, default_save=default_save)

    @property
    def pm(self) -> MasterLedgerPropertyManager:
        return self._component_pm

    @property
    def intent_model(self) -> MasterLedgerIntentModel:
        return self._intent_model

    def add_ledger_pm(self, property_manager: AbstractPropertyManager, save: bool=None):
        """ adds a pm to the ledger

        :param property_manager: the instance of the property manager to add
        :param save: (optional) override of the default save action set at initialisation.
       """
        save = save if isinstance(save, bool) else self._default_save
        self.pm.set_ledger_pm(property_manager)
        self.pm_persist(save)

    def remove_ledger_pm(self, manager: str, task: str, save: bool=None):
        """ removes a pm from the ledger

        :param manager: The name of the component manager
        :param task: The name of the manager task
        :param save: (optional) override of the default save action set at initialisation.
        :return True if removed, False if not
        """
        save = save if isinstance(save, bool) else self._default_save
        result = self.pm.remove_ledger_pm(manager=manager, task=task)
        self.pm_persist(save)
        return result
