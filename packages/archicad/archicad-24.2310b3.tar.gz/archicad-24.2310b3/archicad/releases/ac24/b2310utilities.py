import os, sys, subprocess
from typing import Optional, Union, Tuple, List, Callable
from archicad.releases.ac24.b2310types import *
from archicad.releases.ac24.b2310commands import *


def _find_in_tree(treeRootItem, itemattr, childrenattr, criterion) -> list:
    result = []
    if criterion(treeRootItem):
        result.append(treeRootItem)
    if treeRootItem.__getattribute__(childrenattr):
        for node in treeRootItem.__getattribute__(childrenattr):
            result.extend(_find_in_tree(node.__getattribute__(itemattr), itemattr, childrenattr, criterion))
    return result


class Utilities:
    """ Utility functions for the archicad module.
    """
    def __init__(self, actypes: Types, accommands: Commands):
        self.actypes = actypes
        self.accommands = accommands

    @staticmethod
    def OpenFile(filepath: str):
        """Opens the given file with the default application."""
        if sys.platform == "win32":
            os.startfile(filepath)
        else:
            subprocess.call(["open" if sys.platform == "darwin" else "xdg-open", filepath])

    @staticmethod
    def FindInNavigatorItemTree(treeRootItem: NavigatorItem,
                                criterion: Callable[[NavigatorItem], bool]) -> List[NavigatorItem]:
        """Finds items in a navigator tree.
        
        Args:
            treeRootItem (:obj:`NavigatorItem`): The root item of the navigator tree.
            criterion (Callable[[NavigatorItem], bool]): The criterion function.
        
        Returns:
            :obj:`List[NavigatorItem]`: The list of navigator items, which fulfill the criterion function.
        """
        return _find_in_tree(treeRootItem, 'navigatorItem', 'children', criterion)

    @staticmethod
    def FindInClassificationItemTree(treeRootItem: ClassificationItemInTree,
                                     criterion: Callable[[ClassificationItemInTree], bool]) -> List[ClassificationItemInTree]:
        """Finds items in a navigator tree.
        
        Args:
            treeRootItem (:obj:`ClassificationItemInTree`): The root item of the classification tree.
            criterion (Callable[[ClassificationItemInTree], bool]): The criterion function.
        
        Returns:
            :obj:`List[ClassificationItemInTree]`: The list of classification items, which fulfill the criterion function.
        """
        return _find_in_tree(treeRootItem, 'classificationItem', 'children', criterion)

    def FindClassificationItemInSystem(self, system_name: str, item_id: str) -> Optional[ClassificationItemId]:
        """Finds the classification item in a system."""
        system_id = next(system.classificationSystemId for system in
                            self.accommands.GetAllClassificationSystems() if system.name == system_name)
        classifications_tree = self.accommands.GetAllClassificationsInSystem(system_id)
        for tree in classifications_tree:
            classification_ids = Utilities.FindInClassificationItemTree(tree.classificationItem, lambda c: c.id == item_id)
            assert len(classification_ids) <= 1
            if classification_ids:
                return classification_ids[0]
        return None
    
    def GetBuiltInPropertyId(self, name: str) -> PropertyId:
        """Returns the PropertyId of the corresponding built-in property."""
        return self.accommands.GetPropertyIds([BuiltInPropertyUserId(name)])[0].propertyId

    def GetUserDefinedPropertyId(self, groupName: str, name: str) -> PropertyId:
        """Returns the PropertyId of the corresponding user-defined property."""
        return self.accommands.GetPropertyIds([UserDefinedPropertyUserId([groupName, name])])[0].propertyId
