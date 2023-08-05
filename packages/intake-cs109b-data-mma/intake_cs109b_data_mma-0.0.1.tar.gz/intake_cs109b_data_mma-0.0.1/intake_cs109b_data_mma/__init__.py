import intake
import os

here = os.path.abspath(os.path.dirname(__file__))

# the catalog is a YAML file in the same directory as this init file
cat = intake.open_catalog(os.path.join(here, "nested_catalog.yaml"))
data = cat.main_catalog.shared.original.airpred_clean()  # <- note the parentheses

# after installation, this will be available as intake.cat.cs109b, with one entry, main_catalog
# and intake.cat.airpred_clean, which is a data source.
# intake.cat.cs109b.main_catalog.shared.original.airpred_clean and intake.cat.airpred_clean are identical.
