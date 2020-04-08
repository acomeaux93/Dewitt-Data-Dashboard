import dash_bootstrap_components as dbc

def Navbar():
	navbar = dbc.NavbarSimple(
		children=[dbc.NavItem(dbc.NavLink("*Credit Accumulation*", href="/credit-accumulation")),
				dbc.NavItem(dbc.NavLink("*Credit On-Track Percentage*", href="/credit-track")),
				dbc.NavItem(dbc.NavLink("*Period Attendance Heat Map*", href="/attendance-map")),
				dbc.NavItem(dbc.NavLink("*Regents Scores Heat Map*", href="/regents-map")),
				],
			brand="Home",
			brand_href="/home",
			sticky="top",
		)
	return navbar
