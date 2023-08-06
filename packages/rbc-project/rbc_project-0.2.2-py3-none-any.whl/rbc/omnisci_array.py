import re
import operator
from llvmlite import ir
import numpy as np
from . import typesystem
from .utils import get_version
if get_version('numba') >= (0, 49):
    from numba.core import datamodel, cgutils, extending, types
else:
    from numba import datamodel, cgutils, extending, types


class ArrayPointer(types.Type):
    """Type class for pointers to :code:`Omnisci Array<T>` structure.

    We are not deriving from CPointer because ArrayPointer getitem is
    used to access the data stored in Array ptr member.
    """
    mutable = True

    def __init__(self, dtype, eltype):
        self.dtype = dtype
        self.eltype = eltype
        name = "(%s)*" % dtype
        super(ArrayPointer, self).__init__(name)

    @property
    def key(self):
        return self.dtype


@datamodel.register_default(ArrayPointer)
class ArrayPointerModel(datamodel.models.PointerModel):
    pass


@extending.intrinsic
def omnisci_array_len_(typingctx, data):
    sig = types.int64(data)

    def codegen(context, builder, signature, args):
        data, = args
        rawptr = cgutils.alloca_once_value(builder, value=data)
        struct = builder.load(builder.gep(rawptr,
                                          [ir.Constant(ir.IntType(32), 0)]))
        return builder.load(builder.gep(
            struct, [ir.Constant(ir.IntType(32), 0),
                     ir.Constant(ir.IntType(32), 1)]))
    return sig, codegen


@extending.overload(len)
def omnisci_array_len(x):
    if isinstance(x, ArrayPointer):
        return lambda x: omnisci_array_len_(x)


@extending.intrinsic
def omnisci_array_getitem_(typingctx, data, index):
    sig = data.eltype(data, index)

    def codegen(context, builder, signature, args):
        data, index = args
        rawptr = cgutils.alloca_once_value(builder, value=data)
        arr = builder.load(builder.gep(rawptr,
                                       [ir.Constant(ir.IntType(32), 0)]))
        ptr = builder.load(builder.gep(
            arr, [ir.Constant(ir.IntType(32), 0),
                  ir.Constant(ir.IntType(32), 0)]))
        res = builder.load(builder.gep(ptr, [index]))

        return res
    return sig, codegen


@extending.overload(operator.getitem)
def omnisci_array_getitem(x, i):
    if isinstance(x, ArrayPointer):
        return lambda x, i: omnisci_array_getitem_(x, i)


@extending.intrinsic
def omnisci_array_setitem_(typingctx, data, index, value):
    sig = types.none(data, index, value)

    def codegen(context, builder, signature, args):
        zero = ir.Constant(ir.IntType(32), 0)

        data, index, value = args

        rawptr = cgutils.alloca_once_value(builder, value=data)
        ptr = builder.load(rawptr)

        arr = builder.load(builder.gep(ptr, [zero, zero]))
        builder.store(value, builder.gep(arr, [index]))

    return sig, codegen


@extending.overload(operator.setitem)
def omnisci_array_setitem(a, i, v):
    if isinstance(a, ArrayPointer):
        return lambda a, i, v: omnisci_array_setitem_(a, i, v)


@extending.overload(np.sum)
@extending.overload(sum)
def omnisci_np_sum(a):
    if isinstance(a, ArrayPointer):
        def impl(a):
            s = 0
            n = len(a)
            for i in range(n):
                s += a[i]
            return s
        return impl


@extending.overload(np.prod)
def omnisci_np_prod(a):
    if isinstance(a, ArrayPointer):
        def impl(a):
            s = 1
            n = len(a)
            for i in range(n):
                s *= a[i]
            return s
        return impl


_array_type_match = re.compile(r'\A(.*)\s*[\[]\s*[\]]\Z').match


def array_type_converter(target_info, obj):
    """Return Type instance corresponding to Omniscidb `Array` type.

    Omniscidb `Array` is defined as follows (using C++ syntax)::

      template<typename T>
      struct Array {
        T* ptr;
        size_t sz;
        bool is_null;
      }

    Parameters
    ----------
    obj : str
      Specify a string in the form `T[]` where `T` specifies the Array
      items type.
    """
    if isinstance(obj, str):
        m = _array_type_match(obj)
        if m is not None:
            t = typesystem.Type.fromstring(m.group(1), target_info=target_info)
            ptr_t = typesystem.Type(t, '*', name='ptr')
            typename = 'Array<%s>' % (t.toprototype())
            size_t = typesystem.Type.fromstring('size_t sz',
                                                target_info=target_info)
            array_type = typesystem.Type(
                ptr_t,
                size_t,
                typesystem.Type.fromstring('bool is_null',
                                           target_info=target_info),
            )
            array_type_ptr = array_type.pointer()

            # In omniscidb, boolean values are stored as int8 because
            # boolean has three states: false, true, and null.
            numba_type_ptr = ArrayPointer(
                array_type.tonumba(bool_is_int8=True),
                t.tonumba(bool_is_int8=True))

            array_type_ptr._params['typename'] = typename
            array_type_ptr._params['tonumba'] = numba_type_ptr

            return array_type_ptr
