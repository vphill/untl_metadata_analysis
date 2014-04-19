import sys
import hashlib
from datetime import datetime
from pyuntl.untldoc import untlxml2py, untlpy2dict


def get_is_hidden(untl_dict):
    untl_dict = untl_dict
    hidden = "False"
    for meta in untl_dict["meta"]:
        if meta["qualifier"] == "hidden":
            hidden = meta["content"]
    return hidden


def get_metadata_creator(untl_dict):
    untl_dict = untl_dict
    metadata_creator = "None"
    for meta in untl_dict["meta"]:
        if meta["qualifier"] == "metadataCreator":
            metadata_creator = meta["content"]
    return metadata_creator


def get_metadata_editor(untl_dict):
    untl_dict = untl_dict
    metadata_editor = "None"
    for meta in untl_dict["meta"]:
        if meta["qualifier"] == "metadataModifier":
            metadata_editor = meta["content"]
    return metadata_editor


def get_metadata_creation_date(untl_dict):
    untl_dict = untl_dict
    metadata_creation_date = "None"
    for meta in untl_dict["meta"]:
        if meta["qualifier"] == "metadataCreationDate":
            metadata_creation_date = meta["content"]
    return metadata_creation_date


def get_metadata_edit_date(untl_dict):
    untl_dict = untl_dict
    metadata_edit_date = "None"
    for meta in untl_dict["meta"]:
        if meta["qualifier"] == "metadataModificationDate":
            metadata_edit_date = meta["content"]
    return metadata_edit_date


def get_ark(untl_dict):
    untl_dict = untl_dict
    ark = "None"
    for meta in untl_dict["meta"]:
        if meta["qualifier"] == "ark":
            ark = meta["content"]
    return ark


metadata_fields = ["title", "creator", "contributor", "publisher", "date",
                   "language", "description", "subject", "primarySource",
                   "coverage", "source", "citation", "relation", "collection",
                   "institution", "rights", "resourceType", "format",
                   "identifier", "degree", "note", "meta"]

header = True

for filename in sys.stdin:
    try:
        rd = {}
        untl = untlxml2py(filename.strip())
        rd["completeness"] = untl.completeness
        rd["record_length"] = untl.record_length
        rd["record_content_length"] = untl.record_content_length

        untl_dict = untlpy2dict(untl)
        for field in metadata_fields:
            rd[field] = len(untl_dict.get(field, []))
            hash_name = "%s_hash" % field
            rd[hash_name] = hashlib.md5(str(untl_dict.get(field, []))).hexdigest()

        rd["hidden"] = get_is_hidden(untl_dict)
        rd["metadata_creator"] = get_metadata_creator(untl_dict)
        rd["metadata_editor"] = get_metadata_editor(untl_dict)
        rd["metadata_creation_date"] = get_metadata_creation_date(untl_dict)
        rd["metadata_edit_date"] = get_metadata_edit_date(untl_dict)
        rd["ark"] = get_ark(untl_dict)

        if rd["metadata_creation_date"] != "None":
            creation_time = datetime.strptime(rd["metadata_creation_date"],
                                              "%Y-%m-%d, %H:%M:%S")

        if rd["metadata_edit_date"] != "None":
            #2014-03-12, 11:42:25
            edit_time = datetime.strptime(rd["metadata_edit_date"],
                                          "%Y-%m-%d, %H:%M:%S")
            rd["time_since_creation"] = int((edit_time - creation_time).total_seconds())
            rd["0_sample_id"] = "%s_%s" % (rd["ark"], edit_time.isoformat())
        else:
            rd["time_since_creation"] = 0
            rd["0_sample_id"] = "%s_%s" % (rd["ark"], creation_time.isoformat())

        if header is True:
            print "\t".join([k for k in sorted(rd)])
            header = False
        print "\t".join([str(rd[k]) for k in sorted(rd)])
    except:
        pass
