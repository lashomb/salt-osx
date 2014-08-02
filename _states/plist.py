# -*- coding: utf-8 -*-
"""
Management of preference list values
====================================

Management of specific keys and their values can be done using these states.

.. code-block:: yaml

    /Library/Preferences/x.plist:
        plist.managed_keys:
            - key:
                nested_key: 'value'
            - key_two: True

.. note::

    This uses native API by default, and therefore should be safe with files managed by cfprefsd.

"""
import salt.utils


def __virtual__():
    """Only load on OSX"""
    return 'plist' if salt.utils.is_darwin() else False


def managed_keys(name, **keys):
    """
    This function manages a specific list of keys within a named property list file.

    name
        The name of the property list file to manage.

    keys
        Every other property of this state is used to describe a key hierarchy and a value to manage.

        When describing key values in YAML, you are restricted to types easily translated.

    """
    ret = {'name':name, 'result':False, 'changes':{}, 'comment':''}
    changes = {'old': __salt__['plist.read_keys'](name, keys), 'new': {}}

    changed = __salt__['plist.write_keys'](name, keys, __opts__['test'])

    if changed:
        changes['new'] = changed
        ret['changes'] = changes

    if __opts__['test'] == True:
        ret['comment'] = 'Values will be changed' if changed else 'No changes will be required'
        ret['result'] = None
    else:
        ret['comment'] = 'Values changed' if changed else 'No changes required'
        ret['result'] = True if changed else None

    return ret