from pathlib import Path

import pytest

import gconf


@pytest.fixture(autouse=True)
def reset_gconf():
	gconf.reset()


def assert_all():
	assert len(gconf.get('parent.child.list')) == 2
	assert gconf.get('parent.child.list')[0] == 'entry 0'
	assert gconf.get('parent.child.list')[1] == 'entry 1'
	assert gconf.get('parent.child.some string') == 'foo bar baz'
	assert gconf.get('parent.another child') == 'child content'
	assert gconf.get('another parent') == 'parent content'


def test_get_methods():
	gconf.load(Path('conf.yml'))
	assert_all()
	assert gconf.get('parent.child.some string') == gconf.get('parent', 'child', 'some string')
	assert gconf.get('parent.child.some string') == gconf.get('parent.child', 'some string')
	assert gconf.get('parent.child.some string') == gconf.get('parent')['child']['some string']
	assert gconf.get('parent.child.some string') == gconf.get('parent.child')['some string']
	assert gconf.get('parent.child.some string') == gconf.get()['parent']['child']['some string']


def test_non_existing_with_error():
	gconf.load(Path('conf.yml'))
	with pytest.raises(KeyError):
		gconf.get('non-existing')
	with pytest.raises(KeyError):
		gconf.get('parent.non-existing')


def test_non_existing_with_default():
	gconf.load(Path('conf.yml'))
	default_value = 'some default value'
	assert gconf.get('non-existing', default=default_value) == default_value
	assert gconf.get('parent.non-existing', default=default_value) == default_value
	assert gconf.get('non-existing-parent.non-existing-child', default=default_value) == default_value
	assert gconf.get('non-existing-parent', 'non-existing-child', default=default_value) == default_value


def test_default_is_falsey():
	gconf.load(Path('conf.yml'))
	assert gconf.get('non-existing', default=None) == None
	assert gconf.get('non-existing', default=False) == False
	assert gconf.get('non-existing', default='') == ''


def test_loading_2_configs_at_once():
	gconf.load('conf.yml', 'conf_overlay.yml')
	assert gconf.get('parent.child.some string') == 'coconut'
	assert gconf.get('new entry') == 'banana'
	assert gconf.get('parent.another child') == 'child content'


def test_loading_2_configs_iteratively():
	gconf.load('conf.yml')
	assert_all()
	gconf.load('conf_overlay.yml')
	assert gconf.get('parent.child.some string') == 'coconut'
	assert gconf.get('new entry') == 'banana'
	assert gconf.get('parent.another child') == 'child content'


def test_loading_with_path():
	gconf.load(Path('conf.yml'))
	assert_all()


def test_load_empty():
	gconf.load('conf_empty.yml')
	assert len(gconf.get()) == 0


def test_load_2_with_1_empty():
	gconf.load('conf.yml', 'conf_empty.yml')
	assert_all()


def test_loading_required():
	with pytest.raises(FileNotFoundError) as e:
		gconf.load('conf.yml', 'non-existing.yml')
	assert Path(str(e.value)).is_absolute()


def test_loading_not_required():
	gconf.load('conf.yml', 'non-existing.yml', required=False)
	assert_all()


def test_load_first():
	gconf.load_first('a', 'b', 'conf.yml', 'conf_overlay.yml')
	assert_all()


def test_load_first_none_with_required():
	with pytest.raises(FileNotFoundError) as e:
		gconf.load_first('a', 'b')
	assert all(Path(s.strip()).is_absolute() for s in str(e.value).split(','))


def test_load_first_none_with_required_false():
	gconf.load_first('a', 'b', required=False)


def test_load_first_with_folder():
	with pytest.raises(FileNotFoundError) as e:
		gconf.load_first('../test')
	assert Path(str(e.value)).is_absolute()


def test_add_new():
	gconf.load('conf.yml')
	gconf.add({'added': 5})
	assert_all()
	assert gconf.get('added') == 5


def test_add_override():
	gconf.load('conf.yml')
	gconf.add({'parent': {'child': 'new child'}})
	assert gconf.get('parent.child') == 'new child'


def test_reset():
	gconf.load('conf.yml')
	assert_all()
	gconf.reset()
	with pytest.raises(KeyError):
		assert_all()


def test_conf_override_existing_with_alternative():
	gconf.load(Path('conf.yml'))
	override_key = 'parent.another child'
	override_value = 'the override value'
	override_dict = {'parent': {'another child': override_value}}
	with gconf.override_conf(override_dict):
		assert gconf.get(override_key) == override_value
	assert_all()


def test_conf_override_add_new():
	gconf.load(Path('conf.yml'))
	override_key = 'parent.new.override.value'
	override_value = 'the override value'
	override_dict = {'parent': {'new': {'override': {'value': override_value}}}}
	with gconf.override_conf(override_dict):
		assert gconf.get(override_key) == override_value
	assert_all()


def test_conf_override_existing_delete():
	gconf.load(Path('conf.yml'))
	override_key = 'parent.another child'
	override_dict = {'parent': {'another child': gconf.DELETED}}
	with gconf.override_conf(override_dict):
		with pytest.raises(KeyError):
			gconf.get(override_key)
	assert_all()


def test_conf_override_existing_delete_tree():
	gconf.load(Path('conf.yml'))
	override_key = 'parent.child'
	override_dict = {'parent': {'child': gconf.DELETED}}
	with gconf.override_conf(override_dict):
		with pytest.raises(KeyError):
			gconf.get(override_key)
	assert_all()


def test_getting_dict_with_separate_layers():
	gconf.add({'foo': 1})
	gconf.add({'bar': 2})
	result = gconf.get()

	assert result['foo'] == 1
	assert result['bar'] == 2


def test_dict_reflects_global_updates():
	gconf.add({'foo': 1})
	result = gconf.get()
	gconf.add({'bar': 2})

	assert result['foo'] == 1
	assert result['bar'] == 2


def test_dict_reflects_global_updates_after_override():
	gconf.add({'foo': 1})
	result = gconf.get()
	with gconf.override_conf({'baz': 3}):
		pass
	gconf.add({'bar': 2})

	assert result['foo'] == 1
	assert result['bar'] == 2
