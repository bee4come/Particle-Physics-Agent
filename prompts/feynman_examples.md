# Prompt Examples for TikZ Feynman Generation

---

### Example 1
**Description:** An electron emits a photon and continues as an electron.

**Expected Output:**
```latex
\feynmandiagram [horizontal=a to b] {
a [particle=e⁻] -- [fermion] b -- [fermion] c [particle=e⁻],
b -- [photon] d [particle=γ],
};
```

---

### Example 2
**Description:** A muon and anti-muon annihilate into a Z boson, which decays into an electron and positron.

**Expected Output:**
```latex
\feynmandiagram [horizontal=a to d] {
a [particle=μ⁻] -- [fermion] b -- [fermion] c [particle=μ⁺],
b -- [boson, edge label=Z] d,
d -- [fermion] e [particle=e⁻],
d -- [anti fermion] f [particle=e⁺],
};
