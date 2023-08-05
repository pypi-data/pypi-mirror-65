import inspect

from aistac.properties.master_ledger_property_manager import MasterLedgerPropertyManager
from aistac.intent.abstract_intent import AbstractIntentModel

__author__ = 'Darryl Oatridge'


class MasterLedgerIntentModel(AbstractIntentModel):

    def __init__(self, property_manager: MasterLedgerPropertyManager, default_save_intent: bool=None,
                 default_intent_level: [str, int, float]=None, default_replace_intent: bool=None,
                 intent_type_additions: list=None):
        """initialisation of the Intent class.

        :param property_manager: the property manager class that references the intent contract.
        :param default_save_intent: (optional) The default action for saving intent in the property manager
        :param default_intent_level: (optional) The default intent level
        :param default_replace_intent: (optional) The default replace intent
        :param intent_type_additions: (optional) if the intent parameters have extra types beyond standard
        """
        default_save_intent = default_save_intent if isinstance(default_save_intent, bool) else True
        default_intent_level = default_intent_level if isinstance(default_intent_level, (str, int, float)) else 0
        default_replace_intent = default_replace_intent if isinstance(default_replace_intent, bool) else True
        intent_param_exclude = ['inplace', 'canonical']
        intent_type_additions = intent_type_additions if isinstance(intent_type_additions, list) else list()
        super().__init__(property_manager=property_manager, default_save_intent=default_save_intent,
                         intent_param_exclude=intent_param_exclude, default_intent_level=default_intent_level,
                         default_replace_intent=default_replace_intent, intent_type_additions=intent_type_additions)

    def run_intent_pipeline(self, intent_levels: [int, str, list], **kwargs):
        pass

    def replace_uri(self, components: dict, old: str, new: str, save_intent: bool=True,
                    replace_intent: bool=None,  intent_level: [int, str]=None):
        """ resets the list of contract names provided

        :param components: a dictionary of components in the form {manager: [tasks_list]}
        :param old: the old uri or part uri
        :param new: the new uri or part uri to replace the old with
        :param save_intent (optional) if the intent contract should be saved to the property manager
        :param replace_intent: (optional) if the intent exists replace
        :param intent_level: (optional) a level to place the intent
        :return:
        """
        # resolve intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, save_intent=save_intent, replace_intent=replace_intent)
        # intend code block on the canonical

    def set_source_from_template(self, components: dict, save_intent: bool=True, replace_intent: bool=None,
                                 intent_level: [int, str]=None):
        """ resets the list of contract names provided

        :param components: a dictionary of components in the form {manager: [tasks_list]}
        :param save_intent (optional) if the intent contract should be saved to the property manager
        :param replace_intent: (optional) if the intent exists replace
        :param intent_level: (optional) a level to place the intent
        :return:
        """
        # resolve intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, save_intent=save_intent, replace_intent=replace_intent)
        # intend code block on the canonical

    def set_persist_from_template(self, components: dict, save_intent: bool=True, replace_intent: bool=None,
                                  intent_level: [int, str]=None):
        """ resets the list of contract names provided

        :param components: a dictionary of components in the form {manager: [tasks_list]}
        :param save_intent (optional) if the intent contract should be saved to the property manager
        :param replace_intent: (optional) if the intent exists replace
        :param intent_level: (optional) a level to place the intent
        :return:
        """
        # resolve intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, save_intent=save_intent, replace_intent=replace_intent)
        # intend code block on the canonical
