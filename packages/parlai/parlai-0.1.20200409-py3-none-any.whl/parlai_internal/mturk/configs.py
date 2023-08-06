#!/usr/bin/env python3
def force_opt(opts, opt_name, opt_val):
    if opts[opt_name] != opt_val:
        print("[FBInternal Parlai Config] Overriding {} to {}"
              "".format(opt_name, opt_val))
    opts[opt_name] = opt_val


def apply_default_opts(opts):
    # TODO re-enable max time once the infrastructure to support it is in place
    # force_opt(opts, 'max_time', 60*60*3.5)
    # force_opt(opts, 'max_time_qual', 'max_time_on_noah_hits_per_day')
    return opts


def set_default_qualifications(quals):
    fin_quals = [{
        'QualificationTypeId': '00000000000000000071',
        'Comparator': 'In',
        'LocaleValues': [
            {'Country': 'US', 'Subdivision': 'AL'},
            {'Country': 'US', 'Subdivision': 'AR'},
            {'Country': 'US', 'Subdivision': 'DE'},
            {'Country': 'US', 'Subdivision': 'FL'},
            {'Country': 'US', 'Subdivision': 'GA'},
            {'Country': 'US', 'Subdivision': 'IA'},
            {'Country': 'US', 'Subdivision': 'KS'},
            {'Country': 'US', 'Subdivision': 'KY'},
            {'Country': 'US', 'Subdivision': 'LA'},
            {'Country': 'US', 'Subdivision': 'MD'},
            {'Country': 'US', 'Subdivision': 'MN'},
            {'Country': 'US', 'Subdivision': 'MS'},
            {'Country': 'US', 'Subdivision': 'MO'},
            {'Country': 'US', 'Subdivision': 'NE'},
            {'Country': 'US', 'Subdivision': 'ND'},
            {'Country': 'US', 'Subdivision': 'OK'},
            {'Country': 'US', 'Subdivision': 'SC'},
            {'Country': 'US', 'Subdivision': 'SD'},
            {'Country': 'US', 'Subdivision': 'TN'},
            {'Country': 'US', 'Subdivision': 'TX'},
            {'Country': 'US', 'Subdivision': 'VA'},
            {'Country': 'US', 'Subdivision': 'WV'},
            {'Country': 'CA'},
            {'Country': 'GB'},
            {'Country': 'AU'},
            {'Country': 'NZ'}
        ],
        'RequiredToPreview': True,
    }]
    for q in quals:
        if q['QualificationTypeId'] != '00000000000000000071':
            # Can only have one location qualification, and it's the one we've
            # already listed above
            fin_quals.append(q)
    return fin_quals


def get_true_url(use_url):
    return use_url + '_fb'
