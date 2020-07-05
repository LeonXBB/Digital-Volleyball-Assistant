# ABOUT:
# 
# This is a very limited tool for editing protocol up to different rules. 
#
# In current version users can:
#
# 1)exclude some given areas of the protocol, 
# 2)change location of said areas, 
# 3)unite similar areas into groups.
#
# But they can't:
#
# 1)add new areas, 
# 2)change data to display in said areas, 
# 3)for areas with pre-specified character division (see below) where divider is fixed (unlike those depending on the lenght of data to 
# display), specify a divider (it's always equal to corresponding area of the original protocol), 
# 4)specify a border offset for said areas if there is any type of line between characters (it's done automatically for original protocol
# but may not work for other ones, or work incorrectly).

# NAMING CONVENTIONS:
# 
# Generally, each area name consists of 1)Location, 2)Type, 3)Team, 4)Specification, however, it may vary
#
# Valid values for Location: Header, Set#, Teams, Sanctions, Remarks, Approval, Results
#
# Valid values for Type and Team include all the ones below, and only them (as for now). Note that same value in different Location will
# be treaded differently.
#
# Valid values for Specification include either Char + digit for element of the group where character division is specified, or
# _0 for horizontal group, _1 for vertical group. For example, for list of team's players, you could either specify each separate 
# entry box by doing something like TeamsPlayerListTeamAChar3 for the fourth player (indexes start on 0) or TeamPlayerListTeamA_1
# (assuming division in vertical) for the whole list. In this case division will be handled automatically.

# SYNTAX:
#
# *Area Name* = [top_left_x, top_up_y, top_right_x, top_bottom_y] 

# POTENTIAL FUTURE SYNTAX:
#
# areas = [[coordinates], data_to_display, group_data, [border offset and other visual kwargs]]
# (group_data = either ('Non-group'), or ('Char', index), or ('Group', direction))
# 
# The biggest con of this is that the user not only would need to know Python but also the DVA's architecture and the way it works, 
# which is sort of conter-intuitive to modding. Perhaps, use some middle-level special language?

HeaderCompetitionName = [450, 122, 1960, 166]
HeaderMatchCity_0 = [175, 175, 724, 202]
HeaderMatchCourtAddress_0 = [175, 212, 724, 243]
HeaderCompetitionStage = [965, 215, 1060, 245]
HeaderMatchCountryCode_0 = [1240, 180, 1325, 205]
HeaderMatchNumber_0 = [1270, 215, 1325, 245]
HeaderMatchSexMales = [377, 270, 400, 295]
HeaderMatchSexFemales = [505, 270, 528, 295]
HeaderCompetitionAgeSenior = [935, 270, 960, 295]
HeaderCompetitionAgeJunior = [1095, 270, 1120, 295]
HeaderCompetitionAgeYouth = [1245, 270, 1270, 295]
HeaderMatchStartDate_0 = [1440, 190, 1665, 217]
HeaderMatchStartTime_0 = [1795, 190, 1945, 217]
HeaderTeamNameLeft = [1445, 250, 1565, 310]
HeaderTeamNameRight = [1740, 250, 1860, 310]
HeaderTeamLetterLeft = [1400, 255, 1430, 285]
HeaderTeamLetterRight = [1880, 255, 1910, 285]

TeamsLetterLeft = [2645, 1250, 2670, 1280]
TeamsLetterRight = [3160, 1250, 3185, 1280]
TeamsNamesLeft = [2690, 1250, 2835, 1280]
TeamsNamesRight = [3000, 1250, 3145, 1280]
TeamsPlayerNumbersLeft_1 = [2605, 1340, 2635, 1775]
TeamsPlayerNumbersRight_1 = [2920, 1340, 2950, 1775]
TeamsPlayerNamesLeft_1 = [2643, 1335, 2910, 1785]
TeamsPlayerNamesRight_1 = [2963, 1335, 3210, 1785]
TeamsLiberosNumbersLeft_1 = [2605, 1820, 2635, 1887]
TeamsLiberosNumbersRight_1 = [2920, 1820, 2950, 1887]
TeamsLiberosNamesLeft_1 = [2645, 1820, 2910, 1890]
TeamsLiberosNamesRight_1 = [2960, 1820, 3225, 1890]
TeamsHeadCoachLeft = [2605, 1930, 2885, 1960]
TeamsHeadCoachRight = [2945, 1930, 3225, 1960]
TeamStaffLeft_1 = [2605, 1965, 2885, 2065]
TeamStaffRight_1 = [2945, 1965, 3185, 2065]