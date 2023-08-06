from ..models import State, Chamber, simple_numbered_districts

NE = State(
    name="Nebraska",
    abbr="NE",
    capital="Lincoln",
    capital_tz="America/Chicago",
    fips="31",
    unicameral=True,
    legislature_name="Nebraska Legislature",
    legislature_organization_id="ocd-organization/803c558f-dec2-4f43-9c35-e73a6e849408",
    division_id="ocd-division/country:us/state:ne",
    jurisdiction_id="ocd-jurisdiction/country:us/state:ne/government",
    url="http://nebraskalegislature.gov/",
    legislature=Chamber(
        chamber_type="unicameral",
        name="Nebraska Legislature",
        organization_id="ocd-organization/803c558f-dec2-4f43-9c35-e73a6e849408",
        num_seats=49,
        title="Senator",
        districts=simple_numbered_districts(
            "ocd-division/country:us/state:ne", "legislature", 49
        ),
    ),
)
