import pytest
import episodekit.object

SUB = {'element':[{'name':'a','type':'int32'},{'name':'b','type':'int32','default':7}]}
OUTER = {'element':[{'name':'inner','type':'definition:sub'}]}
REF = {'definition':'definition:sub','data':{'a':100,'b':200},'depends_on':[]}

def expand(element, data=None, mods=None):
  items = {'definition:sub':SUB, 'definition:outer':OUTER, 'object:ref':REF}
  items['definition:top'] = {'element':[dict({'name':'s','type':'definition:sub'}, **element)]}
  return episodekit.object.expand(data or {}, 'definition:top', items, object_mods=mods)[0]

@pytest.mark.parametrize('element,expected', [
  ({}, {'s':{'a':5,'b':7}}),
  ({'optional':True}, {'s':{'a':5,'b':7}}),
  ({'default':{'a':1,'b':2}}, {'s':{'a':5,'b':2}}),
  ({'default':'object:ref'}, {'s':{'a':5,'b':200}}),
])
def test_dotted_mods_apply_to_missing_sub_object(element, expected):
  assert expand(element, mods={'s.a':5}) == expected

def test_dotted_mods_apply_to_nested_missing_sub_objects():
  result = expand({'type':'definition:outer'}, mods={'s.inner.a':5})
  assert result == {'s':{'inner':{'a':5,'b':7}}}

def test_dotted_mods_apply_to_present_sub_object():
  assert expand({}, data={'s':{'a':1}}, mods={'s.a':5}) == {'s':{'a':5,'b':7}}

def test_dict_default_is_not_mutated_by_mods():
  default = {'a':1,'b':2}
  expand({'default':default}, mods={'s.a':5})
  assert default == {'a':1,'b':2}

@pytest.mark.parametrize('element,mods,expected', [
  ({'optional':True}, None, {}),
  ({'optional':True}, {'ss.a':5}, {}),
  ({'default':{'a':1,'b':2}}, None, {'s':{'a':1,'b':2}}),
])
def test_missing_sub_object_without_matching_mods_is_unchanged(element, mods, expected):
  assert expand(element, mods=mods) == expected
