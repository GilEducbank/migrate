import binascii
import datetime

import bson


# flatten nested objects, keeping their parent names as reference
def flatten_doc(simple_doc, map_reference, parent_name):
    for field in simple_doc:
        if isinstance(simple_doc[field], dict):
            if parent_name == "":
                flatten_doc(simple_doc[field], map_reference, field)
            else:
                flatten_doc(simple_doc[field], map_reference, parent_name + "." + field)
        else:
            if parent_name == "":
                map_reference[field] = simple_doc[field]
            else:
                map_reference[parent_name + "." + field] = simple_doc[field]
    return map_reference


# convert arrays to string and rename them
def treat_arrays(simple_doc):
    map = dict()
    for field in simple_doc:
        if isinstance(simple_doc[field], list):
            map["array_" + field] = str(simple_doc[field])
        else:
            map[field] = simple_doc[field]

    return map


# converts binarys from a single object
def convert_its_binarys_from_dict(simple_doc):
    if not isinstance(simple_doc, dict) and not isinstance(simple_doc, list):
        return simple_doc
    map = dict()
    for field in simple_doc:
        if isinstance(simple_doc[field], bson.binary.Binary):
            binary_to_string = str(binascii.b2a_base64(simple_doc[field], newline=False))
            map[field] = binary_to_array(binary_to_string)
        elif isinstance(simple_doc[field], dict):
            map[field] = convert_its_binarys_from_dict(simple_doc[field])
        elif isinstance(simple_doc[field], list):
            map[field] = convert_its_binarys_from_list(simple_doc[field])
        else:
            map[field] = simple_doc[field]
    return map


# convert binarys from a  list of objects
def convert_its_binarys_from_list(simple_list):
    result = []
    for inner_item in simple_list:
        result.append(convert_its_binarys_from_dict(inner_item))

    return result


# transform binary into
def binary_to_array(insertion):
    str = cut_string(insertion)
    return '{ "$binary" : "' + str + '", "$type" : "04" }'


# remove unnecessary characters
def cut_string(string_to_cut):
    str = string_to_cut[:len(string_to_cut) - 1]
    str = str[2:]
    return str


# call all necessary functions to treat the document
def treat_document(document):
    # this can only be called like that because we want to transform binarys only for the second level forward
    for inner_field in document:
        if isinstance(document[inner_field], list):
            document[inner_field] = convert_its_binarys_from_list(document[inner_field])

    inner_result = flatten_doc(document, dict(), "")
    inner_result = treat_arrays(inner_result)
    return inner_result


map_types = {
    bson.binary.Binary: "bytea",
    str: "text",
    datetime.datetime: "timestamp(6)",
    bool: "bool",
    bson.int64.Int64: "int8",
    bson.objectid.ObjectId: "bytea",
    int: "integer",
    None: "text",
    bytes: "bytea"
}


#receives a field and return its type in postgres, like a dictionary (key-value DS)
def map_types_by_field(field):
    try:
        if field is None:
            return "text"

        return map_types[type(field)]
    except:
        return "Unknown data type " + str(type(field))


# gets a type as input and return postgres type. If is not Known, return text as default
def map_types_by_type(input_type):
    try:
        return map_types[input_type]
    except:
        return "text"


# return a dictionary (key-value DS) of field -> type of field for a given collection of documents
def get_collection_types(collection):
    field_type = dict()
    first_document = collection[0]

    #always get the biggest document from collection
    for doc in collection:
        if len(doc) > len(first_document):
            first_document = doc

    for field in first_document:
        if first_document[field] is None:
            field_type[field] = None
        else:
            field_type[field] = type(first_document[field])

    # this for will try to find a different type for the field if he is currently set as None
    for document in collection:
        for field in field_type:
            if field_type[field] is None and document[field] is not None:
                field_type[field] = type(document[field])

    return field_type
