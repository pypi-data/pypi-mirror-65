from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ParseError
from xml.parsers.expat import errors
import xml.dom.minidom as md
import json
import copy
import re
import cv2


def clean_text(temp):
    temp = temp.replace('{', '<br>')
    temp = temp.replace('}', '')
    temp = temp.replace('', '')
    temp = temp.replace('[', '<break-line><br>')
    temp = temp.replace(']', '<br>')
    temp = temp.replace('"', '')
    temp = temp.replace("'", '')
    if '<br>' in temp:
        temp = temp.replace(',', '')
    return temp


def diff_text(new, old):
    new_list = new.split("<br>")
    old_list = old.split("<br>")
    ref_list = old_list if len(old_list) > len(new_list) else new_list
    for index in range(len(ref_list)):
        try:
            old_item = old_list[index]
        except:
            old_item = ""
        try:
            new_item = new_list[index]
        except:
            new_item = ""
        if len(old_item) != len(new_item) or any([old_item[i] != new_item[i] for i in range(len(old_item))]):
            if old_item:
                break_line = "margin-bottom:30px;margin-top:15px" if "<break-line>" in old_item else ""
                old_item = old_item.replace("<break-line>", "")
                old_list[
                    index] = "<p style='background-color:red;color:white;word-break: break-all;{0}'>".format(
                    break_line) + old_item + "</p>"
            if new_item:
                break_line = "margin-bottom:30px;margin-top:15px" if "<break-line>" in new_item else ""
                new_item = new_item.replace("<break-line>", "")
                new_list[
                    index] = "<p style='background-color:red;color:white;word-break: break-all;{0}'>".format(
                    break_line) + new_item + "</p>"
        else:
            if old_item:
                break_line = "margin-bottom:30px;margin-top:15px" if "<break-line>" in old_item else ""
                old_item = old_item.replace("<break-line>", "")
                old_list[
                    index] = "<p style='word-break: break-all;{0}'>".format(break_line) + old_item + "</p>"
            if new_item:
                break_line = "margin-bottom:30px;margin-top:15px" if "<break-line>" in new_item else ""
                new_item = new_item.replace("<break-line>", "")
                new_list[
                    index] = "<p style='word-break: break-all;{0}'>".format(break_line) + new_item + "</p>"

    return "".join(new_list), "".join(old_list)


def convert_list_to_dict(result, value, ignore_nr=False):
    for nv in value:
        key = list(nv.keys())[0]
        if isinstance(nv[key], list):
            if not len(nv[key]):
                result.update({key: 'N/R'})
            else:
                convert_list_to_dict(result, nv[key], ignore_nr=ignore_nr)
        elif isinstance(nv[key], dict):
            result.update(nv[key])
        else:
            if not ignore_nr or nv[key] != "N/R":
                result.update(nv)


def json_to_string(json_string, indent=4, sort_keys=False):
    return json.dumps(json_string, indent=indent, sort_keys=sort_keys)


def remove_json_trailing_commas(json_like):
    """
    Removes trailing commas from *json_like* and returns the result.  Example::
        remove_trailing_commas('{"foo":"bar","baz":["blah",],}')
        '{"foo":"bar","baz":["blah"]}'
    """
    trailing_object_commas_re = re.compile(r'(,)\s*}(?=([^"\\]*(\\.|"([^"\\]*\\.)*[^"\\]*"))*[^"]*$)')
    trailing_array_commas_re = re.compile(r'(,)\s*\](?=([^"\\]*(\\.|"([^"\\]*\\.)*[^"\\]*"))*[^"]*$)')
    # Fix objects {} first
    objects_fixed = trailing_object_commas_re.sub("}", json_like)
    # Now fix arrays/lists [] and return the result
    return trailing_array_commas_re.sub("]", objects_fixed)


def validate_xml_from_string(xml_string):
    result = {
        'is_valid': True,
        'line': -1,
        'column': -1,
        'error_message': ''
    }
    try:
        xml_string_tested = copy.copy(xml_string)
        parsed_file_tree = parse_xml_from_string(xml_string_tested)
    except ParseError as ex:
        result['is_valid'] = False
        result['line'] = ex.position[0]
        result['column'] = ex.position[1]
        result['error_message'] = errors.messages[ex.code]

    return result


def sort_all_xml_tags(xml_et: ET.Element, parent_tag_name):
    # Reads
    tag_et = xml_et.find(parent_tag_name)
    # Sorts
    tag_et[:] = sorted(tag_et, key=lambda child: child.tag)

    # sorted xml etree
    return xml_et


def et_to_string(element: ET.Element, indent=2, add_xml_definition=False,
                 xml_definition='<?xml  version="1.0" encoding="UTF-8" ?>'):
    raw_xml = ET.tostring(element, encoding='unicode')
    pretty_xml = prettify_xml(raw_xml, indent, add_xml_definition, xml_definition)

    return pretty_xml


def et_to_string_mapcon(element: ET.Element, indent=2, add_xml_definition=False,
                        xml_definition='<?xml  version="1.0" encoding="UTF-8" ?>'):
    raw_xml = ET.tostring(element, encoding='unicode')
    pretty_xml = prettify_xml(raw_xml, indent, add_xml_definition, xml_definition)
    pretty_xml = re.sub("</operator>", "</operator>\n", pretty_xml)
    return pretty_xml


def et_to_string_epdg(element: ET.Element, indent=2, add_xml_definition=False,
                      xml_definition='<?xml  version="1.0" encoding="UTF-8" ?>'):
    raw_xml = ET.tostring(element, encoding='unicode')
    raw_xml = re.sub("\" ", "\"\n", raw_xml)
    raw_xml = re.sub("><", ">\n\n<", raw_xml)
    return raw_xml


def prettify_xml(text, indent=2, add_xml_definition=False, xml_definition='<?xml  version="1.0" encoding="UTF-8" ?>'):
    output = md.parseString(text).toprettyxml(indent=' ' * indent)

    # removing default xml definition added by md.parseString() method
    output = '\n'.join([line for line in output.split('\n')[1:] if line.strip()])

    # Add xml definition header
    if add_xml_definition:
        output = xml_definition + '\n' + output

    return output


def parse_xml_from_string(xml_str):
    # Removes invalid character present at beginning of some MPS xml files

    if isinstance(xml_str, bytes):
        xml_str = xml_str.decode('utf-8')

    xml_str = xml_str.replace(r'ï»¿', '')
    return ET.fromstring(xml_str)


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)
