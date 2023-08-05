# Copyright (c) 2019-2020 SAP SE or an SAP affiliate company. All rights reserved. This file is
# licensed under the Apache Software License, v. 2 except as noted otherwise in the LICENSE file
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools
import unittest
import pytest

import product.util as util
import product.model as model

# functions under test
greatest_crefs = util.greatest_references
diff_components = util.diff_components


def component_ref(name, version, prefix='gh.com/o/'):
    return model.ComponentReference.create(name=prefix + name, version=version)


@pytest.fixture
def cref():
    return component_ref


def image_ref(name, version):
    return model.ContainerImage.create(
        name=name,
        version=version,
        image_reference='dont:care',
    )


@pytest.fixture
def iref():
    return image_ref


class ProductUtilTest(unittest.TestCase):
    def setUp(self):
        self.cref1 = component_ref(name='c1', version='1.2.3')
        self.cref2 = component_ref(name='c2', version='2.2.3')

    def test_greatest_references(self):
        # trivial case: single cref
        result = list(greatest_crefs((self.cref1,)))
        self.assertSequenceEqual(result, (self.cref1,))

        # trivial case: two crefs, different
        result = list(greatest_crefs((self.cref2, self.cref1)))
        self.assertSequenceEqual(result, (self.cref2, self.cref1))

        # non-trivial case: duplicate component name, different versions
        cref1_greater = model.ComponentReference.create(name=self.cref1.name(), version='9.0.9')
        cref1_lesser = model.ComponentReference.create(name=self.cref1.name(), version='0.0.1')

        result = set(greatest_crefs((self.cref1, self.cref2, cref1_greater, cref1_lesser)))
        self.assertSetEqual({cref1_greater, self.cref2}, result)

    def test_greatest_references_argument_validation(self):
        # None-check
        with self.assertRaises(ValueError):
            next(greatest_crefs(None))

        # reject elements that are not component references
        with self.assertRaises(ValueError):
            non_component_element = 42 # int is not of type product.model.ComponentReference
            next(greatest_crefs((self.cref1, non_component_element)))


def test_diff_components(cref):
    left_components = (
        cref('c1', '1.2.3'),
        cref('c2', '1.2.3'),
        cref('c3', '1.2.3'),
    )
    right_components = (
        cref('c1', '2.2.3'), # version changed
        cref('c2', '1.2.3'), # no change
        #cref('c3', '1.2.3'), # missing on right
        cref('c4', '1.2.3'), # added on right
    )

    result = diff_components(left_components, right_components)

    assert result.crefs_only_left == {cref('c3', '1.2.3'), cref('c1', '1.2.3')}
    assert result.crefs_only_right == {cref('c4', '1.2.3'), cref('c1', '2.2.3')}
    assert result.crefpairs_version_changed == {(cref('c1', '1.2.3'), cref('c1', '2.2.3'))}
    assert result.names_only_left == {'gh.com/o/c3'}
    assert result.names_only_right == {'gh.com/o/c4'}
    assert result.names_version_changed == {'gh.com/o/c1'}


def test_diff_images(cref, iref):
    comp_desc = model.ComponentDescriptor.from_dict({})
    left_comp = model.Component.create('x.o/a/b', '1.2.3')
    right_comp = model.Component.create('x.o/a/b', '2.3.4')
    comp_desc.add_component(left_comp)
    comp_desc.add_component(right_comp)
    l_deps = left_comp.dependencies()
    r_deps = right_comp.dependencies()

    examinee = functools.partial(
        util.diff_images,
        left_component_descriptor=comp_desc,
        right_component_descriptor=comp_desc,
    )

    img1 = iref('i1', '1.2.3')

    l_deps.add_container_image_dependency(img1)
    r_deps.add_container_image_dependency(img1)

    img_diff = examinee(left_component=left_comp, right_component=right_comp)

    # same image added declared by left and right - expect empty diff
    assert img_diff.left_component == left_comp
    assert img_diff.right_component == right_comp
    assert len(img_diff.irefs_only_left) == 0
    assert len(img_diff.irefs_only_right) == 0

    img2 = iref('i2', '1.2.3')
    img3 = iref('i3', '1.2.3')
    l_deps.add_container_image_dependency(img2)
    r_deps.add_container_image_dependency(img3)

    # img2 only left, img3 only right
    img_diff = examinee(left_component=left_comp, right_component=right_comp)
    assert len(img_diff.irefs_only_left) == 1
    assert len(img_diff.irefs_only_right) == 1
    assert list(img_diff.irefs_only_left)[0] == img2
    assert list(img_diff.irefs_only_right)[0] == img3

    img4_0 = iref('i4', '1.2.3')
    img4_1 = iref('i4', '2.0.0') # "change version"
    l_deps.add_container_image_dependency(img4_0)
    r_deps.add_container_image_dependency(img4_1)
    img_diff = examinee(left_component=left_comp, right_component=right_comp)
    assert len(img_diff.irefs_only_left) == 1
    assert len(img_diff.irefs_only_right) == 1
    assert len(img_diff.irefpairs_version_changed) == 1
    left_i, right_i = list(img_diff.irefpairs_version_changed)[0]
    assert type(left_i) == type(img4_0)
    assert left_i.raw == img4_0.raw
    assert left_i == img4_0
    assert right_i == img4_1


def test_enumerate_effective_images(cref):
    comp_desc = model.ComponentDescriptor.from_dict({})

    c1 = cref('c1', '1.2.3')
    comp_desc.add_component(c1)
    c1 = comp_desc.component(c1)

    c1deps = c1.dependencies()
    image1 = model.ContainerImage.create(name='i1', version='1.2.3', image_reference='i:1')
    # image2 shares same logical name (-> regression test)
    image2 = model.ContainerImage.create(name='i1', version='1.2.4', image_reference='i:3')
    images_count = 2

    c1deps.add_container_image_dependency(image1)
    c1deps.add_container_image_dependency(image2)

    # ensure it's contained in regular enumerate_images
    comps_and_images = tuple(util._enumerate_images(comp_desc))
    assert len(comps_and_images) == images_count
    result_c, result_i = comps_and_images[0]
    assert result_c == c1
    assert result_i == image1
    result_c, result_i2 = comps_and_images[1]
    assert result_c == c1
    assert result_i2 == image2

    # ensure it's also there in enumerate_effective_images (with no overwrites)
    comps_and_images = tuple(util._enumerate_effective_images(comp_desc))
    assert len(comps_and_images) == images_count
    result_c, result_i = comps_and_images[0]
    assert result_c == c1
    assert result_i == image1
    result_c, result_i2 = comps_and_images[1]
    assert result_c == c1
    assert result_i2 == image2

    # now add an overwrite
    comp_overwrites = comp_desc.component_overwrite(declaring_component=cref('dontcare1', '1.2.3'))
    dep_overwrites = comp_overwrites.dependency_overwrite(
        referenced_component=c1,
        create_if_absent=True,
    )
    # name and version must match
    image_overwrite = model.ContainerImage.create(name='i1', version='1.2.3', image_reference='i:2')
    dep_overwrites.add_container_image_overwrite(image_overwrite)

    # ensure the overwrite is evaluated
    comps_and_images = tuple(util._enumerate_effective_images(comp_desc))
    assert len(comps_and_images) == images_count
    result_c, result_i = comps_and_images[0]
    assert result_c == c1
    assert result_i == image_overwrite

    result_c, result_i2 = comps_and_images[1]
    assert result_c == c1
    assert result_i2 == image2


def test_grouped_effective_images(cref):
    comp_desc = model.ComponentDescriptor.from_dict({})

    c1 = cref('c1', '1.2.3')
    comp_desc.add_component(c1)
    c1 = comp_desc.component(c1)

    c1deps = c1.dependencies()
    image1 = model.ContainerImage.create(name='i1', version='1.2.3', image_reference='i:1')
    # image2 shares same logical name
    image2 = model.ContainerImage.create(name='i1', version='1.2.4', image_reference='i:3')
    # image3 has different logical name
    image3 = model.ContainerImage.create(name='xo', version='1.2.4', image_reference='i:3')

    c1deps.add_container_image_dependency(image1)
    c1deps.add_container_image_dependency(image2)
    c1deps.add_container_image_dependency(image3)

    grouped_images = tuple(
        util._grouped_effective_images(
            c1,
            component_descriptor=comp_desc,
        )
    )

    # image1 and image2 should have been grouped, so expect two groups
    assert len(grouped_images) == 2
    img1_and_img2, img3 = grouped_images

    assert len(img1_and_img2) == 2
    assert len(img3) == 1
