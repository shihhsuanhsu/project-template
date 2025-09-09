* This do file install the packages use in this project
* that are not included in the default Stata installation

* list of packages to install
local packages estout xtscc reghdfe distinct

* uncomment below to update the packages if already installed
* local replace , replace

* loop over the packages and install them
foreach package of local packages {
    capture noisily ssc install `package' `replace'
}
