import os
import pytest
import confuse
import confuse_jinja
confuse_jinja.enable()


def test_basic():
    assert confuse.Subview is confuse_jinja.Subview

    config = confuse.Configuration('shhhh', read=False)
    config.set({
        'asdf': {'blah': 'asdf{{ C.other.thing }}'},
        'circle1': '{{ C.circle2 }}',
        'circle2': '{{ C.circle1 }}',
        'nested': '{{ C.asdf }}',
        'nestedstr': 'asdf{{ C.asdf }}',
        'other': {'thing': 4},
    })

    assert config['asdf']['blah'].get() == 'asdf4'

    with pytest.raises(confuse_jinja.CircularReference):
        config['circle1'].get()

    assert config['asdf'].get() == {'blah': 'asdf4'}
    assert config['nested'].get() == config['asdf'].get()
    assert config['nestedstr'].get() == 'asdf{}'.format(str(config['asdf'].get()))

def test_yaml():
    assert confuse.Subview is confuse_jinja.Subview

    config = confuse.Configuration('shhhh', read=False)
    config.set(confuse.load_yaml(
        os.path.join(os.path.dirname(__file__), 'sample.yml')))

    assert config['asdf']['blah'].get() == 'asdf4'
    assert config['asdf'].get() == {'blah': 'asdf4'}
    assert config['nested'].get() == config['asdf'].get()
