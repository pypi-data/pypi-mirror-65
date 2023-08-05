from pathlib import Path
from datalad.support import json_py


# TODO: deal with :all etc. qualifiers


class Specification(list):
    # bind to Path (read config for default)

    def __init__(self, path=None):
        super(Specification, self).__init__()

        self.specfile = Path(path)

        if self.specfile.exists():
            [self.append(s) for s in json_py.load_stream(str(self.specfile))]
            # Hmmm. Snippet()?


    def get_uniques(self):  # TODO: Naming is wrong/misleading

        collect = dict()
        for snippet in self:

            # problem: we have (non-) editable fields. In addition for a list like procedures or tags uniques might not
            # be the list itself, but a particular entry

            for k, v in snippet.items():
                collect[k]

    # def is_valid()

    # def get_uniques() =>

    # need to overwrite self.sort()?!
    pass


class Snippet(dict):

    dict.__init__(**kwargs)
    # create mandatory fields
    #
    # def is_valid()

    # overwrite update()?
    pass


# Should have 'location', 'dataset-id', 'dataset-refcommit', 'tags', 'procedures'

# - update a snippet
# - access snippets ... get/update/remove/append/insert/get values/
#   get list by type or type:qualifier
# - sorting? Not clear, but order is relevant, so needs to be stable re inserting/updating snippets
# - how exactly to identify a snippet (Replace vs. add)? location only? what if => spec4anything --replace
# - validation? auto before store?

class SpecHandler(object):

    def __init__(self, path):  # alternatively acquisition or handle this above?
        # what if not (yet) exists?
        # load it
        # should path be allowed to be a dir or a spec-file?
        pass

    def store(self):  # datalad save or not? => message
        pass

########## from spec_helpers ###############


def sort_spec(spec):
    """Helper to provide a key function for `sorted`

    Provide key to sort by type first and by whatever identifies a particular
    type of spec dict

    Parameters
    ----------
    spec: dict
      study specification dictionary

    Returns
    -------
    string
    """

    if spec['type'] == 'dicomseries':
        return 'dicomseries' + spec['uid']
    else:
        # ATM assuming everything else is identifiable by its location:
        return spec['type'] + spec['location']


def get_specval(spec, key):
    return spec[key]['value']


def has_specval(spec, key):
    return key in spec and 'value' in spec[key] and spec[key]['value']


############################# from spec4anything ############################

# TODO: Prob. should be (partially?) editable, but for now we need consistency
# here:
non_editables = ['location', 'type', 'dataset-id', 'dataset-refcommit']


def _get_edit_dict(value=None, approved=False):
    # our current concept of what an editable field looks like
    return dict(approved=approved, value=value)


def _add_to_spec(spec, spec_dir, path, ds, overrides=None, replace=False):
    """
    Parameters
    ----------
    spec: list of dict
      specification to add the snippet to
    spec_dir:
      path to where the spec file is (paths in spec are relative to that location)
    path:
      path to the entity this snippet is about
    meta:
      metadata of the dataset (for dataset_id and refcommit)
    overrides: dict
      key, values to add/overwrite the default
    """

    from datalad_metalad import get_refcommit
    snippet = {
        'type': 'generic_' + path['type'],
        'location': posixpath.relpath(path['path'], spec_dir),
        'dataset-id': ds.id,
        'dataset-refcommit': get_refcommit(ds),
        'id': _get_edit_dict(),
        'procedures': _get_edit_dict(),
        'comment': _get_edit_dict(value=""),
    }

    snippet.update(overrides)

    # figure, whether we need to append the snippet or replace an
    # existing one
    if replace:
        for s in spec:
            if s['type'] == snippet['type'] and \
               s['location'] == snippet['location'] and \
               s['id']['value'] == snippet['id']['value']:
                # replace existing snippet:
                # Note: This needs to be documented. The identification as well
                # as the fact that only first occurence will be replaced.
                s.update(snippet)
                return spec

    spec.append(snippet)
    return spec


# if properties:
#
#     # TODO: This entire reading of properties needs to be RF'd
#     # into proper generalized functions.
#     # spec got more complex. update() prob. can't simply override
#     # (think: 'procedures' and 'tags' prob. need to be appended
#     # instead)
#
#     # load from file or json string
#     if isinstance(properties, dict):
#         props = properties
#     elif op.exists(properties):
#         props = json_py.load(properties)
#     else:
#         props = json_py.loads(properties)
#     # turn into editable, pre-approved records
#     spec_props = {k: dict(value=v, approved=True)
#                   for k, v in props.items()
#                   if k not in non_editables + ['tags', 'procedures']}
#     spec_props.update({k: v
#                        for k, v in props.items()
#                        if k in non_editables + ['tags']})
#
#     # TODO: still wrong. It's a list. Append or override? How to decide?
#     spec_props.update({o_k: [{i_k: dict(value=i_v, approved=True)
#                               for i_k, i_v in o_v.items()}]
#                        for o_k, o_v in props.items()
#                        if o_k in ['procedures']})
#
#     overrides.update(spec_props)

# TODO: It's probably wrong to use uniques for overwriting! At least
# they cannot be used to overwrite values explicitly set in
# _add_to_spec like "location", "type", etc.
#
# But then: This should concern non-editable fields only, right?

spec = _add_to_spec(spec, posixpath.split(spec_path)[0], ap,
                    dataset, overrides=overrides, replace=replace)

################################ from dicom2spec

def add_to_spec(ds_metadata, spec_list, basepath,
                subject=None, anon_subject=None, session=None, overrides=None, dataset=None):

    # TODO: discover procedures and write default config into spec for more convenient editing!
    # But: Would need toolbox present to create a spec. If not - what version of toolbox to use?
    # Double-check run-procedure --discover

    # Spec needs a dicomseries:all snippet before the actual dicomseries
    # snippets, since the order determines the order of execution of procedures
    # later on.
    # Note, that here we only make sure such a snippet exists. It is to be
    # updated with unique values from the dicomseries snippets later on.
    existing_all_dicoms = [i for s, i in zip(spec_list, range(len(spec_list)))
                           if s['type'] == 'dicomseries:all']
    assert len(existing_all_dicoms) <= 1

    if not existing_all_dicoms:
        spec_list.append({'type': 'dicomseries:all'})
        existing_all_dicoms = len(spec_list) - 1
    else:
        existing_all_dicoms = existing_all_dicoms[0]

    # proceed with actual image series:
    lgr.debug("Discovered %s image series.",
              len(ds_metadata['metadata']['dicom']['Series']))

    # generate a list of dicts, with the "rule-proof" entries:
    base_list = []
    for series in ds_metadata['metadata']['dicom']['Series']:
        base_list.append({
            # Note: The first 4 entries aren't a dict and have no
            # "approved flag", since they are automatically managed
            'type': 'dicomseries',
            'location': op.relpath(ds_metadata['path'], basepath),
            'uid': series['SeriesInstanceUID'],
            'dataset-id': ds_metadata['dsid'],
            'dataset-refcommit': ds_metadata['refcommit'],
            'tags': []
            #'tags': ['hirni-dicom-converter-ignore']
            #        if not series_is_valid(series) else [],
        })

    rules_new = RuleSet(dataset=dataset)   # TODO: Pass on dataset for config access! => RF the entire thing
    derived = rules_new.apply(ds_metadata['metadata']['dicom']['Series'],
                              subject=subject,
                              anon_subject=anon_subject,
                              session=session
                              )

    # TODO: Move assertion to a test?
    assert len(derived) == len(base_list)
    for idx in range(len(base_list)):
        base_list[idx].update(derived[idx])

    # merge with existing spec plus overrides:
    for series in base_list:

        series.update(overrides)

        existing = [i for s, i in
                    zip(spec_list, range(len(spec_list)))
                    if s['type'] == 'dicomseries' and s['uid'] == series['uid']]
        if existing:
            lgr.debug("Updating existing spec for image series %s",
                      series['uid'])
            # we already had data of that series in the spec;
            spec_list[existing[0]].update(series)
        else:
            lgr.debug("Creating spec for image series %s", series['uid'])
            spec_list.append(series)

    # spec snippet for addressing an entire dicom acquisition:
    # fill in values of editable fields, that are unique across
    # dicomseries
    uniques = dict()
    for s in spec_list:
        for k in s.keys():
            if isinstance(s[k], dict) and 'value' in s[k]:
                if k not in uniques:
                    uniques[k] = set()
                uniques[k].add(s[k]['value'])

    all_dicoms = dict()
    for k in uniques:
        if len(uniques[k]) == 1:
            all_dicoms[k] = _get_edit_dict(value=uniques[k].pop(),
                                           approved=False)

    all_dicoms.update({
        'type': 'dicomseries:all',
        'location': op.relpath(ds_metadata['path'], basepath),
        'dataset-id': ds_metadata['dsid'],
        'dataset-refcommit': ds_metadata['refcommit'],
        'procedures': [{
                'procedure-name': {'value': 'hirni-dicom-converter',
                                   'approved': False},
                'procedure-call': {'value': None,
                                   'approved': False},
                'on-anonymize': {'value': False,
                                 'approved': False},
            },
        ]
    })

    spec_list[existing_all_dicoms].update(all_dicoms)

    return spec_list
