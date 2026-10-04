# Prime ideals and Boolean-valued maps

Import `IdealCompletion` or, for only this theory, `IdealCompletion.PrimeIdeal`.
The results below require `[Lattice A]` and `[BoundedOrder A]`, with no
distributivity, finiteness, nontriviality, or decidable-membership assumption.

- [`Order.Ideal.IsPrime.toBoolHom`](../IdealCompletion/PrimeIdeal.lean) sends
  `a : A` to `false` exactly when `a ∈ I`; its `toBoolHom_apply_eq_false_iff`
  and `toBoolHom_apply_eq_true_iff` laws characterize both values.
- [`BoundedLatticeHom.falseIdeal`](../IdealCompletion/PrimeIdeal.lean) is the
  ideal of inputs sent to `false`; `mem_falseIdeal_iff` characterizes its members,
  and `falseIdeal_isPrime` proves primality. Each bounded homomorphism to `Bool`
  is surjective by `surjective_toBool`.
- [`Order.Ideal.primeEquivBoolHom`](../IdealCompletion/PrimeIdeal.lean) packages
  the two constructions as an equivalence. The simp lemmas
  `BoundedLatticeHom.falseIdeal_toBoolHom` and
  `Order.Ideal.IsPrime.toBoolHom_falseIdeal` recover each input. Its forward
  and inverse evaluations have `primeEquivBoolHom_apply` and
  `primeEquivBoolHom_symm_apply` laws. `IsPrime.exists_boolHom` gives the
  pointwise false-fiber characterization and surjectivity together.

The [examples](../IdealCompletionPrimeIdealExamples.lean) give a prime ideal
in `Bool`, an identity false fiber, and the first-coordinate map from
`Bool × Bool`. They also show that `PUnit` has neither a prime order ideal nor
a bounded lattice homomorphism to `Bool`; the equivalence covers this empty case.
The [native generated reference](API.md) documents only an earlier
ideal-completion source revision, as described in its [scope record](README.md).
