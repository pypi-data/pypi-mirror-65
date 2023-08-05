'''_751.py

FaceGearSetMicroGeometry
'''


from typing import List

from mastapy.gears.gear_designs.face import _750, _748, _747
from mastapy._internal import constructor, conversion
from mastapy.gears.analysis import _952
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Face', 'FaceGearSetMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetMicroGeometry',)


class FaceGearSetMicroGeometry(_952.GearSetImplementationDetail):
    '''FaceGearSetMicroGeometry

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_MICRO_GEOMETRY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def face_gear_set_design(self) -> '_750.FaceGearSetDesign':
        '''FaceGearSetDesign: 'FaceGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_750.FaceGearSetDesign)(self.wrapped.FaceGearSetDesign) if self.wrapped.FaceGearSetDesign else None

    @property
    def face_gear_micro_geometries(self) -> 'List[_748.FaceGearMicroGeometry]':
        '''List[FaceGearMicroGeometry]: 'FaceGearMicroGeometries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearMicroGeometries, constructor.new(_748.FaceGearMicroGeometry))
        return value

    @property
    def face_mesh_micro_geometries(self) -> 'List[_747.FaceGearMeshMicroGeometry]':
        '''List[FaceGearMeshMicroGeometry]: 'FaceMeshMicroGeometries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshMicroGeometries, constructor.new(_747.FaceGearMeshMicroGeometry))
        return value
