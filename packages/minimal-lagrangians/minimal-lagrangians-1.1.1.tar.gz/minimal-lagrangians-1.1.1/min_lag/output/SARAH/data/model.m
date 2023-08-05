$sarah_file_comment
Off[General::spell];

Model`Name = "$model_name";
Model`NameLaTeX = "$model_name_latex";
Model`Authors = "$model_authors";
Model`Date = "$model_date";

(*-------------------------------------------*)
(*   particle content                        *)
(*-------------------------------------------*)

(* global symmetries *)
(* discrete ℤ₂ symmetry *)
Global[[1]] = {Z[2], Z2};
$model_u1_definition

(* gauge groups *)
Gauge[[1]] = {B,   U[1], hypercharge, g1, False, 1};
Gauge[[2]] = {WB, SU[2], left,        g2, True,  1};
Gauge[[3]] = {G,  SU[3], color,       g3, False, 1};

(* matter fields *)
(*                   {name, gens, components, Y/2,  SU(2), SU(3), global} *)
(* Standard Model *)
FermionFields[[1]] = {q,    3,    {uL, dL},    1/6, 2,      3,    1$model_u1_sm};
FermionFields[[2]] = {l,    3,    {vL, eL},   -1/2, 2,      1,    1$model_u1_sm};
FermionFields[[3]] = {u,    3,    conj[uR],   -2/3, 1,     -3,    1$model_u1_sm};
FermionFields[[4]] = {d,    3,    conj[dR],    1/3, 1,     -3,    1$model_u1_sm};
FermionFields[[5]] = {e,    3,    conj[eR],      1, 1,      1,    1$model_u1_sm};

ScalarFields[[1]]  = {H,    1,    {Hp, H0},    1/2, 2,      1,    1$model_u1_sm};

(* new fields *)
$model_fields_definition

(*----------------------------------------------*)
(*   DEFINITION                                 *)
(*----------------------------------------------*)
NameOfStates = {GaugeES, EWSB};

(* ----- before EWSB ----- *)
DEFINITION[GaugeES][LagrangianInput] = {
	(* Standard Model Lagrangian *)
	{LagNoHC,    {AddHC -> False}},
	{LagHC,      {AddHC -> True }}$model_lagrangian_input_comma
	(* Lagrangian involving the new fields *)
$model_lagrangian_input_list
};

(* Standard Model Lagrangian *)
LagNoHC    = mu2 conj[H].H - 1/2 λ conj[H].H.conj[H].H;
LagHC      = -Yu u.q.H - Yd conj[H].d.q - Ye conj[H].e.l;

(* Lagrangian involving the new fields *)
$model_lagrangian_no_hc
$model_lagrangian_hc

(* ----- after EWSB ----- *)
(* gauge sector mixing *)
DEFINITION[EWSB][GaugeSector] = {
	{{VB,     VWB[3]}, {VP, VZ}, ZZ},
	{{VWB[1], VWB[2]}, {VWp, conj[VWp]}, ZW}
};

(* VEVs *)
DEFINITION[EWSB][VEVs] = {
$model_vev
};

(* mixing *)
DEFINITION[EWSB][MatterSector] = {
	(* Standard Model mixing *)
	{{{uL}, {conj[uR]}}, {{UL, Vu}, {UR, Uu}}},
	{{{dL}, {conj[dR]}}, {{DL, Vd}, {DR, Ud}}},
$model_mixing
};

(* Dirac spinors *)
DEFINITION[EWSB][DiracSpinors] = {
	(* Standard Model Dirac spinors *)
	Fu -> {UL, conj[UR]},
	Fd -> {DL, conj[DR]},
$model_dirac_spinors
};
