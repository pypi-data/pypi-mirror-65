$sarah_file_comment

OnlyLowEnergySPheno = True;

MINPAR = {
	{1, lambdaInput},
$spheno_minpar
};

BoundaryLowScaleInput = {
	(* Standard Model *)
	{λ, lambdaInput}$spheno_boundary_comma
	(* BSM *)
$spheno_boundary
};

(* NOTE: DEFINITION[MatchingConditions] and ParametersToSolveTadpoles should be
         adjusted manually if there are BSM fields which acquire a VEV *)
DEFINITION[MatchingConditions] = {
	{Yu, YuSM},
	{Yd, YdSM},
	{Ye, YeSM},
	{g1, g1SM},
	{g2, g2SM},
	{g3, g3SM},
	{v, vSM}
};

ParametersToSolveTadpoles = {mu2$spheno_parameters_tadpoles};

ListDecayParticles = {Fu, Fd, $spheno_decay_particles};
ListDecayParticles3B = {{Fu, "Fu.f90"}, {Fd, "Fd.f90"}, {Fe, "Fe.f90"}};

