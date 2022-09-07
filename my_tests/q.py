import parablade as pb

details_dict = pb.ReadUserInput(r'./testcases/MatchBlades/Aachen_2D/Aachen_3D.cfg')
o = pb.BladeMatch(details_dict)
o.match_blade(matching_mode='DVs')