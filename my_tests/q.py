import parablade as pb

details_dict = pb.ReadUserInput(r'/home/daep/j.fesquet/git_repos/parablade/testcases/MatchBlades/NASA_R67/NASA_R67.cfg')
o = pb.BladeMatch(details_dict)
o.match_blade(matching_mode='DVs')