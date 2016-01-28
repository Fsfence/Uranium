# Copyright (c) 2015 Ultimaker B.V.
# Uranium is released under the terms of the AGPLv3 or higher.

from . import Operation
from UM.Scene.SceneNode import SceneNode
from UM.Math.Vector import Vector
import copy
class ScaleOperation(Operation.Operation):
    def __init__(self, node, scale, **kwargs):
        super().__init__()
        self._node = node
        self._old_scale = node.getScale()
        self._set_scale = kwargs.get("set_scale", False)
        self._add_scale = kwargs.get("add_scale", False)
        self._relative_scale = kwargs.get("relative_scale", False)
        self._scale = scale

    def undo(self):
        self._node.setScale(self._old_scale)

    def redo(self):
        if self._set_scale:
            self._node.setScale(self._scale)
        elif self._add_scale:
            self._node.setScale(self._node.getScale() + self._scale)
        elif self._relative_scale:
            new_scale = self._node.getScale() + self._scale
            current_scale = copy.deepcopy(self._node.getScale())
            new_scale.setX(new_scale.x / current_scale.x)
            new_scale.setY(new_scale.y / current_scale.y)
            new_scale.setZ(new_scale.z / current_scale.z)

            self._node.scale(new_scale, SceneNode.TransformSpace.Parent)
        else:
            self._node.scale(self._scale, SceneNode.TransformSpace.World)

    def mergeWith(self, other):
        if type(other) is not ScaleOperation:
            return False

        if other._node != self._node:
            return False

        if other._set_scale and not self._set_scale:
            return False

        if other._add_scale and not self._add_scale:
            return False

        op = ScaleOperation(self._node, self._scale)
        op._old_scale = other._old_scale
        return op

    def __repr__(self):
        return "ScaleOperation(node = {0}, scale={1})".format(self._node, self._scale)

