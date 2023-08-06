# vim:fileencoding=utf-8:noet
from __future__ import (unicode_literals, division, absolute_import, print_function)

from powerline.theme import requires_segment_info


@requires_segment_info
def exit_status(pl, segment_info, only_failed=False, style='code'):
    '''Return last exit status

    :param bool only_failed:
        If False (default) shows exit status always. Otherwise shows only
        fail status and does't show success status.

    :param str style:
        Style the segment depending on value. Accepted values:
        symbol, color, code, None

    Highlight groups used: ``exit_status_fail``, ``exit_status_success``
    '''
    exit_code = segment_info['args'].last_exit_code
    if not exit_code:
        if only_failed:
            return None
        elif str(style) == 'symbol':
        	retval = '\u2714'
        elif str(style) == 'color':
        	retval = ''
        elif str(style) == 'code':
        	retval = str(exit_code)
        return [{'contents': retval, 'highlight_groups': ['exit_status_success']}]
    if str(style) == 'symbol':
    	retval = '\u2715'
    elif str(style) == 'color':
        retval = ''
    elif str(style) == 'code':
        retval = str(exit_code)
    return [{'contents': retval, 'highlight_groups': ['exit_status_fail']}]
