from typing import overload, Tuple, Any, List, Iterable, Iterator, Optional, TypeVar, Union
from .z3types import Ast, ContextObj

class Context:
  ...

class Z3PPObject:
  ...

class AstRef(Z3PPObject):
  @overload
  def __init__(self, ast: Ast, ctx: Context) -> None:
    self.ast: Ast = ...
    self.ctx: Context= ...

  @overload
  def __init__(self, ast: Ast) -> None:
    self.ast: Ast = ...
    self.ctx: Context= ...
  def ctx_ref(self) -> ContextObj:  ...
  def as_ast(self) -> Ast:  ...
  def children(self) -> List[AstRef]: ...
  def eq(self, other: AstRef) -> bool:  ...
  # TODO: Cannot add __eq__ currently: mypy complains conflict with
  # object.__eq__ signature
  #def __eq__(self, other: object) -> ArithRef:  ...

class SortRef(AstRef):
  ...

class FuncDeclRef(AstRef):
  def arity(self) -> int: ...
  def name(self) -> str:  ...
  def __call__(self, *args: ExprRef) -> ExprRef:  ...

class ExprRef(AstRef):
  def sort(self) -> SortRef:  ...
  def decl(self) -> FuncDeclRef:  ...

class BoolSortRef(SortRef):
  ...

class ArraySortRef(SortRef):
  ...

class BoolRef(ExprRef):
  ...


def is_true(a: BoolRef) -> bool:  ...
def is_false(a: BoolRef) -> bool:  ...
def is_int_value(a: AstRef) -> bool:  ...
def substitute(a: AstRef, *m: Tuple[AstRef, AstRef]) -> AstRef: ...
def simplify(a: AstRef, *args: Any, **kwargs: Any) -> AstRef: ...


class ArithSortRef(SortRef):
  ...

class ArithRef(ExprRef):
  def __neg__(self) -> ExprRef: ...
  def __le__(self, other: ArithRef) -> BoolRef:  ...
  def __lt__(self, other: ArithRef) -> BoolRef:  ...
  def __ge__(self, other: ArithRef) -> BoolRef:  ...
  def __gt__(self, other: ArithRef) -> BoolRef:  ...
  def __add__(self, other: ArithRef) -> ArithRef:  ...
  def __sub__(self, other: ArithRef) -> ArithRef:  ...
  def __mul__(self, other: ArithRef) -> ArithRef:  ...
  def __div__(self, other: ArithRef) -> ArithRef:  ...
  def __truediv__(self, other: ArithRef) -> ArithRef:  ...
  def __mod__(self, other: ArithRef) -> ArithRef:  ...

class BitVecSortRef(SortRef):
  ...

class BitVecRef(ExprRef):
  def size(self) -> int:  ...
  def __add__(self, other: Union[BitVecRef, int]) -> BitVecRef:  ...
  def __radd__(self, other: Union[BitVecRef, int]) -> BitVecRef:  ...
  def __mul__(self, other: Union[BitVecRef, int]) -> BitVecRef:  ...
  def __rmul__(self, other: Union[BitVecRef, int]) -> BitVecRef:  ...
  def __sub__(self, other: Union[BitVecRef, int]) -> BitVecRef:  ...
  def __rsub__(self, other: Union[BitVecRef, int]) -> BitVecRef:  ...

  def __or__(self, other: Union[BitVecRef, int]) -> BitVecRef:  ...
  def __ror__(self, other: Union[BitVecRef, int]) -> BitVecRef:  ...
  def __and__(self, other: Union[BitVecRef, int]) -> BitVecRef:  ...
  def __rand__(self, other: Union[BitVecRef, int]) -> BitVecRef:  ...
  def __xor__(self, other: Union[BitVecRef, int]) -> BitVecRef:  ...
  def __rxor__(self, other: Union[BitVecRef, int]) -> BitVecRef:  ...
  def __pos__(self) -> BitVecRef:  ...
  def __neg__(self) -> BitVecRef:  ...
  def __invert__(self) -> BitVecRef:  ...
  def __div__(self, other: BitVecRef) -> BitVecRef:  ...
  def __rdiv__(self, other: BitVecRef) -> BitVecRef:  ...
  def __truediv__(self, other: BitVecRef) -> BitVecRef:  ...
  def __rtruediv__(self, other: BitVecRef) -> BitVecRef:  ...
  def __mod__(self, other: BitVecRef) -> BitVecRef:  ...
  def __rmod__(self, other: BitVecRef) -> BitVecRef:  ...

  def __le__(self, other: BitVecRef) -> BoolRef:  ...
  def __lt__(self, other: BitVecRef) -> BoolRef:  ...
  def __ge__(self, other: BitVecRef) -> BoolRef:  ...
  def __gt__(self, other: BitVecRef) -> BoolRef:  ...


  def __rshift__(self, other: BitVecRef) -> BitVecRef:  ...
  def __lshift__(self, other: BitVecRef) -> BitVecRef:  ...
  def __rrshift__(self, other: BitVecRef) -> BitVecRef:  ...
  def __rlshift__(self, other: BitVecRef) -> BitVecRef:  ...

class BitVecNumRef(BitVecRef):
  def as_long(self) -> int: ...
  def as_signed_long(self) -> int: ...
  def as_string(self) -> str: ...

class IntNumRef(ArithRef):
  def as_long(self) -> int: ...
  def as_string(self) -> str: ...

class SeqSortRef(ExprRef):
  ...

class SeqRef(ExprRef):
  ...

class ReSortRef(ExprRef):
  ...

class ReRef(ExprRef):
  ...

class ArrayRef(ExprRef):
  ...

class CheckSatResult: ...

class ModelRef(Z3PPObject):
  def __getitem__(self, k:  FuncDeclRef) -> IntNumRef:  ...
  def decls(self) -> Iterable[FuncDeclRef]: ...
  def __iter__(self) -> Iterator[FuncDeclRef]:  ...

class FuncEntry:
  def num_args(self) -> int:  ...
  def arg_value(self, idx: int) -> ExprRef:  ...
  def value(self) -> ExprRef:  ...

class FuncInterp(Z3PPObject):
  def else_value(self) -> ExprRef: ...
  def num_entries(self) -> int: ...
  def arity(self) -> int: ...
  def entry(self, idx: int) -> FuncEntry:  ...

class Goal(Z3PPObject):
  ...

class Solver(Z3PPObject):
  ctx:  Context
  def __init__(self, ctx:Optional[Context] = None) -> None: ...

  def to_smt2(self) -> str: ...
  def check(self) -> CheckSatResult: ...
  def push(self) -> None:  ...
  def pop(self, num: Optional[int] = 1) -> None:  ...
  def model(self) -> ModelRef:  ...
  def set(self, *args:  Any, **kwargs:  Any) -> None: ...
  @overload
  def add(self, *args:  Union[BoolRef, Goal]) -> None: ...
  @overload
  def add(self, args:  List[Union[BoolRef, Goal]]) -> None: ...
  def reset(self) -> None:  ...

class Optimize(Z3PPObject):
  ctx:  Context
  def __init__(self, ctx:Optional[Context] = None) -> None: ...

  def check(self) -> CheckSatResult: ...
  def push(self) -> None:  ...
  def pop(self) -> None:  ...
  def model(self) -> ModelRef:  ...
  def set(self, *args:  Any, **kwargs:  Any) -> None: ...
  @overload
  def add(self, *args:  Union[BoolRef, Goal]) -> None: ...
  @overload
  def add(self, args:  List[Union[BoolRef, Goal]]) -> None: ...
  def minimize(self, element: ExprRef) -> None:  ...
  def maximize(self, element: ExprRef) -> None:  ...

sat: CheckSatResult = ...
unsat: CheckSatResult = ...

@overload
def Int(name: str) -> ArithRef: ...
@overload
def Int(name: str, ctx: Context) -> ArithRef: ...

@overload
def Bool(name: str) -> BoolRef: ...
@overload
def Bool(name: str, ctx: Context) -> BoolRef: ...

@overload
def parse_smt2_string(s: str) -> ExprRef: ...
@overload
def parse_smt2_string(s: str, ctx: Context) -> ExprRef: ...

def Array(name: str, domain: SortRef, range: SortRef) -> ArrayRef:  ...
def K(domain: SortRef, v: Union[ExprRef, int, bool, str]) -> ArrayRef:  ...

# Can't give more precise types here since func signature is
# a vararg list of ExprRef optionally followed by a Context
def Or(*args: Any) -> BoolRef: ...
def And(*args: Any) -> BoolRef: ...
def Not(p: BoolRef, ctx: Optional[Context] = None) -> BoolRef: ...
def Implies(a: BoolRef, b: BoolRef, ctx:Context) -> BoolRef: ...

T=TypeVar("T", bound=ExprRef)
def If(a: BoolRef, b: T, c: T, ctx: Optional[Context] = None) -> T: ...
def ULE(a: T, b: T) -> BoolRef:	...
def ULT(a: T, b: T) -> BoolRef:	...
def UGE(a: T, b: T) -> BoolRef:	...
def UGT(a: T, b: T) -> BoolRef:	...
def UDiv(a: T, b: T) -> T:	...
def URem(a: T, b: T) -> T:	...
def SRem(a: T, b: T) -> T:	...
def LShR(a: T, b: T) -> T:	...
def RotateLeft(a: T, b: T) -> T:	...
def RotateRight(a: T, b: T) -> T:	...
def SignExt(n: int, a: BitVecRef) -> BitVecRef:	...
def ZeroExt(n: int, a: BitVecRef) -> BitVecRef:	...

@overload
def Concat(args: List[Union[SeqRef, str]]) -> SeqRef:  ...
@overload
def Concat(*args: Union[SeqRef, str]) -> SeqRef:  ...
@overload
def Concat(args: List[ReRef]) -> ReRef:  ...
@overload
def Concat(*args: ReRef) -> ReRef:  ...
@overload
def Concat(args: List[BitVecRef]) -> BitVecRef:  ...
@overload
def Concat(*args: BitVecRef) -> BitVecRef:  ...

@overload
def Extract(high: Union[SeqRef], lo: Union[int, ArithRef], a: Union[int, ArithRef]) -> SeqRef:  ...
@overload
def Extract(high: Union[int, ArithRef], lo: Union[int, ArithRef], a: BitVecRef) -> BitVecRef:  ...

@overload
def Sum(arg: BitVecRef, *args: Union[BitVecRef, int]) -> BitVecRef:  ...
@overload
def Sum(arg: Union[List[BitVecRef], int]) -> BitVecRef:  ...
@overload
def Sum(arg: ArithRef, *args: Union[ArithRef, int]) -> ArithRef:  ...
# Can't include this overload as it overlaps with the second overload.
#@overload
#def Sum(arg: Union[List[ArithRef], int]) -> ArithRef:  ...

def Function(name: str, *sig: SortRef) -> FuncDeclRef:  ...
def IntVal(val: int, ctx: Optional[Context] = None) -> IntNumRef:  ...
def BoolVal(val: bool, ctx: Optional[Context] = None) -> BoolRef:  ...
def BitVecVal(val: int, bv: Union[int, BitVecSortRef], ctx: Optional[Context] = None) -> BitVecRef:  ...
def BitVec(val: str, bv: Union[int, BitVecSortRef], ctx: Optional[Context] = None) -> BitVecRef:  ...

def IntSort(ctx: Optional[Context] = None) -> ArithSortRef:  ...
def BoolSort(ctx:Optional[Context] = None) -> BoolSortRef:  ...
def ArraySort(domain: SortRef, range: SortRef) -> ArraySortRef:  ...
def BitVecSort(domain:  int, ctx:Optional[Context] = None) -> BoolSortRef:  ...

def ForAll(vs: List[ExprRef], expr: ExprRef) -> ExprRef: ...
def Select(arr: ExprRef, ind: ExprRef) -> ExprRef:  ...
def Update(arr: ArrayRef, ind: ExprRef, newVal: ExprRef) -> ArrayRef:  ...
def Store(arr: ArrayRef, ind: ExprRef, newVal: ExprRef) -> ArrayRef:  ...

def BVAddNoOverflow(a: BitVecRef, b: BitVecRef, signed: bool) -> BoolRef:	...
def BVAddNoUnderflow(a: BitVecRef, b: BitVecRef) -> BoolRef:	...
def BVSubNoOverflow(a: BitVecRef, b: BitVecRef) -> BoolRef:	...
def BVSubNoUnderflow(a: BitVecRef, b: BitVecRef, signed: bool) -> BoolRef:	...
def BVSDivNoOverflow(a: BitVecRef, b: BitVecRef) -> BoolRef:	...
def BVSNegNoOverflow(a: BitVecRef) -> BoolRef:	...
def BVMulNoOverflow(a: BitVecRef, b: BitVecRef, signed: bool) -> BoolRef:	...
def BVMulNoUnderflow(a: BitVecRef, b: BitVecRef) -> BoolRef:	...
